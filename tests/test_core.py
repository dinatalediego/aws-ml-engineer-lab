from datetime import date

import pandas as pd

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


def test_mastery_formula():
    result = calculate_skill_mastery(sample_skills())
    # 0.2*80 + 0.3*60 + 0.3*40 + 0.2*100 = 66
    assert result.loc[0, "mastery"] == 66.0


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


def test_next_action_refuses_to_optimize_before_h0():
    empty_h0 = pd.DataFrame([{"total_questions": ""}])
    action = next_best_action(sample_skills(), pd.DataFrame(), empty_h0)
    assert action["type"] == "H0"


def test_next_action_uses_priority_after_h0():
    action = next_best_action(sample_skills(), pd.DataFrame(), complete_h0())
    assert action["type"] == "SKILL"
    assert action["skill_id"] in {"D1-01", "D2-01"}
