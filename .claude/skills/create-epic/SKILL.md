---
name: create-epic
description: Turn a business goal from the wiki into a SMART Epic as a GitHub issue with the correct type, label and board fields. Use when asked to create or write an epic, or to turn a business goal or objective into an epic for the Tulip Churn board.
argument-hint: <business goal, wiki page name or URL, or objective name>
---

Create an Epic from the business goal in `$ARGUMENTS`. The goal must be SMART, and the epic
derived from it must be SMART too. Never create issues with `gh issue create` alone: it
skips the template, so the type and board fields get lost.

## 1. Read the goal

Business goals live in the [GitHub Wiki](https://github.com/agile-orchestrator/tulip-churn/wiki) of this repo (clone
`agile-orchestrator/tulip-churn.wiki` or use `gh api`/WebFetch on the page).

- **[Project Overview](https://github.com/agile-orchestrator/tulip-churn/wiki/Project-Overview)**: Objectives, Success metrics, Stakeholders,
  Scope, Timeline.
- **[Meeting Notes](https://github.com/agile-orchestrator/tulip-churn/wiki/Meeting-Notes)**: stakeholder sessions (for example
  "Q4 Goals with the PO") where goals are agreed.
- If `$ARGUMENTS` is a URL or page name, read that page. If it is free text, find the
  matching goal in the wiki. If nothing matches, say so and ask; do not invent a goal.

Also run `gh issue list --label epic --state all` so you do not duplicate an existing epic.

## 2. Score the business goal (Gate 1)

Rate each letter **met**, **weak** or **missing**, with a one-line reason quoted from the
source:

| | Check |
|---|---|
| **S**pecific | Who or what changes, and where (segment, country, process) |
| **M**easurable | Metric, baseline and target value |
| **A**chievable | Plausible with the data and the team |
| **R**elevant | Tied to a bank objective, with a named owner or stakeholder |
| **T**ime-bound | A deadline or review date |

## 3. Derive the epic and score it (Gate 2)

The epic inherits the goal's metric, target and deadline. It must never contradict or go
beyond them. It adds delivery detail:

- **S**: the capability that gets delivered, plus in scope / out of scope
- **M**: same metric with current baseline, target, how it is measured, and one **leading
  indicator** (the goal metric may lag)
- **A**: finishable within **one quarter, or the goal's own time-bound period** if it names
  another. Check the data dictionary and the code: is the input data available **at scoring
  time**, and does the metric mean what it says (watch for target leakage)? If the scope
  will not plausibly fit the period, say so and propose trimming or splitting the epic.
- **R**: link to the goal, named stakeholders from the Project overview
- **T**: target date, not later than the goal's deadline

### Blocking rules

- **Measurable or Time-bound missing or weak: hard block.** Do not create the epic. List
  what is missing and go to step 4.
- **Specific, Achievable or Relevant weak: soft warn.** Create is allowed after the user
  confirms; show the warning in the epic body under "Risks and warnings".

## 4. Clarify

Ask only about gaps that change whether the epic is well defined. Batch them into one
round of at most 4 questions with a recommended answer each (use `AskUserQuestion`). If the
user does not know, record it as an open question. Never invent numbers, baselines, dates or
names. If a baseline is unknown, propose "establish the baseline" as the first feature
instead of making up a figure.

## 5. Confirm

Show the title, the SMART scorecard (goal and epic), the full body, labels and priority.
Wait for the user's OK before creating anything.

## 6. Create

Body headings follow `.github/ISSUE_TEMPLATE/epic.yml`: Business goal, Business outcome,
Success metric (name, baseline, target), Leading indicator, Target date, Stakeholders,
In scope / out of scope, Achievability notes, Risks and warnings, Open questions, Wiki
link. Write the body to a file in the scratchpad directory.

Title: `[Epic] ` followed by an outcome-focused name, as in the issue template.

```bash
URL=$(gh issue create --title "<title>" --label epic --body-file <file>)
N=${URL##*/}
gh api repos/agile-orchestrator/tulip-churn/issues/$N -X PATCH -f type=Epic
gh project item-add 1 --owner agile-orchestrator --url $URL --format json --jq .id
```

Set Status = **Backlog** (the In refinement entry bar in `CLAUDE.md` is for PBIs) and Priority with `gh project field-list 1 --owner
agile-orchestrator --format json` and `gh project item-edit`. Epics and features get no
Story Points. If a `gh project` command fails, do not retry in a loop: say what is missing
and that the issue exists without board fields.

## 7. Verify and report

```bash
gh api repos/agile-orchestrator/tulip-churn/issues/$N --jq '{type:.type.name, labels:[.labels[].name]}'
```

Report the issue URL, the SMART scorecard, warnings, open questions, and which board fields
were or were not set. Suggest `create-features` as the next step.
