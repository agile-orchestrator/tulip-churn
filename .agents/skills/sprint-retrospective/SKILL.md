---
name: sprint-retrospective
description: Prepare and wrap up a sprint retrospective for the Tulip Churn team on a Miro board. Gathers the sprint's facts from the GitHub board, repo and wiki, drafts talking points that challenge the team, builds the retro board in Miro (sprint in numbers, check-in, talking points, went well / to improve / try next, actions), and after the retro turns the agreed actions into backlog items or working agreements and records the retro on the wiki. Use when asked to set up, prepare, run or wrap up a retro or retrospective.
argument-hint: "[sprint name, e.g. Sprint 3]"
---

Prepare the retro so the team spends its hour talking, not collecting data. The user (the
facilitator, often the Scrum Master or PO) decides; you gather, prepare and apply. Ask for OK
before each of these steps: creating the Miro board, sharing it, creating or editing issues,
pushing to the wiki.

Rules for the whole session:

- **Blameless.** Numbers stay at team level. No counts per person (PRs, points, commits), and
  no names next to problems. Only name people as owners of actions they agreed to.
- **Facts, not opinions.** Everything you put on the board comes from a source you can link
  (issue, PR, CI run, wiki page, log entry). Never write stickies for participants or guess
  how the sprint felt.
- **Public by default.** The repo and wiki are public, and a Miro board is visible to everyone
  it is shared with. No customer data, secrets or confidential Compliance details.

## 0. Which sprint?

State it in the first line of your first message, e.g. "Retro for **Sprint 3** (Sep 28 to
Oct 11), retro on Fri Oct 9 at 16:00."

- Take `$ARGUMENTS` if given. Otherwise read the iterations (step 1) and today's date.
- If today is in the last week of the current sprint, the retro is for the current sprint.
  Otherwise take the most recent completed sprint that has no `Sprint-N-Retrospective` wiki
  page yet.
- Ask when it is unclear, for example when the last sprint was run by a previous team.
- The retro takes place on the sprint's last Friday. Take the time from
  `../tulip-churn.wiki/How-We-Work.md`.
- If the sprint is still running, every number is a snapshot: write "as of <date>" on the
  board and offer to refresh it on the day of the retro.

## 1. Gather the facts (read only)

```bash
S=<scratchpad>
R=agile-orchestrator/tulip-churn
git -C ../tulip-churn.wiki pull --ff-only
gh api graphql -f query='{organization(login:"agile-orchestrator"){projectV2(number:1){
  field(name:"Sprint"){... on ProjectV2IterationField{configuration{
  iterations{id title startDate duration} completedIterations{id title startDate duration}}}}}}}'
gh project item-list 1 --owner agile-orchestrator --format json -L 200 > $S/items.json
jq -r --arg s "Sprint N" '.items[] | select(.sprint.title==$s)
  | [.content.number, .status, (.["story Points"] // 0), (.priority // "-"), .title] | @tsv' $S/items.json
```

`START` is the sprint's `startDate`. `END` is `startDate + duration - 1`, or today if the sprint
is still running.

```bash
gh pr list -R $R --state merged --search "merged:START..END" -L 100 \
  --json number,title,url,createdAt,mergedAt
gh issue list -R $R --state all --search "created:START..END" -L 100 --json number,title,labels,url
gh run list -R $R --branch main --created START..END -L 200 --json conclusion,workflowName,url
gh api repos/$R/issues/<n>/events --jq '.[] | select(.event=="reopened") | .created_at'  # per sprint item
```

Then read the context:

- `Sprint-N-Planning` on the wiki: the sprint goal, the committed items and points, and the
  decisions. Compare with the board. Committed and Done, committed and not Done, added during
  the sprint (on the board, not on the planning page), dropped (on the page, Sprint cleared).
- The previous retro, `Sprint-<N-1>-Retrospective`, and its actions. Find the issues that came
  from it with `gh issue list -R $R --state all --search "Sprint-<N-1>-Retrospective in:body"`
  and give each action a status (done, in progress, not started, dropped).
- Meeting notes dated inside the sprint (`Meeting-Notes.md` index).
- `docs/ai-harness-scrum-log.md`, entries inside the sprint dates: what the AI harness did and
  every *Miss*. These are facts about the team's tooling and belong in the retro.

Turn this into team-level numbers:

| Fact | How |
|---|---|
| Points committed / done / not done | planning page vs `items.json` |
| Items added and dropped mid-sprint | planning page vs `items.json` |
| PRs merged, median hours from open to merge | `gh pr list` above |
| Bugs opened during the sprint | issues created in the window with label `bug` |
| Red runs on `main` | `gh run list` above, `conclusion=="failure"` |
| Items reopened | issue events above |
| Sprint goal met? | the goal on the planning page vs what is Done. Say "partly" when it is |

Wrong board state you notice on the way (an open issue In review whose PR is merged, a Sprint
value on an item that is not in the sprint) goes in your report, not on the retro board.

## 2. Draft talking points

Talking points get the team past "it went fine". Each one puts a fact from step 1 next to
what the team said it would do, and ends in a question the team would rather skip. Draft 4
to 6, and look for them where plan and practice part ways:

| Tension | Example from Sprint 3 |
|---|---|
| Commitment vs capacity or velocity | 29 pts committed against a capacity of 16 to 20 |
| Priority vs the order work got done | a P3 item done while two P1 items wait for review |
| "Done" vs done | the leak fix merged while nobody knew which model was live; an item closed and reopened 11 minutes later |
| Our own rules vs practice (DoD, PR reviews, CI, the sprint goal) | 19 of 28 commits on `main` without a PR, one turned CI red |
| The deadline and stakeholder asks vs where the time went | pilot requirements not on the board while half the merged PRs were team tooling |
| What we trusted the AI tooling with vs what we checked | the misses in `docs/ai-harness-scrum-log.md` |
| Previous retro actions that did not happen | the actions from `Sprint-<N-1>-Retrospective` |

