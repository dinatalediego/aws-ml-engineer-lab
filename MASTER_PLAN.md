# MLA-C02 Master Plan — Mastery OS

## Mission

Pass MLA-C02 quickly **without trading away engineering depth**. The repository is optimized for two outputs:

1. **CERTIFY** — recognize exam requirements, eliminate distractors and pass reliably.
2. **ENGINEER** — build, operate, secure and troubleshoot representative ML/AI workloads.

Before the exam the default effort split is `60% CERTIFY / 40% ENGINEER`. After the exam it becomes `20% CERTIFY / 80% ENGINEER`.

---

## 1. The learning loop

Every important skill moves through:

`DIAGNOSE → LEARN → CLOSED-BOOK RECALL → APPLY → DISCRIMINATE → BREAK → RECOVER → RETAIN → SIMULATE → PROMOTE`

### Promotion evidence

A topic cannot be marked mastered from recognition alone. Promotion requires evidence in four dimensions:

- **R — Retrieval:** Can I explain the concept without notes?
- **A — Application:** Can I apply it correctly?
- **D — Discrimination:** Can I choose it over plausible alternatives and explain why?
- **T — Retention:** Can I recover it after a delay?

Default mastery score:

`Mastery = 0.20R + 0.30A + 0.30D + 0.20T`

The weighting is intentionally heavier on application and discrimination.

---

## 2. Mastery states

- `UNSEEN`
- `EXPOSED`
- `UNDERSTOOD`
- `RECALLED`
- `APPLIED`
- `DISCRIMINATED`
- `RETAINED`
- `EXAM_READY`

### Anti-inflation rule

A state can only advance with an evidence link: lab, quiz, architecture note, teach-back, failure analysis, simulation or PR.

---

## 3. Daily protocol

### Full session — 120 minutes

1. **15m Blind recall** — yesterday's concepts, no notes.
2. **25m Learn** — AWS official material focused on one gap.
3. **35m Build** — small lab or architecture exercise.
4. **20m Decide** — scenario questions and service discrimination.
5. **15m Error analysis** — update `ERROR_LEDGER.csv`.
6. **10m Teach-back** — explain one concept as if mentoring another engineer.

### Compressed session — 60 minutes

`10 recall → 20 learn → 20 questions → 10 errors`

A day with only passive consumption does not count as a complete study session.

---

## 4. Spaced revalidation

Every important error or fragile concept returns at:

- Day 1
- Day 3
- Day 7
- Day 14

If it fails again, its state is reopened. "I studied this already" is not evidence.

---

## 5. Error taxonomy

Every wrong answer gets a root-cause code:

- `K` — knowledge gap
- `C` — confused similar services/patterns
- `T` — missed trade-off
- `R` — misread dominant requirement
- `E` — English / interpretation issue
- `S` — security gap
- `O` — operations / MLOps gap
- `G` — GenAI / Bedrock gap
- `H` — high-confidence wrong mental model

`H` errors receive maximum remediation priority because certainty plus incorrect reasoning is more dangerous than an admitted gap.

---

## 6. Next-best-study-action engine

Prioritize gaps instead of studying whatever feels interesting.

Suggested priority formula:

`Priority = ExamWeight × (100 - Mastery) × ErrorFrequency × ConfidencePenalty`

Where `ConfidencePenalty` increases sharply for high-confidence wrong answers.

The next session should usually attack the top one or two priority gaps, not open a new topic.

---

## 7. Anti-skip gates

A module is not closed until:

- G1 — explain without notes;
- G2 — solve a realistic scenario;
- G3 — produce a reproducible lab where appropriate;
- G4 — explain why plausible alternatives lose;
- G5 — score at least 80% on focused questions;
- G6 — pass delayed revalidation;
- G7 — close related Error Ledger entries with evidence.

### Break-it gate

For operational skills, deliberately introduce a failure and diagnose it from evidence before changing things.

Preferred failure record:

`failure → symptom → evidence → root cause → fix → prevention`

---

## 8. Practitioner review questions

Every meaningful lab must answer:

1. What business/technical requirement dominates this design?
2. What is the simplest AWS pattern that satisfies it?
3. Which plausible alternative did I reject, and why?
4. What breaks first at 10× scale?
5. What would make this expensive?
6. What security boundary matters most?
7. What telemetry proves it is healthy?
8. What failure would be silent if I did not instrument it?
9. What is stateful, and where does state live?
10. What must be reproducible/versioned?
11. What would trigger rollback or retraining?
12. Where is human approval justified?
13. What part should be managed rather than custom-built?
14. If GenAI is present, why is deterministic logic or traditional ML insufficient?
15. What evidence would make me stop trusting the model or agent?

These questions are intentionally harder than the exam. They prevent shallow certification knowledge.

---

## 9. Project sequence

### P01 — Production ML Pipeline

Synthetic lead-scoring style dataset:

`S3 → preparation → training → evaluation → registry → approval → deployment → monitoring`

Primary skills: SageMaker AI, data flow, deployment choices, model lifecycle, monitoring, IAM.

### P02 — Bedrock RAG

`documents → S3 → chunking → embeddings → retrieval/vector store → Bedrock → evaluation → guardrails`

Primary skills: FM selection, RAG trade-offs, freshness, retrieval quality, safety, observability and cost.

### P03 — Agentic AI Operations

`signal → agent reasoning → tool call → evidence → approval → action → observability`

Primary skills: tool boundaries, permissions, state, failure modes, versioning, human-in-the-loop and cost.

### P04 — Failure & Recovery Lab

A collection of deliberately broken workloads covering IAM, S3, KMS, endpoint configuration, malformed data, secrets, monitoring and deployment failure.

---

## 10. Weekly review

At the end of each week record:

- current readiness;
- domain scores;
- strongest evidence created;
- top 5 unresolved gaps;
- high-confidence errors;
- concepts due for delayed retrieval;
- weakest practitioner FAQ categories;
- next week's single highest-leverage capability.

Do not optimize for number of commits, notebooks or hours.

---

## 11. Certification gate

Do not use the official 720 scaled passing standard as the study target. Our internal readiness gate is deliberately safer:

- 2 full simulations ≥80%;
- no domain <70%;
- critical gaps = 0;
- high-confidence wrong answers <3%;
- 7-day retention ≥80%;
- representative blank-page architecture defense passed.

If one condition is missing, readiness remains `NOT YET`.

---

## 12. Practitioner promotion gate

Certification readiness and practitioner readiness are different.

A practitioner-level project must additionally include:

- reproducible setup;
- architecture and trade-off notes;
- cost awareness;
- least-privilege reasoning;
- monitoring and failure signals;
- tests or deterministic checks where applicable;
- at least one deliberately induced failure and recovery;
- versioning and rollback/recovery thinking;
- explanation for an engineer, an executive and a data scientist/economist.

---

## 13. Source hierarchy

1. AWS MLA-C02 Exam Guide
2. AWS service documentation
3. AWS Skill Builder / official practice material
4. AWS Builder Labs / SimuLearn / official hands-on material
5. This repository's distilled notes
6. Third-party courses, blogs and videos

When sources disagree, move upward in this hierarchy.

---

## 14. Meta-rule

> We are not trying to know more AWS. We are trying to make better ML-engineering decisions on AWS with less uncertainty, less wasted complexity and stronger evidence.
