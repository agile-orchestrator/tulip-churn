---
name: sprint-close
description: Close out a sprint on the Tulip Churn board - go through every sprint item and stray item with the Product Owner, decide per ticket (next sprint, product backlog, back to refinement, re-estimate, split, accept as Done, drop), apply the decisions, judge whether the sprint goal was met and record the outcome on the wiki planning page. Use when asked to end, close or wrap up a sprint, or to handle unfinished sprint items.
argument-hint: "[sprint name, e.g. Sprint 3]"
---

Close the sprint so the next planning starts from a clean board. The user (usually the Product
Owner) decides what happens to each ticket. You gather, propose and apply. Every board change
and every wiki push waits for the user's OK.

## 0. Which sprint?

State it in the first line of your first message, e.g. "Closing **Sprint 3** (Sep 28 to
Oct 11). Next sprint: **Sprint 4** (Oct 12 to Oct 25)."

- Take `$ARGUMENTS` if given. Otherwise take the iteration that contains today. Between
  sprints, take the most recent completed iteration whose planning page has no `## Outcome`
  section yet.
- The next sprint is the iteration that starts the day after this one ends. If it does not
  exist, give the user the settings link,
  `https://github.com/orgs/agile-orchestrator/projects/1/settings/fields/415112175` →
  "Add iteration", and carry on. "Next sprint" moves wait until it exists. Adding iterations
  through `updateProjectV2Field` replaces the whole list without ids and can unassign every
  item from past sprints, so that stays a UI task.
- Close-out comes after the retro and before the next planning. Moving an item off the sprint
  removes it from what `sprint-retrospective` reads. If
  `../tulip-churn.wiki/Sprint-N-Retrospective.md` does not exist yet, say so and ask whether
  to go on.
- If the sprint still has days left, say how many and offer a **dry run**: the full
  walk-through with decisions recorded, then the change list (step 5) and the Outcome text
  (step 6) shown, with nothing applied or pushed. Mark every number "as of <date>".

## 1. Gather the facts (read only)

```bash
S=<scratchpad>
R=agile-orchestrator/tulip-churn
git -C ../tulip-churn.wiki pull --ff-only
gh project field-list 1 --owner agile-orchestrator --format json > $S/fields.json
gh project item-list 1 --owner agile-orchestrator --format json -L 200 > $S/items.json
gh api graphql -f query='{organization(login:"agile-orchestrator"){projectV2(number:1){id
  field(name:"Sprint"){... on ProjectV2IterationField{id configuration{
  iterations{id title startDate duration} completedIterations{id title startDate duration}}}}}}}' \
  > $S/sprints.json
gh pr list -R $R --state all -L 100 \
  --json number,title,state,headRefName,author,reviewDecision,mergedAt,statusCheckRollup > $S/prs.json
```

The **tickets** to go through:

| Group | Selection in `items.json` |
|---|---|
| Sprint items | `.sprint.title == "Sprint N"` |
| Stray items | items not Done on an older sprint, and items In progress or In review with no Sprint. Items labelled `epic` or `feature` stay out: their status follows their children |

`items.json` has no issue state. The query below gives it.

For each ticket, read the state behind the fields:

```bash
gh api graphql -f query='{repository(owner:"agile-orchestrator",name:"tulip-churn"){issue(number:<n>){
  state stateReason assignees(first:5){nodes{login}}
  closedByPullRequestsReferences(first:5,includeClosedPrs:true){nodes{number state reviewDecision}}
  timelineItems(itemTypes:[CROSS_REFERENCED_EVENT],first:20){nodes{... on CrossReferencedEvent{
  source{... on PullRequest{number state headRefName}}}}}}}}'
gh api repos/$R/issues/<n> --jq .body          # acceptance criteria
gh api repos/$R/issues/<n>/comments --jq '.[] | "\(.user.login) \(.created_at): \(.body)"'
```

`closedByPullRequestsReferences` lists the PRs that close the issue. A PR written without
`Closes #n` only shows up as a cross-reference, so match those on title and branch
(`fix/35-...`).

From `Sprint-N-Planning.md` take the sprint goal and whether it was confirmed, the committed
items and points (the sprint backlog table plus items its Decisions section adds), and the
items moved out.

Done when every ticket has its status, points, priority, owner, issue state, linked PRs with
review decision and checks, the acceptance criteria still open, and whether it was committed
at planning or added later.

## 2. Done items in one table

Show every ticket whose status is Done or whose issue is closed in one table: `#n Title`,
points, and a ✅ / ⚠️ per Definition of Done check that GitHub can show:

- issue closed as completed, status Done
- closing PR merged
- PR approved by someone other than the author (`reviewDecision` is `APPROVED`)
- checks green

A row with only ✅ needs no question. For each ⚠️, name the gap with a link and ask: keep it
Done (the gap goes in the Outcome notes), reopen it (it then gets a card in step 3), or log a
follow-up with the `log-finding` skill.

## 3. Go through the unfinished tickets, one at a time

Order them by priority, committed items before added ones. Show one card per message and wait
for the answer:

```
#n Title · 5 pts · P1 · In review · committed at planning
State:  owner, branch, PR (checks, review decision), last activity
Open:   the acceptance criteria not met yet
Needed: for the next sprint goal or the deadline, or not (cite the source)
Recommendation: <choice>, with a one-line reason
```