Write each point as a headline of at most 8 words that states the fact, one or two sentences
with the numbers ending in an open question, and the source links. For example: *Fixed in
code is not fixed in production.* "The leak fix is merged, but nobody can say which model
is live, and the retrain (#46, P0) sits in the Backlog. When is a bug done for us?"

- Challenge the team's choices and the system, never a person. Write "we", use no names.
- Check every number and every actor before you write it down. Read the issue comments and
  events before saying who closed, merged or reported something. In the first run an early
  close was blamed on the AI tooling; the issue comment showed the team had confirmed it.
- Prefer the points with the most at stake for the next sprint (the deadline, production,
  Compliance) over the easy ones.

## 3. Present and agree

Show the facilitator, in this order:

1. The sprint, its dates, the retro date and time, the team (`How-We-Work.md`).
2. The facts table from step 1, each row with its source link.
3. What happened, at most 6 bullets with links: incidents, reopened items, deadlines,
   stakeholder news, harness misses.
4. The previous retro's actions and their status.
5. The talking points from step 2.
6. The board you propose (step 4) and its name, `Tulip Churn Sprint N Retro`.

Then ask short, numbered questions:

1. Format: *Went well / To improve / Try next* (default), or another one (Start / Stop /
   Continue, Mad / Sad / Glad, 4Ls). Use the facilitator's column names as written.
2. Any fact or talking point to leave off the board, or to soften?
3. Create the board at the team root, or in a Miro space (ask for its URL)?
4. Who gets access, by e-mail address, and with which role (default `editor`)? Never guess
   addresses from the git log.

## 4. Build the Miro board (after OK)

1. `board_search_boards` with the board name. If it already exists, ask whether to reuse it
   (then read it with `canvas_search` first) or create a new one.
2. `board_create` with the name and a one-line description: sprint, dates, "facts as of
   <date>".
3. Call `canvas_get_canvas_composer_skill` without a step, then with `step="design"` and
   `step="dsl"`, and follow its rules. They decide colours, fonts and spacing. The numbers
   frame is a *synthesis* artifact; the other frames are *workspace* artifacts: leave them
   mostly empty and never fabricate participant content.
4. Create all frames in one `canvas_create_from_svg` call, left to right in this order:

| Frame | Contents |
|---|---|
| **Sprint N in numbers** | Sprint goal and whether it was met; dates and "as of"; the facts table; a table widget of the sprint items (item as a full issue URL, points, status); "What happened" bullets with full URLs; previous actions with status |
| **Check-in** | an `alignment_scale` "How did Sprint N go for you?" (Rough / OK / Great) and a `countdown` action button of 3 minutes |
| **Talking points** | one card per agreed point (headline, question, source links) and the instruction "Pick the two that sting most and start there. Add a sticky next to a point if you see it differently." |
| **Went well / To improve / Try next** (or the agreed columns) | one empty lane per column, with a header and a one-line instruction; a `countdown` of 10 minutes; a `dot_voting` widget "Vote on what to act on" |
| **Actions** | a table widget with the columns Action (title), Owner (text), Check at (date, default the next retro) and Issue (link), and the instruction "At most 3. One owner each." Put the previous retro's open actions in as rows; if there are none, leave the table empty |

   Links must be full URLs (`https://github.com/agile-orchestrator/tulip-churn/issues/34`);
   shorthand like `#34` stays dead text on the board. Escape `&`, `<` and `>` in the SVG, or
   nothing gets created.
5. When the result reports changed dimensions, fix overlaps with `canvas_update_from_svg`,
   starting from the returned `result_svg`. What the first run on Sprint 3 ran into:
   - A table renders wider than its authored width. Fit it inside the frame's padding with
     `data-scale` (for example 0.95).
   - Give countdown buttons `width="126" height="124"`, or they land off their authored spot.
   - A frame cannot shrink while a child is outside the new size. Move the children first,
     then resize the frame in a second call.
   - Read-back shows the markup in a `textArea` escaped (`&lt;b&gt;`). That is only how it
     is returned; the board shows bold text and links. Leave it.
   - A `<text>` at 67 px is about 96 px tall. Start the next element 20 px below its box.
   - A table authored inside a frame lands in the right spot but is not a child of the
     frame. When you move the frame, move the table too, with absolute coordinates.
   - Start a text with a word, not with `#24`: the create result listed such a text without
     its `#`.
6. `board_share` for each approved address, then `board_show` once to show the board.

## 5. During the retro (only when asked)

- Refresh the numbers frame: rerun step 1, read the frame (`canvas_search`, then
  `canvas_read_as_svg`) and update the changed widgets with `canvas_update_from_svg`.
  Widget ids only come from a `result_svg` or a read, never from memory.
- Group stickies into themes: read the lanes (step 6) and propose theme labels to place next
  to each cluster. Do not move, edit or delete participants' stickies.

## 6. Wrap up after the retro

1. Read the board. `canvas_search` with `result_mode="areas"` and the column, Talking points
   and Actions titles as patterns, then `canvas_read_as_svg` with the returned scope. A sticky belongs to
   the lane whose x-range contains it. If the votes are not readable from the SVG, ask the
   facilitator for the top-voted stickies.
2. Summarise per column in themes, in the team's own words, without names. Show it.
3. For every agreed action (at most 3) propose where it goes, and ask for OK per action:

| The action is... | It goes to |
|---|---|
| Work on code, data, CI or tooling | a PBI via the `create-pbi` skill, under the fitting feature (team process work: the feature under the epic *Team ways of working*). The body says `Source: https://github.com/agile-orchestrator/tulip-churn/wiki/Sprint-N-Retrospective`. It meets the entry bar in `AGENTS.md` or goes to Backlog with `needs-refinement` |
| A team agreement ("review PRs within a day") | a line under *Working agreements* in `How-We-Work.md` on the wiki (add the section when there is none) |
| A wrong skill or instruction in this repo | a fix on a `chore/` branch, as `AGENTS.md` describes |

   Every action has one owner who agreed to it and a check date, by default the next retro.
4. Fill the Actions table on the board with owner, date and the issue link. Read the table
   first with `canvas_read_as_svg` to get its field and record ids.
5. Record the retro on the wiki (step 7).

## 7. Record on the wiki

Create `Sprint-N-Retrospective.md` in `../tulip-churn.wiki` (pull first), in the shape of the
other meeting pages:

```markdown
# Sprint N Retrospective

**Date:** <retro date>
**Attendees:** <names the facilitator gives>
**Miro board:** <board URL>
**Processed to backlog:** yes / no

Retro for **Sprint N** (<start> to <end>).

## Sprint in numbers
## Talking points
## Previous actions
## What went well
## What to improve
## Try next
## Actions
| Action | Owner | Check at | Issue |
## Working agreements
```

Link it from `Meeting-Notes.md` (add a *Retrospectives* section when there is none) and from
`_Sidebar.md` under Meeting Notes. Write themes, not quotes. Show the diff and push only after
the facilitator's OK: a wiki push goes live at once.

## 8. Close

Add a bullet to `docs/ai-harness-scrum-log.md` under today's date: what was asked, what the
harness did, the connectors (Miro, gh CLI, wiki) and any lesson or miss.

End with the board link, the wiki page link, the actions table (action, owner, check date,
issue link), wrong board state found in step 1, and what is left: owners still to confirm,
new items to refine before the next sprint planning, the date of the next retro.
