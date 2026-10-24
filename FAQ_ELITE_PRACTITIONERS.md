# Elite Practitioner FAQ — MLA-C02 and Beyond

> These are not trivia questions. They are prompts used to reveal whether a mental model is operational, superficial, or dangerously overconfident.
>
> A strong answer usually contains: **requirement → decision → rejected alternative → trade-off → failure mode → evidence**.

---

# H0 — Baseline: do I actually know what I think I know?

### Q1. How do you distinguish familiarity from competence?
**Strong answer:** familiarity recognizes terminology; competence can retrieve the concept without cues, apply it to a new constraint, reject alternatives and diagnose failure.

### Q2. Why are high-confidence wrong answers more valuable than low-confidence wrong answers?
**Strong answer:** they reveal an incorrect mental model rather than a missing fact. They deserve priority because the same bad rule will produce repeated errors.

### Q3. What should a baseline measure besides percent correct?
**Strong answer:** domain, confidence, error type, time, guessed answers, English/reading issues, repeated confusion pairs and ability to explain the dominant requirement.

---

# H1 — Choosing services rather than naming services

### Q1. What makes an AWS answer “better” when several options technically work?
**Strong answer:** the best answer satisfies every explicit requirement with the least unnecessary operational burden, cost and complexity.

### Q2. What is your procedure when two services both seem valid?
**Strong answer:** identify the hard constraint, state what each service optimizes, then eliminate the one that violates or over-solves the requirement.

### Q3. Why is knowing when *not* to use a service a stronger signal than defining it?
**Strong answer:** real engineering is selection under constraints; definitions do not expose trade-off understanding.

---

# H2 — Data preparation

### Q1. Glue or SageMaker Processing?
**Strong answer:** choose based on where the transformation belongs operationally, ML-specific integration needs, scale, framework and orchestration—not by brand familiarity.

### Q2. Why is Parquet often preferable for analytical ML data?
**Strong answer:** columnar reads, compression and predicate/column pruning can reduce scanned data, latency and cost; CSV can still be appropriate for small/interchange workloads.

### Q3. What is the hidden danger in a perfectly reproducible feature pipeline?
**Strong answer:** it can reproducibly leak future information or produce train/serve skew. Reproducibility does not imply validity.

### Q4. When does streaming become justified?
**Strong answer:** when freshness/latency requirements create business value or an operational SLO that batch cannot meet—not because streaming is more sophisticated.

### Q5. What is the first thing you verify when an ML input dataset suddenly shrinks?
**Strong answer:** pipeline completeness and upstream ingestion/partition evidence before blaming the model.

---

# H3 — Training and model development

### Q1. What is the most important artifact produced by a training job?
**Strong answer:** not only model weights; reproducible lineage linking data/version, code, parameters, environment, metrics and model artifact.

### Q2. When can threshold tuning outperform retraining as the next action?
**Strong answer:** when ranking/probabilities remain useful but the business cost of false positives/negatives changed or the operating point is poorly chosen.

### Q3. Why is a better offline metric not automatically a better model?
**Strong answer:** metric choice may not represent business utility, latency, stability, fairness, calibration or production distribution.

### Q4. What makes a model comparison trustworthy?
**Strong answer:** same evaluation contract, representative data, versioned inputs, uncertainty/variance awareness and no leakage.

---

# H4 — Deployment

### Q1. Real-time vs serverless inference?
**Strong answer:** persistent predictable low-latency workloads favor provisioned real-time; intermittent traffic can favor serverless when cold-start/feature limitations meet the SLO.

### Q2. Async inference vs Batch Transform?
**Strong answer:** async is request-oriented inference where callers submit payloads and results arrive later; batch transform is dataset/job-oriented bulk inference.

### Q3. What does autoscaling fail to solve?
**Strong answer:** bad model architecture, excessive cold starts, downstream bottlenecks, malformed requests, poor concurrency assumptions and an impossible SLO.

### Q4. When is a GPU a bad engineering decision?
**Strong answer:** when acceleration does not materially improve required throughput/latency enough to justify cost and operational constraints.

### Q5. What is the deployment question people ask too late?
**Strong answer:** “How do we roll this back safely?”

---

# H5 — MLOps

### Q1. What is the minimum unit of reproducibility in ML?
**Strong answer:** code + data/version + features + configuration + dependencies + model artifact + evaluation contract; the model file alone is insufficient.

