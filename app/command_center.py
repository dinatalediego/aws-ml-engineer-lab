from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from core import (
    certification_readiness,
    clean_error_ledger,
    critical_gaps,
    domain_readiness,
    evaluate_h0,
    has_learning_evidence,
    high_confidence_errors,
    next_best_action,
    practitioner_baseline,
    read_csv_or_empty,
    retention_due,
    skill_priority_table,
)


ROOT = Path(__file__).resolve().parents[1]
SKILLS_PATH = ROOT / "SKILL_MATRIX.csv"
ERRORS_PATH = ROOT / "ERROR_LEDGER.csv"
H0_RESULTS_PATH = ROOT / "h0" / "H0_RESULTS.csv"
H0_RESPONSES_PATH = ROOT / "h0" / "H0_PRACTITIONER_RESPONSES.csv"

st.set_page_config(page_title="MLA-C02 Command Center", page_icon="🧠", layout="wide")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    skills = read_csv_or_empty(SKILLS_PATH)
    errors = read_csv_or_empty(ERRORS_PATH)
    h0_results = read_csv_or_empty(H0_RESULTS_PATH)
    h0_responses = read_csv_or_empty(H0_RESPONSES_PATH)
    return skills, errors, h0_results, h0_responses


def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def fmt_pct(value: float | None) -> str:
    return "—" if value is None else f"{value:.1f}%"


skills, errors, h0_results, h0_responses = load_data()
h0 = evaluate_h0(h0_results)
measured = has_learning_evidence(skills, h0_results)
readiness = certification_readiness(skills) if measured else None
domains = domain_readiness(skills)
high_conf = high_confidence_errors(errors)
due = retention_due(skills)
gaps = critical_gaps(skills, errors)
priority = skill_priority_table(skills, errors)
action = next_best_action(skills, errors, h0_results)

st.title("AWS MLA-C02 Command Center v0.1")
st.caption("Evidence-driven study control: diagnose → prioritize → practice → revalidate.")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Certification readiness", fmt_pct(readiness))
col2.metric("H0", "PASSED" if h0.passed else "PENDING")
col3.metric("Critical gaps", int(len(gaps)))
col4.metric("Retention due", int(len(due)))
col5.metric("High-confidence errors", int(len(high_conf)))

if not measured:
    st.info("Readiness is intentionally not estimated yet. Complete H0 before using the dashboard as a study optimizer.")

st.subheader("Next Best Study Action")
if action["type"] == "H0":
    st.warning(f"**{action['title']}** — {action['why']}")
    with st.expander("What is still missing from H0?", expanded=True):
        for item in action.get("missing", []):
            st.write(f"- {item}")
elif action["type"] == "SKILL":
    st.success(f"**{action.get('skill_id')} · {action['title']}**")
    st.write(f"Priority: **{action['score']:.1f}/100** · {action.get('domain')} · {action['why']}")
else:
    st.info(action["why"])

overview_tab, gaps_tab, retention_tab, errors_tab, h0_tab, data_tab = st.tabs(
    ["Overview", "Critical Gaps", "Retention", "Error Intelligence", "H0 Diagnostic", "Data Editor"]
)

with overview_tab:
    st.subheader("Domain readiness")
    domain_display = domains.copy()
    if not measured:
        domain_display["readiness"] = pd.NA
    st.dataframe(domain_display, use_container_width=True, hide_index=True)

    if measured:
        chart = domains.set_index("domain")[["readiness"]]
        st.bar_chart(chart)

    st.subheader("Highest-leverage capabilities")
    cols = [
        "skill_id",
        "domain",
        "skill",
        "mastery",
        "priority_score",
        "open_error_count",
        "high_conf_error_count",
        "retention_due",
    ]
    st.dataframe(priority[cols].head(12) if not priority.empty else priority, use_container_width=True, hide_index=True)

    st.subheader("Operating gates")
    gate_rows = [
        {"gate": "H0 baseline completed", "status": h0.passed},
        {"gate": "No domain below 70%", "status": measured and bool((domains["readiness"] >= 70).all())},
        {"gate": "Critical gaps = 0", "status": measured and len(gaps) == 0},
        {"gate": "No high-confidence open errors", "status": measured and len(high_conf) == 0},
        {"gate": "No overdue retention", "status": measured and len(due) == 0},
    ]
    st.dataframe(pd.DataFrame(gate_rows), use_container_width=True, hide_index=True)

