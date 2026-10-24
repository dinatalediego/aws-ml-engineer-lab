# Practitioner Gates by Milestone

This file connects `CHALLENGE_MILESTONES.md` to `FAQ_ELITE_PRACTITIONERS.md`.

A milestone is not complete because its lab exists. It is complete when the lab evidence and the practitioner's reasoning agree.

## Gate protocol

For the current milestone:

1. select 3 FAQ questions from the matching section at random;
2. answer closed-book;
3. score each answer using the 0–5 rubric;
4. require average ≥4.0;
5. no answer may score below 3;
6. if a question exposes a wrong mental model, create an `ERROR_LEDGER.csv` entry even if no exam question was missed;
7. repeat failed questions after 1, 3, 7 and 14 days.

## Mapping

| Milestone | Practitioner focus | Gate challenge |
|---|---|---|
| H0 | epistemic calibration | identify strongest knowledge gap and most dangerous false confidence |
| H1 | service discrimination | solve 10 service-choice scenarios and reject alternatives |
| H2 | data engineering | redesign one pipeline after a changed freshness/scale requirement |
| H3 | model development | defend metric, model and evaluation choices without console or notes |
| H4 | deployment | map 5 workloads to inference modes under latency/cost constraints |
| H5 | MLOps | reproduce a new model version from changed data without manual notebook choreography |
| H6 | troubleshooting | diagnose an unknown injected failure from logs/evidence first |
| H7 | monitoring | separate infra, data, model and audit failures in a mixed incident |
| H8 | security | reduce blast radius of an intentionally over-permissioned architecture |
| H9 | GenAI/RAG | choose RAG, fine-tuning, traditional ML or rules for 4 different problems |
| H10 | agentic AI | contain an agent that selects a wrong tool or receives a malicious/bad tool response |
| H11 | architecture | design and defend a new workload from a blank page in 40 minutes |
| H12 | exam readiness | meet all quantitative readiness gates under timed conditions |
| H13 | portfolio | defend the same project to engineer, executive and data-science audiences |

## Practitioner red flags

Do **not** promote a milestone if any of these appear repeatedly:

- “AWS recommends it” without knowing the requirement;
- “it scales” without a workload estimate;
- “it is secure” without naming identity/resource/action boundaries;
- “it is monitored” without saying what failure signal triggers what action;
- “we can retrain” without a promotion/evaluation gate;
- “use RAG” without explaining why retrieval is the problem;
- “use a larger model” without latency/cost/quality evidence;
- “use serverless” without considering latency/cold-start constraints;
- “encrypt with KMS” as a substitute for authorization;
- “the endpoint is healthy” as proof the model is good;
- “the model improved” based on a single metric or non-comparable evaluation;
- debugging by changing configuration before collecting evidence.

## Practitioner green flags

Promote faster when the answer naturally includes:

- explicit dominant requirement;
- rejected alternatives;
- measurable trade-offs;
- failure and rollback path;
- least-privilege boundary;
- evidence/telemetry source;
- cost implications;
- versioned artifacts and lineage;
- acknowledgement of uncertainty;
- simpler solution when complexity adds no value.

## Final rule

> The purpose of the FAQ is not to memorize ideal answers. It is to expose whether the underlying decision rule survives a changed scenario.