### Q2. Scheduled retraining or drift-triggered retraining?
**Strong answer:** neither is universally superior. Triggering should follow data arrival, degradation, business cadence, cost and risk; retraining should not automatically imply promotion.

### Q3. What is the difference between automation and orchestration?
**Strong answer:** automation executes tasks; orchestration coordinates dependencies, state, retries, conditions, artifacts and lifecycle across tasks.

### Q4. Why separate model registration from deployment?
**Strong answer:** it creates a governed promotion boundary, preserves lineage and enables approval/testing/rollback before production exposure.

### Q5. What should never be silently mutable in an ML pipeline?
**Strong answer:** inputs that determine model behavior—data references, feature definitions, code/environment, hyperparameters, evaluation criteria and model versions.

---

# H6 — Failure and recovery

### Q1. What is the first rule of troubleshooting?
**Strong answer:** collect evidence before changing the system; otherwise the intervention can erase the signal and create a second failure.

### Q2. How do you distinguish permission failure from network failure?
**Strong answer:** inspect the error path and evidence source: authorization/audit policy evaluation versus reachability/DNS/security-group/route behavior.

### Q3. Why is “I fixed it” incomplete?
**Strong answer:** a production-quality resolution also identifies root cause, prevention, detection and whether the same class of failure exists elsewhere.

### Q4. What makes a failure lab valuable?
**Strong answer:** reproducibility, a known fault, observable symptoms, a disciplined diagnostic path and a documented prevention control.

---

# H7 — Monitoring

### Q1. CloudWatch vs CloudTrail?
**Strong answer:** CloudWatch answers operational health/metrics/log questions; CloudTrail answers API/action audit questions such as who changed what and when.

### Q2. Model monitoring vs endpoint monitoring?
**Strong answer:** a healthy endpoint can serve systematically bad predictions. Infrastructure health and model/data behavior are separate observability planes.

### Q3. What is a silent model failure?
**Strong answer:** the service remains technically available while decision quality degrades without triggering infrastructure alarms.

### Q4. Data drift or concept drift?
**Strong answer:** data drift changes input distribution; concept drift changes the relationship between inputs and target. Operational diagnosis requires different evidence and often delayed ground truth for concept drift.

### Q5. What makes an alert bad?
**Strong answer:** no owner, no action, no useful threshold, excessive noise, or a metric that does not map to user/business impact.

---

# H8 — Security

### Q1. Why is encryption not authorization?
**Strong answer:** encryption protects data confidentiality at rest/in transit; authorization controls who or what may perform an action. One does not replace the other.

### Q2. KMS vs Secrets Manager?
**Strong answer:** KMS manages cryptographic keys and cryptographic permissions; Secrets Manager manages secret values and their lifecycle/rotation, commonly protected using KMS.

### Q3. What is the practical meaning of least privilege?
**Strong answer:** grant the smallest actions/resources/conditions necessary for the workload, then verify through actual access patterns rather than using wildcard permissions indefinitely.

### Q4. Why are broad agent permissions especially dangerous?
**Strong answer:** a probabilistic planner can select an unintended action; tool authorization must constrain impact independently of model intent.

### Q5. What is the strongest question to ask in a security review?
**Strong answer:** “If this identity, model or tool is compromised or wrong, what is the maximum action it can perform?”

---

# H9 — Bedrock, RAG and foundation models

### Q1. RAG or fine-tuning?
**Strong answer:** RAG primarily supplies external/fresh knowledge at inference; fine-tuning changes model behavior/style/task adaptation. They can be complementary and neither fixes every quality problem.

### Q2. Why can retrieval quality dominate generation quality?
**Strong answer:** a strong generator grounded on irrelevant/missing context cannot reliably recover facts that retrieval failed to supply.

### Q3. When is an LLM the wrong answer?
**Strong answer:** deterministic business rules, structured prediction with cheaper conventional ML, strict exactness requirements, or tasks where latency/cost/control outweigh language flexibility.

### Q4. How do you evaluate RAG correctly?
**Strong answer:** separate retrieval metrics/coverage from generation faithfulness/relevance, then evaluate end-to-end user/business outcomes.

### Q5. What does a Guardrail not replace?
**Strong answer:** IAM/tool authorization, data-access controls, application validation, evaluation and business approval boundaries.