The choices:

| Choice | Board change | Comment on the issue |
|---|---|---|
| **Next sprint** | Sprint → next sprint, add label `sprint-<N+1>`. Status stays | "Sprint N close: carried over to Sprint N+1." |
| **Product backlog** | clear Sprint. In progress / In review → Ready, Ready stays Ready. The branch or PR stays open | "Sprint N close: back to the product backlog. <reason>" |
| **Back to refinement** | clear Sprint, status → In refinement | "Sprint N close: back to refinement. <what is unclear>" |
| **Re-estimate** | goes with one of the above: new Story Points (1, 2, 3, 5, 8, 13) for the work that is left | adds "Estimate <old> → <new>: <reason>." |
| **Split** | the done part: trim its acceptance criteria to what is done, close as completed. The rest: a new PBI via the `create-pbi` skill under the same parent, which then gets its own card | "Sprint N close: split, the rest is #m." |
| **Accept as Done** | close as completed, status → Done | "Sprint N close: accepted as Done." |
| **Drop** | close as not planned, status → Done | "Sprint N close: dropped. <reason>" |

"Product backlog" means out of the sprint. The Backlog *status* is for unrefined items, and a
Ready item keeps its Ready status.

Sprint labels (`sprint-2`, `sprint-3`) stay on an item when it leaves a sprint. The Sprint
field holds one value, so the labels are the only record of every sprint the item went through.

Typical recommendations: a PR with green checks that only waits for review → Next sprint. Not
started and not needed for the next goal → Product backlog. The work turned out bigger or
unclear → Back to refinement, often with Re-estimate. A PR merged while the issue is still
open → read the PR body and the open criteria first. A PR that says "Part of #n" or leaves a
criterion unticked means work is left, so Accept as Done fits only when nothing is. Follow the
user's call, also against your recommendation.

Keep the decisions in `$S/decisions.md` (#, choice, new points, comment). Done when every
ticket from step 1 has a decision.

## 4. Was the sprint goal met?

Judge the goal on the state after the decisions, since "Accept as Done" and "Split" change what
is done. Split the goal into its parts and give each Met / Partly / Not met with links to the
evidence (issue, PR, CI run on `main`). The overall verdict is Met when every part is met, Not
met when every part is not met, and Partly otherwise. If the goal was never confirmed, say so and judge the
proposed goal. The user confirms the verdict.

## 5. Apply (after OK)

Show the full change list from `$S/decisions.md`, per ticket: field changes, label, comment,
close. Apply it after the user's OK. A dry run stops at the list.

```bash
P=$(jq -r .data.organization.projectV2.id $S/sprints.json)
fid() { jq -r --arg f "$1" '.fields[] | select(.name==$f) | .id' $S/fields.json; }
oid() { jq -r --arg f "$1" --arg o "$2" '.fields[] | select(.name==$f) | .options[] | select(.name==$o) | .id' $S/fields.json; }
item() { jq -r ".items[] | select(.content.number==$1) | .id" $S/items.json; }
NEXT=<iteration id of the next sprint, from sprints.json>

gh project item-edit --project-id $P --id $(item <n>) --field-id $(fid Sprint) --iteration-id $NEXT
gh project item-edit --project-id $P --id $(item <n>) --field-id $(fid Sprint) --clear
gh project item-edit --project-id $P --id $(item <n>) --field-id $(fid Status) \
  --single-select-option-id $(oid Status Ready)
gh project item-edit --project-id $P --id $(item <n>) --field-id "$(fid 'Story Points')" --number 3
gh label create sprint-4 -R $R -d "Sprint 4 (Oct 12 - Oct 25)" -c c5def5   # when missing
gh api repos/$R/issues/<n>/labels -X POST -f 'labels[]=sprint-4'
gh api repos/$R/issues/<n>/comments -X POST -f body='Sprint 3 close: ...'
gh api repos/$R/issues/<n> -X PATCH -f state=closed -f state_reason=completed   # or not_planned
```

Verify with a fresh `gh project item-list`. Done when the board matches the decision list:
every open item has left sprint N, and no open item is In progress or In review without a
sprint.

## 6. Record on the wiki

Add an `## Outcome` section at the end of `../tulip-churn.wiki/Sprint-N-Planning.md`. If the
sprint had no planning page, create one with only this section.

```markdown
## Outcome

Closed on <date>. Sprint goal: **Met / Partly / Not met**.

| Goal part | Verdict | Evidence |
|---|---|---|

Committed <x> pts, done <y> pts (velocity), <z> pts added during the sprint.

| # | Item | Pts | Committed at planning | Decision | Note |
|---|---|---|---|---|---|

Board fixes: <stray items handled, Definition of Done gaps kept as Done>
```

Velocity is the points of sprint items closed as completed. Show the diff and push after the
user's OK, because a wiki push goes live at once.

## 7. Close

Add a bullet to `docs/ai-harness-scrum-log.md` under today's date: what was asked, what the
harness did, the connectors (gh CLI, wiki) and any lesson or miss.

End with the goal verdict, committed vs done points and the velocity of the last three sprints,
the decision table, the wiki link, whether the next iteration exists, and what is left for the
next planning: items to refine, owners to confirm, and `sprint-planning` for Sprint N+1.
