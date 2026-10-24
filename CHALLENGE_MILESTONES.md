# MLA-C02 Challenge Milestones

> This file is not a checklist of content consumed. It is a record of **observable changes in capability**.
>
> A milestone is completed only when there is evidence that the skill can be recalled, applied, distinguished from alternatives, and retained.

## How to use this note

For every milestone, record:

- **Date started**
- **Date passed**
- **Evidence link** (lab, notebook, architecture, quiz, PR, screenshot, report)
- **Confidence before** (1–5)
- **Confidence after** (1–5)
- **Main error discovered**
- **What changed in my mental model**

If a challenge feels easy because notes or previous code are open, repeat it **closed-book**.

---

# H0 — Baseline without protection

## Challenge
Take an initial MLA-C02 diagnostic without studying immediately beforehand and without consulting notes.

## What I should start noticing
I stop saying “I know AWS reasonably well” and can instead identify precisely **what I know, what I confuse, and what I only recognize when I see it**.

## Evidence
- Baseline score by domain.
- Error ledger populated.
- Confidence recorded for every wrong answer.

## Boss fight
Explain the four MLA-C02 domains from memory and identify my two highest-risk gaps.

## Do not move on if
I am explaining poor results only as “careless mistakes” instead of classifying their actual cause.

---

# H1 — I stop memorizing AWS services and start choosing them

## Challenge
Given 20 short scenarios, choose the appropriate AWS service or ML pattern and explain why at least one plausible alternative is worse.

Examples of comparisons:

- CloudWatch vs CloudTrail
- Glue vs EMR
- SageMaker Processing vs Glue
- Real-time vs Serverless vs Async vs Batch Transform
- Bedrock RAG vs fine-tuning
- Secrets Manager vs KMS

## What I should start noticing
AWS questions become less like vocabulary tests and more like **constraint-matching problems**.

I begin noticing trigger words such as:

- least operational overhead
- sporadic traffic
- low latency
- near-real-time
- fully managed
- least privilege
- cost-effective

## Evidence
A `decision_cards/` set where every card contains:

`NEED → CONSTRAINT → OPTIONS → DECISION → WHY NOT THE OTHERS`

## Boss fight
80%+ on a service-discrimination quiz without notes.

## Do not move on if
I can define a service but cannot say when **not** to use it.

---

# H2 — Data stops being “the easy part”

## Challenge
Design and implement a small ML data path using synthetic data:

`raw data → S3 → preparation → feature-ready dataset`

Then justify format, partitioning, data quality checks, and batch/streaming decisions.

## What I should start noticing
My existing SQL/data experience transfers well, but AWS introduces operational choices I previously ignored: storage format, partition strategy, permissions, scale and cost.

## Evidence
- Architecture diagram.
- Reproducible lab.
- Data quality checks.
- Short written trade-off note.

## Boss fight
Receive a changed requirement — for example “now ingestion must be near-real-time” — and redesign the pipeline without copying a tutorial.

## Do not move on if
The pipeline works but I cannot explain why its architecture is preferable to two alternatives.

---

# H3 — I can train a model in AWS without treating SageMaker as magic

## Challenge
Build a complete small training workflow in SageMaker using a familiar business problem such as synthetic lead scoring.

Cover:

- processing
- training
- evaluation
- hyperparameter tuning
- experiment tracking
- model artifact
- Model Registry

## What I should start noticing
I begin separating **ML concepts I already know** from the AWS mechanisms that operationalize them.

## Evidence
A reproducible project under `projects/p01-lead-scoring/`.

## Boss fight
Explain the entire training lifecycle on a blank page, including which SageMaker component owns each stage.

## Do not move on if
I need the AWS console open to remember the workflow.

---

# H4 — Deployment becomes a decision, not a button

## Challenge
Solve deployment scenarios involving:

- real-time endpoints
- serverless inference
- asynchronous inference
- batch transform
- CPU vs GPU
- autoscaling
- cost vs latency

## What I should start noticing
I automatically ask:

1. What latency is required?
2. What traffic pattern exists?
3. How large is the payload?
4. Does the caller wait for the result?
5. What happens when there is no traffic?
6. What cost is acceptable?

## Evidence
A deployment decision matrix plus at least one deployed inference example.

## Boss fight
Given five workloads, choose the deployment mode in under 10 minutes and defend every choice.

## Do not move on if
I am selecting the most powerful architecture rather than the **simplest architecture satisfying the requirement**.

---

# H5 — My first real MLOps loop

## Challenge
Create the lifecycle:

`data → train → evaluate → condition → register → approve → deploy`

Then introduce versioning and a repeatable trigger.

## What I should start noticing
The model itself starts feeling like only one component of a much larger engineering system.

## Evidence
- SageMaker Pipeline or equivalent reproducible workflow.
- Model Registry usage.
- Versioned model evidence.
- Clear human approval point where appropriate.

## Boss fight
Change the dataset and reproduce a new model version without manually repeating every step.

## Do not move on if
“Automation” still means a notebook with many cells that I execute manually.

---

# H6 — Break it, diagnose it, recover it

## Challenge
Intentionally create failures such as:

- wrong IAM permission
- inaccessible S3 object
- incorrect model artifact
- broken endpoint configuration
- missing secret
- incorrect KMS permission
- malformed input

