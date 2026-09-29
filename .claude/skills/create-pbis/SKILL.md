---
name: create-pbis
description: Break a Feature into several PBIs as GitHub issues, linked as sub-issues of the feature with the correct type, labels and board fields, each checked against the Definition of Ready. Use when asked to create, split or refine the PBIs of a feature on the Tulip Churn board. For a single PBI use create-pbi.
argument-hint: <feature issue number>
---

Decompose the Feature `#$ARGUMENTS` into PBIs. Creating each PBI follows the `create-pbi`
skill (template, type, parent link, board fields); this skill adds the decomposition and a
single batched confirmation. Never create issues with `gh issue create` alone.

## 1. Read the context

```bash
gh issue view <n> --json number,title,body,labels,state
gh api repos/agile-orchestrator/tulip-churn/issues/<n>/sub_issues --jq '.[] | {number,title,state}'
gh api repos/agile-orchestrator/tulip-churn/issues/<n>/parent --jq '{number,title}'
```

Read the **Definition of Ready** in Notion (not the "(backup)" copy), the epic the feature
belongs to (for the metric and deadline), `.github/ISSUE_TEMPLATE/pbi.yml`, and the code and
Notion **Data dictionary** where the feature touches data or the model. Existing
sub-issues are already covered: do not propose duplicates, and offer to refine them with
`refine-pbi` instead.

If the feature is not linked to an epic, or its own acceptance criteria are empty, say so
and ask before continuing.

## 2. Clarify

Ask only about gaps that would change the split or make a PBI untestable, in one batch of at
most 4 questions with a recommended answer each (`AskUserQuestion`). Typical gaps: an
acceptance criterion that cannot be tested, a dependency, the metric a model change should
improve, whether data exists at scoring time. If the user does not know, record it as an
open question marked **blocking** or **non-blocking**. Never invent content.

## 3. Propose the split

- Slice **vertically**: each PBI delivers something testable end to end (for example "Score
  endpoint returns a risk band"), not one layer ("write the model", "write the tests").
- Each PBI fits in one sprint and is estimated 1, 2, 3, 5 or 8. Above 8: split further.
- The PBIs together must cover the feature's acceptance criteria. Show the mapping and any
  criterion left uncovered.
- At most 10 PBIs per run. If more are needed, the feature is too big: propose splitting the
  feature (`create-features`).
- Order by dependency; mark which PBIs can run in parallel.
- Model or data PBIs: name the metric with its current value, confirm the data exists at
  scoring time (no information from the future or the target), note compliance impact.
- Every PBI: title in short imperative form (no "[PBI]" prefix), user story (As a / I want
  / So that), Given/When/Then acceptance criteria, technical notes, dependencies and open
  questions, estimate, priority P0-P3.

Check each proposed PBI against the **entry bar for In refinement** in `CLAUDE.md` and the
full DoR checklist, as `create-pbi` step 2 does. Do not invent content to pass either.

- **Meets the entry bar:** Status **In refinement**. Add `needs-refinement` too if other DoR
  items are still open (blocking question, unknown metric, no estimate).
- **Misses the entry bar** (vague items like "Improve model"): do not put it in In
  refinement. List which entry-bar points are missing and what you need. Offer to park it in
  **Backlog** with `needs-refinement`, and only do so if the user agrees.

Show one table: title, estimate, priority, dependencies, entry-bar and DoR result (which
Status it gets, and which criteria are missing), and the acceptance criteria it covers. Then show the full bodies.
Wait for the user to approve, edit or drop items, once for the whole batch.

## 4. Create

For each approved PBI, in dependency order, follow `create-pbi` step 4: write the body to a
file in the scratchpad directory, create the issue, set type = Task, link it as a
sub-issue of the feature, add it to project 1, and set Status (**In refinement**, or
**Backlog** for parked items; look the option up by name as `create-pbi` does), Story
Points, Priority (and Sprint only if the user names one). Labels: always `pbi`; an area label if
one fits (`api`, `model`, `data`, `docs`, `ci`); `needs-refinement` where applicable. Only
set Status **Ready** if the user asks and every DoR item is met.

Record each created number and mention dependencies between PBIs by issue number in the
bodies. If one create fails, stop, report what exists, and do not retry in a loop. If a
`gh project` command fails, say what is missing and that the issues exist without board
fields.

## 5. Verify and report

For each issue check type, labels, parent and board fields as `create-pbi` step 5 does. A
Status of `null` means the edit failed: fix it before reporting. Report the URLs in a table with estimate,
priority, DoR result and board fields set, the total points, and any open questions and
`needs-refinement` items.
