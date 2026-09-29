---
name: sprint-planning
description: Run a sprint planning meeting for the Tulip Churn board - review what is left from the previous sprint and what is Ready, surface deadlines and risks, size the sprint to the team's capacity, apply the agreed scope to the board and record the planning on the wiki. Use when asked to run, start or continue a sprint planning, or to plan the next sprint.
argument-hint: "[sprint name, e.g. Sprint 4]"
---

Help the team decide what goes into the sprint. The user (usually the Product Owner) decides;
you gather, check, recommend and apply. Never create, edit, close or move an issue without the
user's OK for that change.

## 0. Which sprint are we planning?

Settle this first and state it in the first line of your first message, e.g.
"We are planning **Sprint 3** (Sep 28 – Oct 11), already running since Sep 28: 9 working
days left."

- Take `$ARGUMENTS` if given. Otherwise read the iterations (query in step 1) and today's date.
- If the current sprint has **no committed items yet** (for example a new team that arrives
  mid-sprint), plan the **current** sprint for the days that are left. Otherwise plan the
  **next** one.
- If it is ambiguous, ask the user before going further.
- "Previous sprint" below means the sprint before the one being planned.

Use the same sprint name in every message, board change and the wiki page.

## 1. Gather the facts (before presenting anything)

Board, sprints and team:

```bash
S=<scratchpad>
gh project field-list 1 --owner agile-orchestrator --format json > $S/fields.json
gh project item-list 1 --owner agile-orchestrator --format json -L 200 > $S/items.json
gh api graphql -f query='{organization(login:"agile-orchestrator"){projectV2(number:1){id
  field(name:"Sprint"){... on ProjectV2IterationField{id configuration{
  iterations{id title startDate duration} completedIterations{id title startDate duration}}}}}}}'
gh api repos/agile-orchestrator/tulip-churn/collaborators --jq '.[].login'
gh pr list --state open --json number,title,author,headRefName,statusCheckRollup
git fetch -q && git branch -r
```

Then **read the content, not just the fields.** Board fields alone miss deadlines and risks.

