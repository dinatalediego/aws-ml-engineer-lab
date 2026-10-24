# AWS ML Engineer Lab

A deliberate-practice repository for becoming an AWS Machine Learning Engineer and passing **AWS Certified Machine Learning Engineer – Associate (MLA-C02)** without reducing the goal to exam memorization.

## North Star

> Build the ability to make, explain, reproduce, defend, monitor, secure and troubleshoot ML/AI engineering decisions on AWS.

Passing the certification is a milestone. The real output is practitioner-level capability.

## Operating model

This repository uses a mastery loop:

`DIAGNOSE → LEARN → RECALL → APPLY → DISCRIMINATE → BREAK → RECOVER → RETAIN → SIMULATE → PROMOTE`

A topic is never considered complete because a video was watched or a lab ran once.

## Command Center v0.1

The repository includes a local Streamlit control plane that reads the evidence files and calculates:

- Certification Readiness;
- readiness by exam domain;
- Critical Gaps;
- Retention Due;
- High-Confidence Errors;
- Next Best Study Action;
- H0 gate status;
- practitioner baseline by category.

The dashboard is deliberately fail-closed: **before H0 contains real evidence, it refuses to present a meaningful readiness estimate or optimize the study plan.**

### Windows quick start

```powershell
.\scripts\run_command_center.bat
```

The first run creates `.venv`, installs `requirements.txt`, and launches the local application.

See `app/README.md` for formulas and operating details.

## H0 first

Do not begin broad AWS study until the initial baseline is captured.

Use:

- `DIAGNOSTIC_H0.md` — diagnostic design;
- `h0/H0_RUNBOOK.md` — exact execution sequence;
- `h0/H0_RESULTS.csv` — official quantitative baseline;
- `h0/H0_PRACTITIONER_RESPONSES.csv` — closed-book practitioner questions;
- `h0/H0_GAPS.csv` — five ranked weaknesses;
- `h0/H0_7_DAY_PLAN.csv` — first remediation sprint.

The Command Center can edit these locally and recompute the gate.

## Core files

- `MASTER_PLAN.md` — global methodology, cadence and promotion rules.
- `EXAM_BLUEPRINT.md` — current MLA-C02 domains, weights, traps and study priorities.
- `CHALLENGE_MILESTONES.md` — observable capability milestones H0–H13.
- `SKILL_MATRIX.csv` — evidence-based mastery tracker.
- `ERROR_LEDGER.csv` — every meaningful error becomes a learning asset.
- `DIAGNOSTIC_H0.md` — baseline diagnostic protocol.
- `FAQ_ELITE_PRACTITIONERS.md` — high-signal practitioner questions and expected reasoning.
- `PRACTITIONER_GATES.md` — promotion criteria beyond exam recognition.
- `PROGRESS.md` — current readiness, gaps and next best actions.
- `app/` — Command Center and decision engine.
- `tests/` — executable validation of the scoring logic.

## Mastery states

`UNSEEN → EXPOSED → UNDERSTOOD → RECALLED → APPLIED → DISCRIMINATED → RETAINED → EXAM_READY`

## Mastery model

A skill is scored as:

```text
Mastery = 20% Recall
        + 30% Application
        + 30% Discrimination
        + 20% Retention
```

The weighting is deliberate: being able to **apply and choose** matters more than merely recognizing terminology.

## Non-negotiable gates

A skill can only be promoted when there is evidence of:

1. **Recall** — explain it without notes.
2. **Application** — use it in a lab or design.
3. **Discrimination** — distinguish it from plausible alternatives.
4. **Failure handling** — diagnose at least one failure mode where relevant.
5. **Retention** — recover the knowledge later, not just immediately.
6. **Exam transfer** — solve scenario questions under time pressure.

## Current exam target

MLA-C02 validates building, operationalizing, deploying and maintaining traditional ML and foundation-model workloads on AWS. The four exam domains are:

- Data Preparation for ML and AI — 28%
- ML Model and Foundation Model Development — 24%
- Deployment and Orchestration of ML and AI Workflows — 24%
- Operating, Monitoring, and Securing ML and AI Solutions — 24%

Source of truth: AWS exam guide and AWS Certification pages. Third-party material is supplementary only.

## Practitioner rule

> If I know **what** a service does but cannot explain **when not to use it**, I do not know it well enough yet.

## Anti-patterns this repo rejects

- collecting AWS services without understanding trade-offs;
- calling tutorial reproduction “hands-on mastery”;
- confusing a working deployment with a production-ready system;
- treating GenAI as the default answer;
- treating security as a final checklist;
- closing mistakes without recording their root cause;
- booking the exam because studying feels tiring;
- building infrastructure that does not increase exam readiness or engineering skill;
- marking a diagnostic gate complete without evidence.

## Definition of ready

Certification readiness requires all of the following:

- two full simulations at or above 80%;
- no domain below 70%;
- zero unresolved critical knowledge gaps;
- high-confidence wrong answers below 3%;
- 7-day retention at or above 80%;
- ability to defend representative architectures without notes.

The Command Center readiness percentage is a **training metric**, not a conversion to the official AWS scaled score.

## Engineering quality gate

Every change to the application is validated through GitHub Actions:

```text
install dependencies
→ compile app
→ run pytest
```

Study evidence can be messy. The system that measures it should not be.

## Repository philosophy

This repo should become a portfolio artifact that demonstrates the difference between knowing AWS vocabulary and thinking like an ML engineer.
