---
name: create-pbi
description: Create a Product Backlog Item (PBI) as a GitHub issue with the correct type, labels, parent sub-issue link and board fields. Use when asked to create, add or write a PBI, backlog item or task for the Tulip Churn board.
argument-hint: <short description of the work>
---

Create a PBI from the request in `$ARGUMENTS`. Never create issues with `gh issue create`
alone: it skips the issue template, so the type, parent link and board fields get lost.

## 1. Check the Definition of Ready

Read the **Definition of Ready** (Notion page under "Tulip Bank — Churn Early-Warning", or
the GitHub Wiki once migrated). Do not use the "(backup)" copy. Also read
`.github/ISSUE_TEMPLATE/pbi.yml` for the body headings.

## 2. Draft the body

Write it to a file in the scratchpad directory, with these headings:

- **Parent feature** (`#n`; pick from `gh issue list --label feature --state open`)
- **User story**: As a / I want / So that
- **Scope** (in and out of scope), when the boundary is not obvious
- **Acceptance criteria**: testable Given/When/Then checklist items
- **Technical notes**
- **Dependencies and open questions**: mark each blocking or non-blocking
- **Estimate**: 1, 2, 3, 5 or 8. Above 8 means split into several PBIs.
- **Priority**: P0-P3

Title: short imperative ("Make decision threshold configurable"), no "[PBI]" prefix.
For model or data changes also name the metric to improve (with its current value), confirm
the data exists at scoring time, and note compliance impact.

If the request is vague ("Improve model") or a DoR item cannot be filled in, do not invent
content: add the `needs-refinement` label and keep the item in Backlog.

## 3. Confirm

Show the title, body, labels, parent, estimate and priority. Wait for the user's OK before
creating anything.

## 4. Create

```bash
URL=$(gh issue create --title "<title>" --label pbi --label <area> --body-file <file>)
N=${URL##*/}
# issue type (gh issue create does not set it)
gh api repos/agile-orchestrator/tulip-churn/issues/$N -X PATCH -f type=Task
# parent
gh api repos/agile-orchestrator/tulip-churn/issues/<parent>/sub_issues -X POST \
  -F sub_issue_id=$(gh api repos/agile-orchestrator/tulip-churn/issues/$N --jq .id)
# board
gh project item-add 1 --owner agile-orchestrator --url $URL --format json --jq .id
```

Labels: always `pbi`; add an area label if one fits (`api`, `model`, `docs`, `ci`), and
`sprint-N` only if the user names a sprint (or `needs-refinement`, see above).

Then set the project fields with `gh project field-list 1 --owner agile-orchestrator
--format json` (ids) and `gh project item-edit`: Status = **Backlog**, Story Points,
Priority, and Sprint if given. Only set Status to **Ready** if the user asks and every DoR
item is met.

If a `gh project` command fails (for example "Could not resolve to a ProjectV2"), do not
retry in a loop. Say what is missing and that the issue exists without board fields.

## 5. Verify and report

```bash
gh api repos/agile-orchestrator/tulip-churn/issues/$N --jq '{type:.type.name, labels:[.labels[].name]}'
```

Report the issue URL, type, labels, parent, and which board fields were or were not set.
