from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

import pandas as pd


DOMAIN_WEIGHTS = {"D1": 28.0, "D2": 24.0, "D3": 24.0, "D4": 24.0}
MASTERY_WEIGHTS = {
    "recall": 0.20,
    "application": 0.30,
    "discrimination": 0.30,
    "retention": 0.20,
}
VALID_STATES = [
    "UNSEEN",
    "EXPOSED",
    "UNDERSTOOD",
    "RECALLED",
    "APPLIED",
    "DISCRIMINATED",
    "RETAINED",
    "EXAM_READY",
]
H0_BOOLEAN_FIELDS = [
    "blank_page_attempted",
    "error_ledger_complete",
    "top5_identified",
    "remediation_plan_written",
]


@dataclass(frozen=True)
class H0Status:
    passed: bool
    missing: tuple[str, ...]
    overall_pct: float | None


def _numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def _truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y", "si", "sí", "pass", "passed"}


def read_csv_or_empty(path: Path, columns: Iterable[str] | None = None) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=list(columns or []))
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=list(columns or []))


def calculate_skill_mastery(skills: pd.DataFrame) -> pd.DataFrame:
    df = skills.copy()
    for column in MASTERY_WEIGHTS:
        if column not in df.columns:
            df[column] = 0.0
        df[column] = _numeric(df[column]).clip(0, 100)

    df["mastery_calc"] = sum(df[col] * weight for col, weight in MASTERY_WEIGHTS.items())
    # The calculated value is authoritative; the CSV mastery column is kept for readability/export.
    df["mastery"] = df["mastery_calc"].round(1)
    return df


def has_learning_evidence(skills: pd.DataFrame, h0_results: pd.DataFrame | None = None) -> bool:
    if not skills.empty:
        score_cols = [c for c in MASTERY_WEIGHTS if c in skills.columns]
        if score_cols and (_numeric(skills[score_cols].stack()) > 0).any():
            return True
        if "last_evidence" in skills.columns and skills["last_evidence"].fillna("").astype(str).str.strip().ne("").any():
            return True
    if h0_results is not None and not h0_results.empty:
        total = pd.to_numeric(h0_results.iloc[0].get("total_questions"), errors="coerce")
        return bool(pd.notna(total) and total > 0)
    return False


def domain_readiness(skills: pd.DataFrame) -> pd.DataFrame:
    df = calculate_skill_mastery(skills)
    rows = []
    for domain, weight in DOMAIN_WEIGHTS.items():
        domain_rows = df[df["domain"] == domain]
        score = float(domain_rows["mastery"].mean()) if not domain_rows.empty else 0.0
        rows.append({"domain": domain, "weight": weight, "readiness": round(score, 1)})
    return pd.DataFrame(rows)


def certification_readiness(skills: pd.DataFrame) -> float:
    domains = domain_readiness(skills)
    if domains.empty:
        return 0.0
    weighted = (domains["readiness"] * domains["weight"]).sum() / sum(DOMAIN_WEIGHTS.values())
    return round(float(weighted), 1)


def clean_error_ledger(errors: pd.DataFrame) -> pd.DataFrame:
    if errors.empty:
        return errors.copy()
    df = errors.copy()
    meaningful = pd.Series(False, index=df.index)
    for col in ["question_or_scenario", "skill_id", "correct_answer", "selected_answer"]:
        if col in df.columns:
            meaningful |= df[col].fillna("").astype(str).str.strip().ne("")
    return df[meaningful].copy()


def open_errors(errors: pd.DataFrame) -> pd.DataFrame:
    df = clean_error_ledger(errors)
    if df.empty:
        return df
    status = df.get("status", pd.Series("OPEN", index=df.index)).fillna("OPEN").astype(str).str.upper()
    return df[~status.isin({"CLOSED", "RESOLVED", "PASS", "PASSED"})].copy()


def high_confidence_errors(errors: pd.DataFrame, threshold: int = 4) -> pd.DataFrame:
    df = open_errors(errors)
    if df.empty:
        return df
    confidence = pd.to_numeric(df.get("confidence_1_5", 0), errors="coerce").fillna(0)
    return df[confidence >= threshold].copy()


def retention_due(skills: pd.DataFrame, as_of: date | None = None) -> pd.DataFrame:
    if skills.empty or "next_review" not in skills.columns:
        return pd.DataFrame(columns=skills.columns)
    today = pd.Timestamp(as_of or date.today()).normalize()
    df = calculate_skill_mastery(skills)
    next_review = pd.to_datetime(df["next_review"], errors="coerce").dt.normalize()
    state = df.get("state", pd.Series("UNSEEN", index=df.index)).fillna("UNSEEN").astype(str).str.upper()
    return df[next_review.notna() & (next_review <= today) & (state != "UNSEEN")].copy()


