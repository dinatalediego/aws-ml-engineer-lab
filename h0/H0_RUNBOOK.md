# H0 Runbook — Baseline Without Protection

H0 is not a study module. It is the measurement that determines the study plan.

## Status definition

- **SYSTEM READY** — the diagnostic forms and Command Center exist.
- **H0 PENDING** — the learner has not completed the real baseline.
- **H0 PASSED** — the baseline evidence is complete and the gate in `app/core.py` returns true.

The repository may be SYSTEM READY while H0 remains PENDING. Never mark H0 passed by inventing scores.

## Execution order

### 1. Quantitative official baseline

Use an official AWS practice source referenced in `DIAGNOSTIC_H0.md`.

Before reviewing answers, record:

- selected answer;
- confidence 1–5;
- guessed vs reasoned.

After reviewing, put every meaningful miss into `ERROR_LEDGER.csv`.

Enter aggregate scores in `H0_RESULTS.csv`.

### 2. Practitioner cold questions

Open the Command Center → **H0 Diagnostic**.

Answer all rows in `H0_PRACTITIONER_RESPONSES.csv` closed-book.

Use the rubric:

- 0 — cannot answer;
- 1 — vague recognition;
- 2 — mostly correct definition;
- 3 — correct decision rule;
- 4 — decision rule + trade-off;
- 5 — trade-off + failure/cost/security implication.

Self-score first. An evaluator score may replace the self-score later.

### 3. High-signal discrimination

Complete Part C of `DIAGNOSTIC_H0.md` without notes.

A strong answer is a **decision rule**, not two definitions.

Bad:

> CloudWatch monitors things and CloudTrail records actions.

Better:

> Choose CloudWatch when the question asks about operational metrics/logs/alarms; choose CloudTrail when it asks who called an AWS API and when.

### 4. Blank-page architecture

Attempt Part D on paper or in a markdown file without assistance.

Only after finishing may you compare against AWS documentation or ask for critique.

Set `blank_page_attempted=true` only after the attempt exists.

### 5. Failure diagnosis

Complete Part E using evidence-first reasoning.

The goal is to state what evidence you inspect **before changing configuration**.

### 6. Close the baseline loop

Before setting the final H0 booleans to true:

- all wrong quantitative questions are in the Error Ledger;
- high-confidence wrong answers are explicitly identifiable;
- top five gaps are written;
- a seven-day remediation plan exists;
- strongest transfer skill is named;
- most dangerous false confidence is named;
- weakest AWS-specific area is named;
- highest-leverage next skill is named;
- the mental-model change is written.

Then set:

```text
error_ledger_complete=true
top5_identified=true
remediation_plan_written=true
```

The Command Center will recompute the H0 gate on reload.

## What not to do

Do not:

- study immediately before H0;
- search during cold questions;
- round a domain score upward because the miss felt careless;
- delete embarrassing errors;
- treat a guess as evidence of mastery;
- set completion booleans merely to unlock the dashboard.

## H0 output

A successful H0 produces:

1. a real baseline by domain;
2. first entries in `ERROR_LEDGER.csv`;
3. practitioner scores by category;
4. five ranked gaps;
5. dangerous false-confidence topics;
6. a seven-day remediation plan;
7. the first defensible Next Best Study Action.

That output is the start of H1, not an exam-readiness claim.