- Body and comments of every candidate item (step 2), its parent feature and the epic:
  `gh issue view <n> --json title,body,comments,parent` (`--comments` and `--json` don't mix).
- Search all issues and PRs for deadlines: dates, "deadline", "by <day>", "before", "pilot",
  "go-live", "Compliance".
- The wiki: the [Project Overview](https://github.com/agile-orchestrator/tulip-churn/wiki/Project-Overview) (timeline) and the
  [Meeting Notes](https://github.com/agile-orchestrator/tulip-churn/wiki/Meeting-Notes) index, above all stakeholder meetings since the last
  planning and any not yet turned into backlog items. Deadlines and commitments are usually
  written there, not in issues.
- Check suspicious claims against the code. A metric that looks too good (AUC 1.0), or a user
  report that the scores look wrong, is a reason to read `features.py` and the API. Breaking
  "features must work at scoring time" (`CLAUDE.md`) is a P0 bug for the sprint.
- For items In progress / In review: is there an owner, a branch, a PR, green checks, unticked
  DoD boxes?

## 2. Present

Start with the sprint being planned (step 0), its dates and days left, the team, and the
deadline with how many sprints remain before it.

Do **not** show Backlog or In refinement items: only Ready items can enter a sprint.

**Previous sprint's unfinished items** — one short card each, so the user can decide whether
to carry it over:

- `#n Title` · points · status
- **State:** what exists (owner, branch, PR, checks) and what is left
- **Deadline:** needed for the deadline or not, and why (cite the meeting note or issue)
- **Dependencies:** what must happen first
- ✅ / ⚠️ / ❌ **Recommendation** with a one-line reason

**Ready items not in the previous sprint** — same card, shorter.

Put findings that change the plan (a broken model, a missed requirement, stakeholder requests
not on the board) **above** the cards, with the file and line or the source page.

## 3. Capacity

Ask for each engineer's availability (days or full time) if it is not known. Give a points
range from past velocity (`items.json`: closed points per Sprint), adjusted for team size and
onboarding. Past velocity of a different team is a reference, not a target. Show the running
total against the range and say plainly when the plan is over it, but let the user decide.

## 4. Decide

Ask the open decisions as short, numbered questions: carry-over per item, additions, new bugs,
the sprint goal. Propose a sprint goal that fits the chosen items. Follow the user's call, even
against your recommendation, and note the risk in the planning notes.

## 5. Apply (after OK)

Look up ids by name, never type them from memory:

```bash
P=$(gh project view 1 --owner agile-orchestrator --format json --jq .id)
fid() { jq -r --arg f "$1" '.fields[] | select(.name==$f) | .id' $S/fields.json; }
oid() { jq -r --arg f "$1" --arg o "$2" '.fields[] | select(.name==$f) | .options[] | select(.name==$o) | .id' $S/fields.json; }
item() { jq -r ".items[] | select(.content.number==$1) | .id" $S/items.json; }
SPR=$(fid Sprint)   # iteration id comes from the graphql query in step 1
```

- **Into the sprint:** `gh project item-edit ... --field-id $SPR --iteration-id <id>` and the
  `sprint-N` label. Keep status (Ready, In progress, In review).
- **Out of the sprint:** `--field-id $SPR --clear`. An In progress item nobody is working on
  goes back to Ready. Keep existing WIP branches and mention them.
- **Acceptance criteria added during planning:** write the body to `$S/<n>.md`, edit it,
  `gh issue edit <n> --body-file $S/<n>.md`. Use Given/When/Then.
- **New bug:** follow `.github/ISSUE_TEMPLATE/bug.yml` plus acceptance criteria, technical
  notes and an estimate. Link it as a sub-issue of the fitting feature, add it to the board and
  set Status, Priority, Story Points and Sprint. Say that the estimate is yours.
- **Item that turns out broken:** reopen it with a comment linking the bug.
- **Item the team says is done:** close it as completed and set Status to Done.
- If the next iteration does not exist, ask the user to add it in the UI:
  `https://github.com/orgs/agile-orchestrator/projects/1/settings/fields/415112175` →
  "Add iteration". Don't use `updateProjectV2Field` for this: it replaces the whole iteration
  list without ids, which can unassign every item from past and current sprints.

- **Sprint board:** if the project has no view for the planned sprint yet, create a board view
  named after it (columns follow Status) and give the user its link,
  `https://github.com/orgs/agile-orchestrator/projects/1/views/<number>`:

  ```bash
  V=$(gh api graphql -f query="mutation{createProjectV2View(input:{projectId:\"$P\",
    name:\"Sprint N\",layout:BOARD_LAYOUT}){projectV2View{id number}}}" \
    --jq .data.createProjectV2View.projectV2View)
  gh api graphql -f query="mutation{updateProjectV2View(input:{viewId:\"$(jq -r .id <<<"$V")\",
    filter:\"sprint:\\\"Sprint N\\\"\"}){projectV2View{number filter}}}"
  ```

- **Stale sprint values:** list open items whose Sprint is the planned sprint but that were not
  chosen (or not Ready), and items still on an older sprint. Propose clearing or moving them.

Verify with `gh project item-list` that the fields changed before reporting.

## 6. Record on the wiki

Create a wiki page `Sprint-N-Planning` (see `Sprint-3-Planning` for the shape) and link it
from `Meeting-Notes`. Its first line says which sprint is planned, its dates,
and why (current sprint joined mid-way, or next sprint). Then: Context (team, deadline), Capacity,
Sprint goal (proposed or confirmed), Sprint backlog table (#, item, pts, prio, status, note),
Findings, Decisions (including items moved out and why), Follow-ups. Update it as decisions
come in. Edit the page in a clone of `agile-orchestrator/tulip-churn.wiki`, and ask the user
before pushing to the wiki.

## 7. Close

Give a summary table of the sprint (number, title, points, priority), the total against the
capacity range, the order of work where it matters (dependencies), the link to the wiki
page, and follow-ups: owners to assign, meeting notes to process with `/transcript-to-board`,
items to refine for the next sprint, the next iteration to create.