def skill_priority_table(skills: pd.DataFrame, errors: pd.DataFrame, as_of: date | None = None) -> pd.DataFrame:
    df = calculate_skill_mastery(skills)
    if df.empty:
        return df

    active_errors = open_errors(errors)
    high_conf = high_confidence_errors(errors)
    error_counts = active_errors.get("skill_id", pd.Series(dtype=str)).value_counts()
    high_counts = high_conf.get("skill_id", pd.Series(dtype=str)).value_counts()
    due_ids = set(retention_due(df, as_of=as_of).get("skill_id", pd.Series(dtype=str)).astype(str))

    df["open_error_count"] = df["skill_id"].map(error_counts).fillna(0).astype(int)
    df["high_conf_error_count"] = df["skill_id"].map(high_counts).fillna(0).astype(int)
    df["retention_due"] = df["skill_id"].astype(str).isin(due_ids)

    def importance(row: pd.Series) -> float:
        domain = str(row.get("domain", ""))
        if domain in DOMAIN_WEIGHTS:
            return DOMAIN_WEIGHTS[domain] / max(DOMAIN_WEIGHTS.values())
        return 0.75  # cross-domain capabilities matter, but should not crowd out blueprint domains.

    gap = (100.0 - df["mastery"]).clip(0, 100) / 100.0
    error_boost = (df["open_error_count"].clip(0, 3) / 3.0) * 0.25
    confidence_boost = (df["high_conf_error_count"].clip(0, 2) / 2.0) * 0.30
    retention_boost = df["retention_due"].astype(float) * 0.15
    importance_factor = df.apply(importance, axis=1)

    raw = 100.0 * gap * importance_factor * (1.0 + error_boost + confidence_boost + retention_boost)
    df["priority_score"] = raw.clip(0, 100).round(1)
    return df.sort_values(["priority_score", "mastery"], ascending=[False, True]).reset_index(drop=True)


def critical_gaps(skills: pd.DataFrame, errors: pd.DataFrame, limit: int = 8) -> pd.DataFrame:
    priorities = skill_priority_table(skills, errors)
    if priorities.empty:
        return priorities
    # A critical gap is either weak mastery or an unresolved high-confidence misconception.
    mask = (priorities["mastery"] < 60) | (priorities["high_conf_error_count"] > 0)
    return priorities[mask].head(limit).copy()


def evaluate_h0(h0_results: pd.DataFrame) -> H0Status:
    if h0_results.empty:
        return H0Status(False, ("H0_RESULTS.csv has no result row",), None)

    row = h0_results.iloc[0]
    missing: list[str] = []

    numeric_required = ["total_questions", "total_correct", "overall_pct", "d1_pct", "d2_pct", "d3_pct", "d4_pct"]
    for field in numeric_required:
        value = pd.to_numeric(row.get(field), errors="coerce")
        if pd.isna(value):
            missing.append(field)

    total_questions = pd.to_numeric(row.get("total_questions"), errors="coerce")
    if pd.notna(total_questions) and total_questions <= 0:
        missing.append("total_questions > 0")

    for field in H0_BOOLEAN_FIELDS:
        if not _truthy(row.get(field)):
            missing.append(field)

    text_required = ["strongest_transfer", "false_confidence", "weakest_aws_area", "highest_leverage_skill", "mental_model_change"]
    for field in text_required:
        value = row.get(field)
        if value is None or (isinstance(value, float) and pd.isna(value)) or not str(value).strip():
            missing.append(field)

    overall = pd.to_numeric(row.get("overall_pct"), errors="coerce")
    overall_value = None if pd.isna(overall) else round(float(overall), 1)
    return H0Status(not missing, tuple(missing), overall_value)


def practitioner_baseline(responses: pd.DataFrame) -> pd.DataFrame:
    if responses.empty:
        return pd.DataFrame(columns=["category", "score", "answered", "total"])
    df = responses.copy()
    score = pd.to_numeric(df.get("evaluator_score_0_5"), errors="coerce")
    self_score = pd.to_numeric(df.get("self_score_0_5"), errors="coerce")
    df["effective_score"] = score.where(score.notna(), self_score)
    df["answered"] = df.get("response", "").fillna("").astype(str).str.strip().ne("")
    rows = []
    for category, group in df.groupby("category", dropna=False):
        available = group["effective_score"].dropna()
        rows.append(
            {
                "category": str(category),
                "score": round(float(available.mean()), 2) if not available.empty else None,
                "answered": int(group["answered"].sum()),
                "total": int(len(group)),
            }
        )
    return pd.DataFrame(rows)


def next_best_action(skills: pd.DataFrame, errors: pd.DataFrame, h0_results: pd.DataFrame) -> dict[str, object]:
    h0 = evaluate_h0(h0_results)
    if not h0.passed:
        return {
            "type": "H0",
            "title": "Complete H0 baseline",
            "why": "The system refuses to optimize study before a real baseline exists.",
            "score": 100.0,
            "missing": list(h0.missing),
        }

    priorities = skill_priority_table(skills, errors)
    if priorities.empty:
        return {"type": "NONE", "title": "No skill data", "why": "Populate SKILL_MATRIX.csv", "score": 0.0}

    top = priorities.iloc[0]
    reasons = [f"mastery {top['mastery']:.0f}%"]
    if int(top.get("open_error_count", 0)):
        reasons.append(f"{int(top['open_error_count'])} open error(s)")
    if int(top.get("high_conf_error_count", 0)):
        reasons.append("high-confidence misconception present")
    if bool(top.get("retention_due", False)):
        reasons.append("retention review due")

    return {
        "type": "SKILL",
        "skill_id": top.get("skill_id"),
        "title": top.get("skill"),
        "domain": top.get("domain"),
        "score": float(top.get("priority_score", 0.0)),
        "why": "; ".join(reasons),
    }
