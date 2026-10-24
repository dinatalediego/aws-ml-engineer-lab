# MLA-C02 Command Center v0.1

The Command Center turns repository evidence into study decisions. It is intentionally conservative: if H0 is incomplete, it refuses to present a meaningful readiness score.

## Run on Windows

From the repository root, either double-click:

```text
scripts\run_command_center.bat
```

or run:

```powershell
.\scripts\run_command_center.bat
```

On first launch it creates `.venv`, installs dependencies, and starts Streamlit.

Manual alternative:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app\command_center.py
```

## Inputs

- `SKILL_MATRIX.csv`
- `ERROR_LEDGER.csv`
- `h0/H0_RESULTS.csv`
- `h0/H0_PRACTITIONER_RESPONSES.csv`

The Data Editor writes only to the local checkout. Review `git diff` before committing evidence.

## Mastery formula

For each skill:

```text
Mastery = 0.20 Recall
        + 0.30 Application
        + 0.30 Discrimination
        + 0.20 Retention
```

This intentionally weights doing and choosing more heavily than recognition.

## Certification Readiness

Domain readiness is the mean mastery of skills in that domain.

```text
Certification Readiness =
  D1 * 0.28 + D2 * 0.24 + D3 * 0.24 + D4 * 0.24
```

This is a training indicator, **not an AWS exam-score conversion**.

## Critical Gap

A skill is considered critical when either:

- mastery is below 60%; or
- it contains an unresolved high-confidence misconception.

## High-Confidence Error

An open error with `confidence_1_5 >= 4`.

These errors receive extra priority because they represent an incorrect mental model rather than simple uncertainty.

## Retention Due

A skill appears in Retention Due when:

- `next_review <= today`; and
- its state is not `UNSEEN`.

## Next Best Study Action

Before H0 is passed, the next action is always **complete H0**.

After H0, the engine ranks skills using:

- mastery gap;
- MLA-C02 domain importance;
- unresolved error frequency;
- high-confidence errors;
- overdue retention.

The exact function lives in `app/core.py` and is tested in `tests/test_core.py`.

## Design constraints

The app must never:

- infer knowledge from content consumed;
- convert blank scores to optimistic estimates;
- treat a dashboard as evidence;
- overwrite evidence silently;
- mark H0 passed without real diagnostic inputs.

## v0.1 scope

Included:

- readiness;
- domain readiness;
- critical gaps;
- retention due;
- high-confidence errors;
- next best study action;
- H0 data entry;
- skill/error local editors.

Deferred until evidence exists:

- automatic spaced-repetition scheduling;
- simulation history;
- question-bank generation;
- cost tracking for AWS labs;
- GitHub issue generation from critical gaps;
- portfolio evidence scoring.
