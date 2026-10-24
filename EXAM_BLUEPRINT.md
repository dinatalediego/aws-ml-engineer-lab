# MLA-C02 Exam Blueprint — Working Map

> Scope anchor: AWS Certified Machine Learning Engineer – Associate (MLA-C02).
> This file is a study map, not a replacement for the official AWS exam guide.

## Current official structure

AWS defines four scored domains:

| Domain | Weight |
|---|---:|
| D1 — Data Preparation for ML and AI | 28% |
| D2 — ML Model and Foundation Model Development | 24% |
| D3 — Deployment and Orchestration of ML and AI Workflows | 24% |
| D4 — Operating, Monitoring, and Securing ML and AI Solutions | 24% |

The exam validates traditional ML **and** foundation-model/GenAI engineering, including Bedrock, agentic workflows, CI/CD, observability and security.

## Beta context — 2026

The AWS Certification page currently lists the MLA-C02 beta as:

- English only;
- 170 minutes;
- 85 questions;
- USD 75 beta price;
- intended for candidates with SageMaker AI, Bedrock and related ML-engineering experience.

The generic exam guide separately documents standard scoring mechanics and 720 as the scaled passing standard. Treat the current Certification page as the authority for beta delivery specifics and the exam guide as the authority for domains/tasks.

---

# D1 — Data Preparation for ML and AI — 28%

## What to be able to decide

- batch vs streaming ingestion;
- S3 layout, formats and partitioning;
- transformation approach and operational overhead;
- data quality and validation strategy;
- feature preparation and reuse;
- access and encryption boundaries;
- preparation for traditional ML vs GenAI/RAG workloads;
- vector/embedding preparation where relevant.

## High-signal AWS concepts/services

S3, Glue, Athena, Redshift, EMR/Spark, Kinesis, SageMaker Processing/Data Wrangler/Feature Store, data quality patterns, encryption/IAM, vector-oriented storage and retrieval concepts.

## Practitioner FAQ prompts

1. Why is Parquet usually preferable to CSV for analytical ML pipelines?
2. When does Glue become a better choice than SageMaker Processing?
3. What requirement makes streaming necessary rather than fashionable?
4. How do partition choices affect cost and latency?
5. What is the difference between validating schema and validating data quality?
6. What leakage can be introduced during feature preparation?
7. What belongs in an online feature store vs offline storage?
8. When should embeddings be regenerated?
9. What breaks if feature definitions differ between training and inference?
10. How would you detect stale or silently incomplete input data?

## Common traps

- choosing streaming without a latency requirement;
- using a heavier service when managed ETL is enough;
- ignoring train/serve skew;
- forgetting permissions/KMS when a pipeline design otherwise looks correct;
- assuming “data engineering is easy” and underpreparing the highest-weight domain.

---

# D2 — ML Model and Foundation Model Development — 24%

## What to be able to decide

- traditional ML vs FM/GenAI vs deterministic logic;
- algorithm/model family from business and data constraints;
- metrics appropriate to the problem;
- tuning/evaluation strategy;
- model selection and versioning;
- RAG vs prompt engineering vs model customization/fine-tuning;
- FM selection by quality, latency, cost and capability;
- responsible-AI controls and evaluation.

## High-signal AWS concepts/services

SageMaker AI training, Processing, Automatic Model Tuning, Experiments/MLflow concepts, Model Registry, Bedrock foundation models, Knowledge Bases/RAG concepts, embeddings, evaluation, Guardrails, model customization and prompt management concepts.

## Practitioner FAQ prompts

1. Why can accuracy be a bad metric even when classes are not extremely imbalanced?
2. When is threshold tuning more valuable than retraining?
3. What evidence says a model is overfitting rather than simply noisy?
4. When should you choose RAG instead of fine-tuning?
5. What problem does fine-tuning solve that RAG does not?
6. Why can a stronger FM be the worse production choice?
7. What changes when evaluation becomes nondeterministic?
8. How do you compare an FM upgrade safely?
9. When is traditional ML superior to an LLM?
10. How do you evaluate retrieval separately from generation?

## Common traps

- assuming bigger model = better solution;
- choosing GenAI for prediction/classification where conventional ML is cheaper and more controllable;
- confusing RAG with model training;
- optimizing one metric while ignoring business cost;
- forgetting versioning and reproducibility.

---

# D3 — Deployment and Orchestration of ML and AI Workflows — 24%