Diagnose each failure from logs and evidence before fixing it.

## What I should start noticing
AWS error messages become clues instead of noise. I start knowing **where to look first**.

## Evidence
A `failure_lab/` containing:

`failure → symptom → evidence → root cause → fix → prevention`

## Boss fight
Troubleshoot an intentionally broken lab without being told which component is wrong.

## Do not move on if
My debugging method is still “change things until it works.”

---

# H7 — Monitoring changes from dashboarding to operating a model

## Challenge
Instrument a deployed model and distinguish:

- infrastructure metrics
- application logs
- model quality
- data drift
- model degradation
- API auditing

## What I should start noticing
I stop thinking that successful deployment means the system is finished.

The question becomes:

> “How will I know this model should no longer be trusted?”

## Evidence
Monitoring architecture plus concrete alarms or evaluation rules.

## Boss fight
Receive a degradation scenario and determine whether the problem is data, model, infrastructure, permissions, or application behavior.

## Do not move on if
I am using CloudWatch, CloudTrail and Model Monitor as interchangeable concepts.

---

# H8 — Security becomes part of the architecture

## Challenge
Review an ML architecture and reduce its permissions and exposure using:

- IAM roles and policies
- least privilege
- KMS
- Secrets Manager
- VPC/network controls
- CloudTrail
- relevant security services

## What I should start noticing
I begin noticing security requirements **before** reaching the final answer of a scenario.

## Evidence
A before/after security review of one project.

## Boss fight
Find at least five security weaknesses in an intentionally unsafe ML architecture.

## Do not move on if
My security reasoning is only “make it private” or “encrypt it.”

---

# H9 — Bedrock: I know when GenAI is actually appropriate

## Challenge
Build a small RAG system and compare it against:

- prompt-only generation
- fine-tuning/model customization
- traditional ML

Cover:

- embeddings
- chunking
- retrieval
- vector store
- knowledge base
- evaluation
- guardrails

## What I should start noticing
I stop treating GenAI as the default solution. I ask whether the real problem is generation, fresh knowledge, prediction, retrieval, or deterministic business logic.

## Evidence
A project under `projects/p02-bedrock-rag/` plus a decision document describing when RAG should *not* be used.

## Boss fight
Given four business problems, decide which needs RAG, fine-tuning, traditional ML, or no ML at all.

## Do not move on if
Every text-related problem is becoming a Bedrock problem.

---

# H10 — Agentic AI without losing engineering discipline

## Challenge
Design an agent that can use tools but has explicit controls for:

- permissions
- tool failures
- observability
- state
- versioning
- cost
- human approval

## What I should start noticing
An agent stops looking like “an intelligent chatbot” and starts looking like a **distributed software system with probabilistic reasoning inside it**.

## Evidence
Agent architecture + failure modes + at least one controlled tool workflow.

## Boss fight
Explain what happens when the agent chooses the wrong tool, receives a bad tool response, or is not authorized to execute the requested action.

## Do not move on if
The only evaluation criterion is “the answer looked good.”

---

# H11 — Blank-page architecture

## Challenge
Without notes, design an AWS ML solution for a new problem containing:

- ingestion
- storage
- preparation
- training/FM choice
- evaluation
- deployment
- monitoring
- security
- cost considerations

## What I should start noticing
I can navigate a new problem from first principles instead of searching for a tutorial that resembles it.

## Evidence
Three architecture exercises completed on different days.

## Boss fight
30-minute architecture challenge followed by a 10-minute verbal defense of trade-offs.

## Do not move on if
I am adding services because “AWS architectures usually have them.”

---

# H12 — Exam-ready is demonstrated, not felt

## Challenge
Meet all certification gates:

- two full simulations ≥80%
- no domain <70%
- critical gaps = 0
- high-confidence wrong answers <3%
- 7-day retention ≥80%

## What I should start noticing
Questions that previously looked ambiguous now have a dominant requirement I can isolate quickly.

I also become faster at eliminating distractors.

## Evidence
Simulation history and closed Error Ledger.

## Boss fight
Final full simulation under exam conditions.

## Do not move on if
I want to book the exam mainly because I am tired of studying.

---

# H13 — Certification is no longer the ceiling

Passing MLA-C02 unlocks the final milestone rather than ending the repository.

## Challenge
Turn the best labs into a coherent portfolio project that another engineer can clone, understand and evaluate.

## What I should start noticing
I can discuss AWS ML in interviews through systems I actually built, not certification vocabulary.

## Evidence
- polished README
- architecture diagrams
- reproducible deployment instructions
- tests
- cost notes
- security notes
- failure/recovery examples
- lessons learned

## Boss fight
Explain the project to three audiences:

1. ML engineer
2. business executive
3. economist/data scientist

without using the same explanation for all three.

---

# Progress note template

Copy this section whenever a milestone is passed:

```md
## Milestone H__ passed — YYYY-MM-DD

### Challenge completed
...

### Evidence
...

### What I can do now that I could not do before
...

### Most important mistake discovered
...

### Mental model that changed
Before: ...
After: ...

### Remaining weakness
...

### Next challenge
...
```

---

# The rule of this repository

> **Progress is not the number of AWS services I have touched. Progress is the number of engineering decisions I can make correctly, explain clearly, reproduce, and defend without assistance.**
