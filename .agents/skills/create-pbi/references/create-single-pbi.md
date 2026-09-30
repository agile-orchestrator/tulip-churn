Create a PBI from the request in `$ARGUMENTS`. Never create issues with `gh issue create`
alone: it skips the issue template, so the type, parent link and board fields get lost.

## 1. Check the Definition of Ready

Read the **[Definition of Ready](https://github.com/agile-orchestrator/tulip-churn/wiki/Definition-of-Ready)** on the wiki. Also read
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

Do not invent content to fill a heading. Then check the draft against the **entry bar for
In refinement** in `CLAUDE.md` (imperative title, user story, at least one testable acceptance
criterion, candidate parent or "to be decided", open questions listed):

- **Meets the entry bar:** Status **In refinement**. Add `needs-refinement` too if other DoR
  items are still open (for example blocking questions, no parent, no estimate).
- **Misses the entry bar** (for example "Improve model"): do not put it in In refinement. Tell
  the user it needs more work, list exactly which entry-bar points are missing and what you
  would need from them. Offer to park it in **Backlog** with `needs-refinement`, and only do
  so if the user agrees.

## 3. Confirm

Show the title, body, labels, parent, estimate, priority and the Status it will get (with
the entry-bar result). Wait for the user's OK before creating anything.

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

Then set the project fields with `gh project item-edit`: Status, Story Points, Priority, and
Sprint if given. Always set Status: an item left at "No status" does not show up in any
board column.

Status must be one of the options configured on the project, never a name taken from
elsewhere ("New", "Triage", "To do" do not exist on this board). Look the
option up by name instead of hard-coding ids:

```bash
FIELDS=$(gh project field-list 1 --owner agile-orchestrator --format json)
PROJECT_ID=$(gh project view 1 --owner agile-orchestrator --format json --jq .id)
STATUS_FIELD=$(jq -r '.fields[] | select(.name=="Status") | .id' <<<"$FIELDS")
jq -r '.fields[] | select(.name=="Status") | .options[].name' <<<"$FIELDS"   # configured options
STATUS_OPT=$(jq -r --arg s "<In refinement|Backlog>" '.fields[] | select(.name=="Status") | .options[] | select(.name==$s) | .id' <<<"$FIELDS")
gh project item-edit --project-id $PROJECT_ID --id <item-id> --field-id $STATUS_FIELD \
  --single-select-option-id $STATUS_OPT
```

Use the Status decided in step 2: **In refinement** if the entry bar is met, **Backlog** if
not. Only set **Ready** if the user asks and every DoR item is met. If the option is missing,
stop and show the user the configured options rather than guessing.

If a `gh project` command fails (for example "Could not resolve to a ProjectV2"), do not
retry in a loop. Say what is missing and that the issue exists without board fields.

## 5. Verify and report

```bash
gh api repos/agile-orchestrator/tulip-churn/issues/$N --jq '{type:.type.name, labels:[.labels[].name]}'
gh project item-list 1 --owner agile-orchestrator --format json -L 200 \
  --jq ".items[] | select(.content.number==$N) | {status, priority, \"story Points\", sprint}"
```

If status comes back `null`, the Status edit failed: fix it before reporting.

Report the issue URL, type, labels, parent, and which board fields were or were not set.