### Q6. Why can a smaller FM be the better production model?
**Strong answer:** sufficient quality with materially better latency, cost, throughput or controllability can dominate marginal benchmark gains.

---

# H10 — Agentic AI

### Q1. What is an agent from an operations perspective?
**Strong answer:** an orchestrated system that combines probabilistic planning with tools, permissions, state and side effects; it must be operated like software, not judged like a chatbot demo.

### Q2. Where should authorization live?
**Strong answer:** at the tool/action boundary, not only in the prompt or agent reasoning layer.

### Q3. How do you evaluate an agent?
**Strong answer:** task success, tool-selection quality, unsafe/invalid actions, retries, latency, cost, trajectory quality and recovery behavior—not just final-answer fluency.

### Q4. What is the most dangerous agent failure?
**Strong answer:** a plausible-looking successful response paired with an incorrect or unauthorized side effect.

### Q5. When should a human approve an agent action?
**Strong answer:** when reversibility is low, financial/security/legal impact is meaningful, confidence is insufficient or the action crosses a governance threshold.

---

# H11 — Blank-page architecture

### Q1. What should you decide before choosing AWS services?
**Strong answer:** requirements and constraints: workload shape, latency, scale, data, security, failure tolerance, cost and operational ownership.

### Q2. What is a sign of architecture cargo culting?
**Strong answer:** adding services because diagrams commonly include them rather than because a requirement justifies them.

### Q3. How do you know an architecture is too complex?
**Strong answer:** components cannot be tied to a requirement/risk, operational burden exceeds value, or simpler managed alternatives meet the same SLOs.

### Q4. What changes first at 10× scale?
**Strong answer:** there is no universal answer; identify the current bottleneck using throughput, storage, concurrency, downstream dependency and cost assumptions.

### Q5. What makes a design defensible?
**Strong answer:** explicit constraints, rejected alternatives, measurable SLOs, failure strategy, security boundaries and cost assumptions.

---

# H12 — Exam readiness

### Q1. Why is 80% twice more useful than one 90% simulation?
**Strong answer:** repeated performance is evidence of stable retrieval and decision quality rather than a favorable question sample.

### Q2. What should you review after a correct answer?
**Strong answer:** high-uncertainty guesses and correct answers based on weak reasoning can contain hidden gaps.

### Q3. Why should multiple-response options be evaluated independently?
**Strong answer:** one attractive option can anchor the candidate and cause them to select a package rather than test each statement against requirements.

### Q4. What is the best exam fallback when two answers remain?
**Strong answer:** return to the explicit dominant requirement and avoid adding unstated assumptions.

---

# H13 — Beyond certification

### Q1. What makes a certification project portfolio-worthy?
**Strong answer:** another engineer can understand, reproduce, test and critique it; architecture, costs, security, failures and trade-offs are visible.

### Q2. What is stronger than saying “I used SageMaker” in an interview?
**Strong answer:** explaining a concrete requirement, why SageMaker/pattern X won, what failed, how it was monitored and what you would change at larger scale.

### Q3. How do you explain the same ML system to three audiences?
**Strong answer:** preserve the same truth but change the abstraction: implementation/risk for engineers, outcomes/governance for executives, assumptions/evaluation for data scientists/economists.

### Q4. What should remain after the certification expires?
**Strong answer:** transferable systems thinking, operational judgment and a portfolio of reproducible engineering evidence.

---

# The practitioner answer rubric

Score any answer 0–5:

- **0:** no useful model.
- **1:** recognizes the term.
- **2:** gives a correct definition.
- **3:** gives a correct selection rule.
- **4:** selection rule + trade-off/rejected alternative.
- **5:** adds operational failure, cost, security or evidence implications.

## Promotion rule

A topic with many level-2 answers is **not mastered**, even if multiple-choice scores are high.

Target before the exam:

- high-frequency exam concepts: ≥4;
- critical security/deployment/monitoring decisions: ≥4;
- core personal-project concepts: 5.

---

# The elite sanity check

Before calling an architecture, lab or answer “good”, ask:

1. What requirement am I solving?
2. What assumption am I making?
3. What did I reject?
4. How can this fail silently?
5. What evidence tells me it failed?
6. What is the blast radius?
7. How do I recover?
8. What does it cost at current and 10× scale?
9. What should be automated?
10. What should remain explicitly human-controlled?

If these questions feel uncomfortable, that is exactly where the next learning gain usually is.
