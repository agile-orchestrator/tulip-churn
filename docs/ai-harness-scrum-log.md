# AI harness for the scrum lifecycle — presentation log

Raw material for a presentation about running the Tulip Churn scrum lifecycle with Claude Code
and its connectors (GitHub CLI, Notion, Slack, Gmail, Chrome). Newest day first. One bullet per
operation: what was asked, what the harness did, which connectors, and what was learned.

## 2026-09-29 — onboarding a new team mid-sprint

### Project setup
- **Board discovery** — installed and authenticated the `gh` CLI, read the GitHub Project
  (Tulip Churn Board) and summed up every open issue to give the new team the state of the board.
  *Connectors:* gh CLI.
- **Project / board / Notion / repo wiring** — created the GitHub Project, added the
  **In refinement** status, set Sprint, Story Points and Priority fields, fixed a PBI that had no
  status, and linked the documentation that lives in Notion from `CLAUDE.md`.
  *Connectors:* gh CLI (Projects v2), Notion.
- **Access for members** — colleagues could not see the board: they had been added to the repo
  but not to the project. Claude added every repo contributor to the project (first attempt failed
  on permissions; worked once the user had edit rights). *Lesson:* repo access ≠ project access.
  *Connectors:* gh CLI.
- **Encoding the workflow as skills** — each session was turned into a reusable skill pushed to
  the repo: `create-pbi`, `project-setup`, `create-epic`, `create-features`, `create-pbis`,
  `refinement-session`, `sprint-planning`, `review-publish-pr`. Setup changes went straight to
  `main` while bootstrapping.
- **Definition of Ready as a gate** — `CLAUDE.md` and the skills now refuse to put an item in
  *In refinement* unless it meets an entry bar aligned with the Notion DoR; the Notion DoR page
  was updated to match. *Connectors:* Notion, gh CLI.

### Backlog work
- **Idea → PBI from Notion** — the PO's idea (deadline e-mails → Slack ping to the PO) was
  found in Notion, challenged for vague points, and turned into PBI #29 with user story and
  Given/When/Then criteria. *Connectors:* Notion, gh CLI.
- **Creating an epic and a feature** — created Epic #27 *Team ways of working* and Feature #28
  *Agentic workflow for team improvement*, then linked PBIs to them as GitHub sub-issues with the
  matching labels. *Connectors:* gh CLI (sub-issues API).
- **Moving items on the board** — status, sprint, priority and estimate changes done by prompt
  ("move it to Ready", "put it In progress, not closed"). *Connectors:* gh CLI.

