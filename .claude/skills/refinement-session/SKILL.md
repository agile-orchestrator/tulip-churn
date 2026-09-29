---
name: refinement-session
description: Run a backlog refinement session on the Tulip Churn board - list the items In refinement, check them one by one against the Definition of Ready, apply the agreed changes and move them to Ready. Use when asked to run, start or continue a refinement session, or to refine the items in refinement.
argument-hint: "[issue number to start with]"
---

Walk the team through the items in **In refinement**, one at a time. The user (usually the
Product Owner) decides; you check, propose and apply. Never edit, create or move an issue
without the user's OK for that change.

## 1. List the items

```bash
gh project item-list 1 --owner agile-orchestrator --format json -L 200 | jq -r '
  .items[] | select(.status=="In refinement")
  | "#\(.content.number)\t\(.labels // [] | join(","))\t\(.priority // "-")\t\(.["story Points"] // "-")\t\(.title)\t\(.content.url)"'
```

Show them as a table (number, title, labels, priority, points, URL). Point out items with
empty board fields. Start with `$ARGUMENTS` if given, otherwise ask which one to take first.

## 2. Gather everything for one item

- The issue body, parent and comments:
  `gh issue view <n> -R agile-orchestrator/tulip-churn --json title,body,labels,parent`
  and `gh issue view <n> -R agile-orchestrator/tulip-churn --comments`
- Its board fields (Status, Priority, Story Points, Sprint) from `gh project item-list`
- The parent feature and its epic, to judge whether the parent fits
- The **[Definition of Ready](https://github.com/agile-orchestrator/tulip-churn/wiki/Definition-of-Ready)** on the wiki.

## 3. Check it

Report in a table, one row per DoR criterion, with ✅ / ⚠️ / ❌ and a short note. First say
whether the **entry bar for In refinement** (`CLAUDE.md`) is met; if not, it goes back to
**Backlog** with `needs-refinement` (with the user's OK).

Go beyond reading the text. Check each claim against reality:

- **Body vs board:** priority and estimate written in the body but empty on the board count
  as not set.
- **Parent fit:** is the linked feature actually about this work? Suggest a better one from
  `gh issue list --label feature --state open` (and its epic) if not.
- **Hidden blockers:** verify what the item assumes exists: repo settings
  (`gh api repos/agile-orchestrator/tulip-churn --jq '{visibility,has_wiki}'`), connectors or
  tools that must be available, skills or commands it expects to call. Anything missing is a
  blocking dependency, even if the item calls it non-blocking.
- **Completeness of lists:** when an acceptance criterion lists files, pages or places, check
  them (for example `git ls-files | xargs grep -li <term>`) and name what is missing.
- **Consistency with other items:** does it conflict with another backlog item (for example
  an option that another PBI removes)?
- **Size:** estimate above 8 must be split. If the scope grew during the session, say so and
  give your own estimate, but let the team set the number.

## 4. Propose

List the proposed changes (body edits, parent, labels, board fields, split). If the item is
too big, propose a split with user stories and Given/When/Then acceptance criteria for each
part. Ask the open decisions as short, numbered questions. The user may reject a split or
add scope: follow their call and recheck the DoR against the new scope.

## 5. Apply (after OK)

Write the new body to a file in the scratchpad directory and use
`gh issue edit <n> --body-file <file>`. Keep the body's Estimate and Priority in line with
the board fields.

Change the parent:

```bash
R=agile-orchestrator/tulip-churn
ID=$(gh api repos/$R/issues/<n> --jq .id)
gh api repos/$R/issues/<old-parent>/sub_issue -X DELETE -F sub_issue_id=$ID
gh api repos/$R/issues/<new-parent>/sub_issues -X POST -F sub_issue_id=$ID
```

Set board fields by looking up ids by name, never by typing them from memory:

```bash
FIELDS=$(gh project field-list 1 --owner agile-orchestrator --format json)
PROJECT_ID=$(gh project view 1 --owner agile-orchestrator --format json --jq .id)
ITEM=$(gh project item-list 1 --owner agile-orchestrator --format json -L 200 \
  --jq '.items[] | select(.content.number==<n>) | .id')
fid() { jq -r --arg f "$1" '.fields[] | select(.name==$f) | .id' <<<"$FIELDS"; }
oid() { jq -r --arg f "$1" --arg o "$2" '.fields[] | select(.name==$f) | .options[] | select(.name==$o) | .id' <<<"$FIELDS"; }
gh project item-edit --project-id $PROJECT_ID --id $ITEM --field-id $(fid Priority) \
  --single-select-option-id $(oid Priority P2)
gh project item-edit --project-id $PROJECT_ID --id $ITEM --field-id "$(fid 'Story Points')" --number 8
```

Actions outside the board (repo visibility, enabling a wiki, connecting services) are done
only when the user explicitly asks. Before making the repo public, scan tracked files and
history for secrets and say what becomes visible (issues, commit author emails).

## 6. Recheck and move to Ready

Show the DoR table again after the changes. Move the item to **Ready** only when every
criterion is met and the user confirms; remove `needs-refinement` if present. Verify with
`gh project item-list` that the status and fields actually changed before reporting.

Then go to the next item in **In refinement** and show its URL.

## 7. Close the session

When no item is left (or the user stops), give a summary table: number (as a link), title,
status, priority, points, parent. List side effects outside the board (repo settings,
reparented items) and any item sitting at the 8-point limit.