with gaps_tab:
    st.subheader("Critical Gaps")
    st.caption("A gap is critical when mastery is below 60% or a high-confidence misconception remains unresolved.")
    if gaps.empty:
        st.success("No critical gaps under the current evidence.")
    else:
        show = [
            "skill_id",
            "domain",
            "skill",
            "mastery",
            "priority_score",
            "open_error_count",
            "high_conf_error_count",
            "retention_due",
        ]
        st.dataframe(gaps[show], use_container_width=True, hide_index=True)

with retention_tab:
    st.subheader("Retention Due")
    st.caption("A skill only appears here after it has a next_review date and is no longer UNSEEN.")
    if due.empty:
        st.info("No retention reviews are due.")
    else:
        st.dataframe(
            due[["skill_id", "domain", "skill", "mastery", "last_review", "next_review"]],
            use_container_width=True,
            hide_index=True,
        )

with errors_tab:
    meaningful_errors = clean_error_ledger(errors)
    st.subheader("Error Intelligence")
    e1, e2, e3 = st.columns(3)
    e1.metric("Recorded errors", len(meaningful_errors))
    e2.metric("Open high-confidence", len(high_conf))
    closed_count = max(len(meaningful_errors) - len(meaningful_errors[meaningful_errors.get("status", "OPEN").fillna("OPEN").astype(str).str.upper().isin(["OPEN", "REOPEN", "PENDING"])]), 0) if not meaningful_errors.empty else 0
    e3.metric("Closed / resolved", closed_count)

    if not high_conf.empty:
        st.error("High-confidence errors are priority misconceptions. They should be repaired before broadening study.")
        st.dataframe(
            high_conf[[c for c in ["error_id", "domain", "skill_id", "question_or_scenario", "confidence_1_5", "mental_model_after", "status"] if c in high_conf.columns]],
            use_container_width=True,
            hide_index=True,
        )

    if meaningful_errors.empty:
        st.info("No meaningful errors recorded yet. H0 should create the first entries.")
    else:
        st.dataframe(meaningful_errors, use_container_width=True, hide_index=True)

with h0_tab:
    st.subheader("H0 — Baseline Without Protection")
    st.write("H0 is complete only when real diagnostic evidence exists. This application will not synthesize a score.")

    if h0.passed:
        st.success(f"H0 PASSED · quantitative baseline {fmt_pct(h0.overall_pct)}")
    else:
        st.warning("H0 is still pending.")
        for item in h0.missing:
            st.write(f"- {item}")

    st.markdown("### Quantitative baseline")
    if h0_results.empty:
        st.error("Missing h0/H0_RESULTS.csv")
    else:
        edited_results = st.data_editor(h0_results, use_container_width=True, num_rows="fixed", key="h0_results_editor")
        if st.button("Save H0 quantitative baseline", type="primary"):
            save_csv(edited_results, H0_RESULTS_PATH)
            st.success("Saved. Reload the page to recompute gates.")

    st.markdown("### Practitioner cold questions")
    baseline = practitioner_baseline(h0_responses)
    if not baseline.empty:
        st.dataframe(baseline, use_container_width=True, hide_index=True)
    if h0_responses.empty:
        st.error("Missing h0/H0_PRACTITIONER_RESPONSES.csv")
    else:
        edited_responses = st.data_editor(h0_responses, use_container_width=True, num_rows="fixed", key="h0_response_editor")
        if st.button("Save practitioner responses"):
            save_csv(edited_responses, H0_RESPONSES_PATH)
            st.success("Saved. Use evaluator_score_0_5 when a response has been reviewed.")

with data_tab:
    st.subheader("Local evidence editor")
    st.caption("Edits write to your local checkout. Commit them only after reviewing the diff.")

    st.markdown("### Skill Matrix")
    skills_editor = st.data_editor(skills, use_container_width=True, num_rows="fixed", key="skills_editor")
    if st.button("Save SKILL_MATRIX.csv"):
        save_csv(skills_editor, SKILLS_PATH)
        st.success("SKILL_MATRIX.csv saved locally.")

    st.markdown("### Error Ledger")
    errors_editor = st.data_editor(errors, use_container_width=True, num_rows="dynamic", key="errors_editor")
    if st.button("Save ERROR_LEDGER.csv"):
        save_csv(errors_editor, ERRORS_PATH)
        st.success("ERROR_LEDGER.csv saved locally.")

st.divider()
st.caption("Rule: a dashboard is not evidence. Every score must trace back to a diagnostic, lab, decision card, failure lab, teach-back, or simulation.")
