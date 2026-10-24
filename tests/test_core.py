from datetime import date

import pandas as pd
import pytest

from app.core import (
    calculate_skill_mastery,
    certification_readiness,
    evaluate_h0,
    high_confidence_errors,
    next_best_action,
    retention_due,
    skill_priority_table,
)


def sample_skills() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "skill_id": "D1-01",
                "domain": "D1",
                "skill": "Data skill",
                "exam_weight": 28,
                "recall": 80,
                "application": 60,
                "discrimination": 40,
                "retention": 100,
                "state": "APPLIED",
                "next_review": "2026-10-20",
            },
            {
                "skill_id": "D2-01",
                "domain": "D2",
                "skill": "Model skill",
                "exam_weight": 24,
                "recall": 100,
                "application": 100,
                "discrimination": 100,
                "retention": 100,
                "state": "EXAM_READY",
                "next_review": "2026-12-01",
            },
        ]
    )


def complete_h0() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "total_questions": 20,
                "total_correct": 15,
                "overall_pct": 75,
                "d1_pct": 70,
                "d2_pct": 80,
                "d3_pct": 75,
                "d4_pct": 75,
                "blank_page_attempted": True,
                "error_ledger_complete": True,
                "top5_identified": True,
                "remediation_plan_written": True,
                "strongest_transfer": "ML evaluation",
                "false_confidence": "IAM",
                "weakest_aws_area": "Security",
                "highest_leverage_skill": "IAM policies",
                "mental_model_change": "AWS questions are constraint decisions",
            }
        ]
    )


def complete_responses() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "question_id": f"Q{i:02d}",
                "category": "Data",
                "question": "Scenario question",
                "response": "Decision rule with trade-off",
                "self_score_0_5": 4,
                "evaluator_score_0_5": None,
            }
            for i in range(1, 21)
        ]
    )


def complete_gaps() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "rank": i,
                "skill_id_or_topic": f"D4-0{i}",
                "domain": "D4",
                "gap_description": "Specific gap",
                "evidence": "Wrong diagnostic answer",
                "remediation": "Targeted decision card and retest",
            }
            for i in range(1, 6)
        ]
    )


def complete_plan() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "day": i,
                "focus_skill_id_or_topic": "D4-04",
                "objective": "Improve discrimination",
                "exercise": "Scenario drill",
                "evidence_expected": "Decision card + retest",
                "status": "PLANNED",
            }
            for i in range(1, 8)
        ]
    )


def test_mastery_formula():
    result = calculate_skill_mastery(sample_skills())
    assert float(result.loc[0, "mastery"]) == pytest.approx(66.0, abs=1e-9)


def test_readiness_is_blueprint_weighted():
    score = certification_readiness(sample_skills())
    assert 0 <= score <= 100
    assert score > 0


def test_high_confidence_errors_are_prioritized():
    errors = pd.DataFrame(
        [
            {
                "error_id": "E1",
                "skill_id": "D1-01",
                "question_or_scenario": "scenario",
                "confidence_1_5": 5,
                "status": "OPEN",
            }
        ]
    )
    assert len(high_confidence_errors(errors)) == 1
    priorities = skill_priority_table(sample_skills(), errors, as_of=date(2026, 10, 23))
    assert priorities.iloc[0]["skill_id"] == "D1-01"


def test_retention_due_respects_date_and_state():
    due = retention_due(sample_skills(), as_of=date(2026, 10, 23))
    assert due["skill_id"].tolist() == ["D1-01"]


def test_h0_requires_real_evidence():
    pending = pd.DataFrame([{"total_questions": "", "blank_page_attempted": False}])
    assert evaluate_h0(pending).passed is False
    assert evaluate_h0(complete_h0()).passed is True


def test_h0_structured_evidence_is_fail_closed():
    result = evaluate_h0(
        complete_h0(),
        responses=complete_responses().iloc[:10],
        gaps=complete_gaps().iloc[:2],
        plan=complete_plan().iloc[:3],
    )
    assert result.passed is False
    assert any("practitioner responses" in item for item in result.missing)
    assert any("five structured H0 gaps" in item for item in result.missing)
    assert any("seven-day remediation plan" in item for item in result.missing)


def test_h0_passes_with_full_structured_evidence():
    result = evaluate_h0(complete_h0(), complete_responses(), complete_gaps(), complete_plan())
    assert result.passed is True


def test_next_action_refuses_to_optimize_before_h0():
    empty_h0 = pd.DataFrame([{"total_questions": ""}])
    action = next_best_action(sample_skills(), pd.DataFrame(), empty_h0)
    assert action["type"] == "H0"


def test_next_action_uses_priority_after_h0():
    action = next_best_action(
        sample_skills(),
        pd.DataFrame(),
        complete_h0(),
        complete_responses(),
        complete_gaps(),
        complete_plan(),
    )
    assert action["type"] == "SKILL"
    assert action["skill_id"] in {"D1-01", "D2-01"}
