---
name: create-features
description: Break a SMART Epic into Features as GitHub issues, linked as sub-issues of the epic with the correct type, labels and board fields. Use when asked to create or split features for an epic, or to decompose a business goal into features on the Tulip Churn board.
argument-hint: <epic issue number, or a business goal to turn into an epic first>
---

Decompose the epic in `$ARGUMENTS` into Features. Never create issues with `gh issue
create` alone: it skips the template, so the type, parent link and board fields get lost.

## 1. Read the epic

```bash
gh issue view <n> --json number,title,body,labels,state
gh api repos/agile-orchestrator/tulip-churn/issues/<n>/sub_issues --jq '.[] | {number,title,state}'
```

If `$ARGUMENTS` is free text or a goal, run the `create-epic` skill first and continue with
the epic it creates. Also read the Notion **Project overview** and the **Data dictionary**
(not the "(backup)" copies), and list existing features with `gh issue list --label feature
--state all`. Do not propose a feature that already exists.

## 2. SMART gate on the epic

Re-check the epic against Specific, Measurable, Achievable, Relevant and Time-bound.

- **Measurable or Time-bound missing: hard block.** Do not create features. Say what is
  missing and offer to fix the epic first (edit it after the user confirms).
- **S, A or R weak: soft warn.** Continue, and carry the warning into the proposal.

## 3. Clarify

Ask only about gaps that would change the breakdown, in one batch of at most 4 questions
with a recommended answer each (`AskUserQuestion`). If the user does not know, record an
open question marked blocking or non-blocking. Never invent content.

## 4. Propose the breakdown

A Feature is an outcome-sized capability a stakeholder can see, deliverable in roughly
1 to 3 sprints. Rules:

- Slice vertically (value a user or the Retention team can use), not by layer ("model",
  "API", "tests" as separate features is wrong).
- Together the features must cover the epic's scope and success metric, and must fit within
  the epic's period (one quarter unless the epic says otherwise). If they do not, say which
  scope to cut or defer.
- At most 6 features per run. If more are needed, the epic is too big: propose splitting it.
- Include a feature to establish the baseline when the epic has none.
- Model or data features: name the metric, confirm the data exists at scoring time, note
  compliance impact.

Show a table: title, one-line outcome, which SMART metric it moves, rough size in sprints,
dependencies, open questions. Wait for the user to approve, edit or drop rows.

## 5. Create

Body headings follow `.github/ISSUE_TEMPLATE/feature.yml`: Parent epic, Description
(benefit hypothesis), Acceptance criteria (high level), plus Dependencies and open
questions. Write each body to a file in the scratchpad directory. Titles are `[Feature] ` followed by a short,
outcome-focused name, as in the issue template.

For each approved feature:

```bash
URL=$(gh issue create --title "<title>" --label feature --label <area> --body-file <file>)
N=${URL##*/}
gh api repos/agile-orchestrator/tulip-churn/issues/$N -X PATCH -f type=Feature
gh api repos/agile-orchestrator/tulip-churn/issues/<epic>/sub_issues -X POST \
  -F sub_issue_id=$(gh api repos/agile-orchestrator/tulip-churn/issues/$N --jq .id)
gh project item-add 1 --owner agile-orchestrator --url $URL --format json --jq .id
```

Labels: always `feature`; add an area label if one fits (`api`, `model`, `data`, `docs`,
`ci`). Set Status = **Backlog** (the In refinement entry bar in `CLAUDE.md` is for PBIs) and Priority via `gh project field-list` and `gh project
item-edit`. No Story Points on features. If a `gh project` command fails, do not retry in
a loop: say what is missing and that the issue exists without board fields.

## 6. Verify and report

Check each issue's type, labels and parent (`gh api .../issues/<n>/parent`). Report the
URLs, the table with issue numbers, warnings and open questions, and which board fields
were or were not set. Suggest `create-pbis` for each feature as the next step.
