# H0 Diagnostic — Baseline Without Protection

## Purpose

Establish the true starting point before studying. The objective is not to score well. The objective is to separate:

- knowledge I can retrieve;
- knowledge I only recognize;
- concepts I confuse;
- AWS-specific gaps;
- fragile high-confidence mental models.

## Rules

- closed book;
- no console;
- no notes;
- no searching;
- no pausing to study between questions;
- record confidence **before** checking the answer;
- wrong answers must enter `ERROR_LEDGER.csv`.

## Recommended sources

Use official AWS material first:

1. AWS Certification Official Practice Question Set;
2. AWS Certification Official Pretest;
3. additional official exam-style questions from the MLA-C02 Exam Prep Plan.

Do not use leaked exam dumps.

---

## Part A — Quantitative baseline

Record:

| Metric | Result |
|---|---|
| Date | |
| Total questions | |
| Total correct | |
| Overall % | |
| D1 % | |
| D2 % | |
| D3 % | |
| D4 % | |
| High-confidence wrong count | |
| Questions where English was the main issue | |
| Questions guessed | |

### Initial risk labels

- **RED:** <60%
- **AMBER:** 60–74%
- **LIGHT GREEN:** 75–84%
- **GREEN:** ≥85%

These are training labels, not AWS scoring equivalents.

---

# Part B — Practitioner cold questions

Answer without notes in 2–4 sentences each.

## Data

1. When would you choose Glue over SageMaker Processing?
2. Why might Parquet reduce both cost and latency versus CSV?
3. What requirement justifies moving from batch ingestion to streaming?
4. What is training-serving skew and how would you prevent it?
5. What belongs in an online feature store that does not belong only offline?

## Models / foundation models

6. When is traditional gradient-boosted ML a better production choice than an LLM?
7. What problem does RAG solve that fine-tuning usually does not?
8. What problem can fine-tuning solve that RAG usually does not?
9. Why can accuracy be a misleading objective?
10. How would you evaluate retrieval quality separately from answer generation?

## Deployment / MLOps

11. Give one workload for each: real-time, serverless, async, batch inference.
12. What should be versioned besides the model weights/artifact?
13. What should trigger retraining?
14. Where would you put a human approval gate and why?
15. What is the difference between a repeatable pipeline and a notebook someone reruns manually?

## Operations / security

16. CloudWatch vs CloudTrail: what evidence does each answer?
17. Model Monitor vs endpoint health monitoring: what different failures are you looking for?
18. KMS vs Secrets Manager: what problem does each solve?
19. Why is `AdministratorAccess` an operational smell even in a successful prototype?
20. What evidence would make you automatically disable or roll back a model?

---

# Part C — High-signal discrimination

For each pair, write **one sentence that separates them by dominant requirement**:

- Glue vs SageMaker Processing
- Kinesis vs batch ingestion
- Feature Store online vs offline
- RAG vs fine-tuning
- prompt engineering vs RAG
- real-time vs serverless inference
- async inference vs batch transform
- SageMaker Pipelines vs Step Functions
- CloudWatch vs CloudTrail
- CloudWatch vs Model Monitor
- KMS vs Secrets Manager
- IAM policy vs Bedrock Guardrail

If the answer is a definition rather than a decision rule, mark it weak.

---

# Part D — Blank-page architecture

Design in 30 minutes:

> A company wants to score incoming leads, return a probability to an application, retrain periodically, detect model degradation, protect PII, and preserve evidence of who deployed each model version.

Your design must cover:

- ingestion;
- storage;
- transformation/features;
- training;
- evaluation;
- registry/versioning;
- deployment mode;
- monitoring;
- audit trail;
- permissions/encryption;
- retraining trigger;
- rollback.

Then answer:

1. What is the dominant requirement?
2. What did you deliberately *not* add?
3. What breaks first at 10× traffic?
4. What is the most dangerous silent failure?
5. What would you change if requests become sporadic?

---

# Part E — Failure diagnosis

For each symptom, state the **first evidence source you would inspect** before changing configuration:

1. Endpoint returns 5xx after deployment.
2. Training job cannot read an S3 object.
3. Model predictions look valid but performance has degraded for weeks.
4. A user asks who changed an AWS resource last night.
5. Bedrock tool calls are succeeding but an agent is taking unauthorized business actions.

The goal is to diagnose before experimenting.

---

# Scoring the practitioner baseline

Score each cold question:

- 0 — cannot answer;
- 1 — vague recognition;
- 2 — mostly correct definition;
- 3 — correct decision rule;
- 4 — decision rule + trade-off;
- 5 — trade-off + failure/cost/security implication.

Calculate average by category.

A certification-ready answer often needs level 3. A strong practitioner target is level 4–5.

---

# H0 completion gate

H0 passes only when:

- quantitative baseline recorded;
- domain weaknesses ranked;
- all wrong questions entered into the Error Ledger;
- every high-confidence wrong answer tagged `H` in addition to its root cause in notes;
- top 5 gaps identified;
- first seven-day remediation plan written;
- blank-page architecture attempted without assistance.

## Final H0 note

Complete:

**My strongest transfer skill:**

...

**My most dangerous false confidence:**

...

**My weakest AWS-specific area:**

...

**My highest-leverage next skill:**

...

**What changed in my mental model after the diagnostic:**

...