## What to be able to decide

- real-time vs serverless vs asynchronous vs batch inference;
- CPU vs accelerator based on workload;
- autoscaling and capacity strategy;
- container/artifact deployment path;
- pipeline orchestration and repeatability;
- CI/CD and infrastructure-as-code responsibilities;
- retraining triggers and approval gates;
- agent/workflow orchestration where relevant.

## High-signal AWS concepts/services

SageMaker endpoints and inference modes, SageMaker Pipelines, Model Registry, ECR, CodeBuild/CodePipeline/CodeDeploy concepts, EventBridge, Step Functions, Lambda, IaC concepts, containerization, deployment strategies and agent orchestration.

## Practitioner FAQ prompts

1. What exact requirement separates async inference from batch transform?
2. Why can serverless inference be wrong for a low-latency SLO?
3. What is the minimum automation that actually counts as MLOps?
4. What should trigger retraining: time, data, performance or business events?
5. Where should human approval sit in a production ML pipeline?
6. What do you version besides the model artifact?
7. How do you roll back safely when model behavior degrades?
8. When is a multi-model endpoint useful, and what complexity does it introduce?
9. What is the difference between CI for code and CD for models?
10. What belongs in IaC vs runtime configuration?

## Common traps

- deploying the most powerful endpoint instead of the simplest sufficient one;
- confusing scheduled automation with reproducible orchestration;
- no model/data/config version linkage;
- no rollback path;
- treating notebook execution as production automation.

---

# D4 — Operating, Monitoring, and Securing ML and AI Solutions — 24%

## What to be able to decide

- metrics/logs/traces/audit evidence;
- CloudWatch vs CloudTrail vs model-specific monitoring;
- data drift vs concept/model degradation vs infrastructure failure;
- least-privilege IAM and service roles;
- KMS vs Secrets Manager responsibilities;
- VPC/network isolation needs;
- alerts, thresholds and operational response;
- GenAI/agent observability, guardrails and tool-permission boundaries;
- cost/usage monitoring.

## High-signal AWS concepts/services

CloudWatch, CloudTrail, SageMaker Model Monitor/evaluation patterns, IAM, KMS, Secrets Manager, VPC controls, AWS Config/security concepts, Bedrock Guardrails, logging, alarms and cost awareness.

## Practitioner FAQ prompts

1. What can CloudTrail prove that CloudWatch cannot?
2. What does Model Monitor detect that an endpoint health alarm does not?
3. How do you distinguish data drift from concept drift operationally?
4. Why is encryption not equivalent to access control?
5. When do you need a customer-managed KMS key?
6. Why should an agent have narrower permissions than its host application might have?
7. What is a silent model failure?
8. Which metrics should page a human versus create a review task?
9. How do you monitor token/call cost as an engineering signal?
10. What evidence would justify disabling a model or agent automatically?

## Common traps

- CloudWatch/CloudTrail/Model Monitor treated as synonyms;
- broad IAM permissions to “make it work”;
- storing secrets in code/config;
- alerting without an operational action;
- monitoring infrastructure but not model behavior;
- evaluating GenAI only by whether responses look plausible.

---

# Cross-domain discriminations to master

These are disproportionately valuable because exam distractors often contain several technically valid services.

- Glue vs SageMaker Processing
- Athena vs Redshift
- Kinesis vs batch ingestion
- Feature Store online vs offline
- traditional ML vs RAG vs fine-tuning vs deterministic rules
- real-time vs serverless vs async vs batch inference
- SageMaker Pipelines vs Step Functions vs generic CI/CD tooling
- CloudWatch vs CloudTrail vs Model Monitor
- KMS vs Secrets Manager
- IAM identity policies vs resource policies
- prompt engineering vs RAG vs model customization
- Guardrails vs IAM/tool authorization

---

# Exam-reading algorithm

For each scenario:

1. Identify the **dominant requirement**.
2. Mark hard constraints: latency, scale, cost, availability, security, freshness, operational overhead.
3. Eliminate answers that violate a hard constraint.
4. Prefer the simplest managed option satisfying all stated requirements.
5. Ask what each remaining option optimizes.
6. For multiple-response questions, judge every option independently.
7. If unsure, choose based on explicit requirements rather than imagined ones.

---

# Source-of-truth links

- Exam guide: https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02.html
- Certification page: https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/

Review these periodically because MLA-C02 is currently in its 2026 beta transition period.
