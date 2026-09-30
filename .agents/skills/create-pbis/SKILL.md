---
name: create-pbis
description: Break a Feature into several PBIs, or turn a meeting transcript into proposed backlog items, with the correct hierarchy, labels and board fields. Use when asked to create or split PBIs, or process a meeting transcript into backlog work. For a single PBI use create-pbi.
argument-hint: <feature issue number>
---

Decompose the Feature `#$ARGUMENTS` into PBIs. Creating each PBI follows the `create-pbi`
skill (template, type, parent link, board fields); this skill adds the decomposition and a
single batched confirmation. Never create issues with `gh issue create` alone.

## Meeting-transcript mode

When `$ARGUMENTS` is a wiki page, URL, or pasted meeting transcript rather than a feature
number, read it and extract decisions, requests, and open questions. Check the board for
duplicates or existing items to update. Propose the appropriate epic, features, and PBIs,
following the hierarchy and entry-bar rules in `AGENTS.md` and the Definition of Ready.
Show the proposed hierarchy and every candidate item in a table before creating anything.

After the user confirms, create the approved issues with `create-epic`, `create-features`,
and `create-pbi` as applicable; link them as sub-issues and set each PBI to In refinement
only when it meets the entry bar, otherwise Backlog with `needs-refinement`. Report each
created issue's number, title, and status. If the transcript is a wiki page, propose updating
its “Processed to backlog” field with the created issue numbers; update and push the wiki
only after the user agrees.

## 1. Read the context

```bash
gh issue view <n> --json number,title,body,labels,state
gh api repos/agile-orchestrator/tulip-churn/issues/<n>/sub_issues --jq '.[] | {number,title,state}'
gh api repos/agile-orchestrator/tulip-churn/issues/<n>/parent --jq '{number,title}'
```

Read the **[Definition of Ready](https://github.com/agile-orchestrator/tulip-churn/wiki/Definition-of-Ready)** on the wiki, the epic the feature
belongs to (for the metric and deadline), `.github/ISSUE_TEMPLATE/pbi.yml`, and the code and
wiki [Data Dictionary](https://github.com/agile-orchestrator/tulip-churn/wiki/Data-Dictionary) where the feature touches data or the model. Existing
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