### Refinement session
- Listed the items In refinement and walked through them one by one against the DoR.
- **Notion → GitHub Wiki migration (#24)** — updated the parent epic/feature, set priority and an
  8-point estimate, listed every repo file that mentions Notion, enabled the wiki on the (public)
  repo, made it editable by the whole team, moved the item to Ready. The migration itself is on
  PR #40. *Connectors:* Notion, gh CLI.
- Added the Slack dependency and a newcomer **setup skill** (configures all connectors when only
  Claude Code is installed) to the scope of #29.

### Sprint planning (Sprint 3)
- Context given: the previous team left, 4 new full-time engineers joined mid-sprint.
- Claude presented last sprint's leftovers vs. Ready items, sized the sprint to capacity and
  recorded the planning in Notion. *Miss:* it did not flag a deadline written in an issue until
  the PO asked — the `sprint-planning` skill now surfaces deadlines and risks explicitly.
- Created the Sprint 3 iteration, carried unfinished PBIs over (#10, #14, #20), added #12, #24,
  #29, #34, and made the skill state which sprint is being planned first.
  *Connectors:* gh CLI, Notion.

### Doing a PBI end to end (#29)
- Assigned the PO, found the Slack invite in the PO's Gmail, the PO created the account (the one
  step Claude may not do), then Claude set up a private channel and sent a test message.
  *Connectors:* Gmail, Slack.
- Added a newcomer setup skill (PR #42) and a personal memory of e-mail-driven actions.
- **Review & publish** — reviewed the branch against the acceptance criteria and the DoD, pushed,
  opened the PR from the template with `Closes #29`, moved the item to In review; captured as the
  `review-publish-pr` skill. *Connectors:* gh CLI.
- **Asking a teammate for review on Slack**, then handling the review comments one by one:
  removed hard-coded values, and after discussion moved a personal-only skill out of the shared
  repo, with a PR comment explaining the architectural reason. *Connectors:* Slack, gh CLI.

## 2026-09-30

### Project setup — local GitHub Wiki clone
- Asked whether Claude can read the GitHub Wiki: it cloned `tulip-churn.wiki.git` and read all
  14 pages. The PO then asked for a permanent local clone: Claude cloned it at
  `../tulip-churn.wiki`, made `/setup` clone or pull it, and pointed `CLAUDE.md` and
  `project-setup` at the clone instead of raw URLs. *Connectors:* gh CLI / git.
- *Miss:* Claude first answered from a stale local `main` (still pointing to Notion) and its
  push was rejected; PR #40 had already moved the docs to the wiki. Lesson: pull before
  changing setup files.

### Project setup — squash merge only, `/setup` without Notion
- The PO asked to make squash the only merge method: Claude disabled merge commits and rebase
  merges on the repo (`gh repo edit`) and added a "Merging" rule to `CLAUDE.md` (PR titles are
  Conventional Commits, since they become the squash commit). *Connectors:* gh CLI.
- Removed Notion from `/setup` and the README: after the wiki migration (#24) `.mcp.json` has no
  Notion server, so `/setup` was still sending newcomers to log in to a tool nobody uses.
- Turned on "Automatically delete head branches" on the repo. Found 8 merged branches to clean
  up (branch head equal to the merged PR head); auto mode blocked deleting remote
  branches as destructive; the PO switched auto mode off and approved the delete. *Connectors:* gh CLI.

### Project setup — Miro connector and a retrospective skill
- Asked to connect the Miro MCP: the `claude.ai Miro` connector needs an OAuth login that
  Claude cannot start from the terminal, so the PO ran `/mcp` and logged in. Claude then
  checked the connection (user and team ids, no boards yet). *Connectors:* Miro.
- Asked for a skill to set up the sprint retrospective, on Miro. Claude read the board, the
  Sprint field iterations, the merged PRs, CI runs and the wiki (How We Work, Sprint 3
  Planning), loaded Miro's board-authoring format, and wrote `sprint-retrospective`: it
  gathers team-level sprint facts, builds the retro board in Miro, turns agreed actions into
  PBIs or working agreements, and records the retro on the wiki. `/setup` now checks the Miro
  connector. *Connectors:* gh CLI, Miro, wiki (git).
- *Lesson:* Miro's own rules ask for confirmation before creating or sharing a board, and the
  skill keeps those steps behind the facilitator's OK.
- **First run of `sprint-retrospective` (Sprint 3, snapshot on day 3).** Claude gathered the
  sprint's facts (6 committed items, 16 of 29 pts done, 8 merged PRs, 1 red run on `main`,
  2 reopened items, 2 logged harness misses), asked the PO for format, facts, location and
  sharing, then created the Miro board *Tulip Churn Sprint 3 Retro* with four frames: numbers,
  check-in, went well / to improve / try next, actions. Not shared yet. *Connectors:* gh CLI,
  Miro, wiki (git).
- *Lesson:* the first layout needed two fix-up passes (a table wider than authored, countdown
  buttons off their spot, a frame that would not shrink before its children moved). Claude
  wrote these into the skill. It also dropped "save `result_svg` in the scratchpad": the
  wrap-up runs in a later session, where the scratchpad is gone.
- **Talking points.** The PO asked for challenging talking points on the board and in the
  skill. Claude checked the facts behind them (19 of 28 commits on `main` since Sep 28 had
  no PR; #46 lists "which model is live?" as a blocking question) and added a *Talking points*
  frame with six cards: over-commitment, priority vs order of work, fixed in code vs in
  production, done vs reopened, review practice, pilot requirements vs tooling work. The
  skill now has a step to draft them. *Connectors:* gh CLI, Miro.
- *Miss:* the first board version blamed #24's early close on the AI tooling. The issue
  comment shows the team confirmed it at planning. Claude corrected the board and added a
  rule to the skill: check who did something before saying so. Also, moving the Actions
  frame left its table behind: tables are not frame children.
- **Commit and PR.** Claude committed the skill, the `/setup` and `AGENTS.md` changes and this
  log on `chore/sprint-retrospective-skill`, opened PR #50 from the template (no issue: team
  tooling under #28) and requested AdamAlansary as reviewer, the only other collaborator who
  committed to the touched files. Lint and tests green. *Connectors:* gh CLI.

### Project setup — a sprint close-out skill
- Asked, through a grilling session, for a skill to end the current sprint. The PO chose
  close-out only (no sprint review, the retro keeps its own skill), a walk through every ticket
  with a decision per ticket (next sprint, product backlog, back to refinement, re-estimate,
  split, accept as Done, drop), and a check of the sprint goal. The PO cut the questions short
  ("just add to .agents/skills/"), so Claude took its own recommendations for the rest: run it
  after the retro and before planning, keep sprint labels as history, and write an *Outcome*
  section on the sprint's planning page. Claude wrote `sprint-close`. *Connectors:* gh CLI,
  wiki (git).
- **Dry run on Sprint 3 (day 3, read only).** Claude ran the skill's queries: 7 sprint items, 2
  stray items (#8 still on Sprint 2, #35 In review without a sprint), 3 Done items with a
  Definition of Done gap (#24 and #29 merged with changes requested, #34 merged without an
  approval), sprint goal Partly met, no Sprint 4 iteration, no retro page yet. Nothing changed on
  the board or the wiki. *Connectors:* gh CLI, wiki (git).
- *Lesson:* the dry run found a wrong rule in the first draft. "PR merged, issue open → Accept as
  Done" would have closed #35, whose PR says "Part of #35" with one criterion still open. The
  skill now reads the PR body and the open criteria first.
- **Commit and PR.** Claude committed the skill and this log on `chore/sprint-close-skill`,
  opened PR #51 from the template (no issue: team tooling under #28) and requested AdamAlansary
  as reviewer, the only other collaborator who committed to the touched paths. Lint and tests
  green. *Connectors:* gh CLI.

### Sprint 3 status and refinement of #12
- Asked "what else is needed to finish Sprint 3": Claude read the board, the open PRs and the
  wiki Sprint-3-Planning page. 16 of 31 points in the sprint were done; the rest sat in review
  (#20 PR #49 no review yet, #10 PR #47 with merge conflicts, #14 PR #23 with changes
  requested) plus #12 not started. *Connectors:* gh CLI, wiki (git).
- Refined #12 against the DoR: no Given/When/Then criteria, "ADR in Notion" stale after the
  wiki migration, no metric baseline (found in PR #38: AUC 0.795, precision 0.610, recall
  0.298), and a hidden blocker on #10 (`train.py` is still a stub). It was also in Sprint 3
  although the planning page never committed it. The PO removed it from Sprint 3 (Sprint field
  cleared, `sprint-3` label removed). *Connectors:* gh CLI.
- *Miss:* Claude first said #12 had no parent; `gh project item-list` does not show parents, and
  the sub-issues API showed #3. Lesson: check the parent via the issues API, not the board.
- The PO skipped the rest of the #12 refinement (open: precision floor, threshold, fate of #11).
  Board fix: #35 moved from In review to In progress, since PR #41 was only "Part of #35" and
  the notebook re-run is still open. *Connectors:* gh CLI.
