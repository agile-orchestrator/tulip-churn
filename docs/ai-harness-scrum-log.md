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

### Picking up a PBI — #11 "Improve model"
- The PO asked to take the PBI about improving the model: Claude assigned #11 to them
  (`gh api .../assignees`). *Connectors:* gh CLI.
- *Miss flagged:* #11 is still a one-liner with `needs-refinement` ("maybe try xgboost") and
  overlaps #12 (compare candidate models), so it does not meet the Definition of Ready yet.
- **slopguard setup for #11.** The PO wanted the `python-slopguard` Stop hook before starting.
  Claude installed it as a dev dependency, walked through every setting one at a time with
  examples measured on this repo (ruff, vulture, PMD), and applied the PO's choices: complexity 4,
  15 statements, return tuples of 2, 3 types per hint, `existing_violations = "block"`,
  PMD required. It installed PMD locally and added a type-hint rule to `AGENTS.md`. Committed on
  `feat/11-improve-model`, not `main`, at the PO's request. *Connectors:* gh CLI.
- *Lesson:* testing a claim beats explaining it. Claude's copy-paste example was wrong: PMD
  only matches exact copies, even with `--ignore-identifiers`. The PO spotted it, and Claude
  opened kimzed/python-slopguard#1.
- *Miss:* `on_missing_tool = "error"` blocked Claude's own next Stop before PMD was installed,
  and the generated `vulture_whitelist.py` broke `ruff check` until it was excluded.
- **Finding logged and fixed.** `data.TARGET` was unused while `"Exited"` was hard-coded in 6
  places. Following `log-finding`, Claude created #55 (PBI, `data`, P3, parent #3), fixed it on
  `chore/55-use-target-constant` and opened PR #56 with theunis as reviewer (last committer to
  `data.py` and the tests); #55 is In review with no sprint. *Connectors:* gh CLI.

### Working on #11 while the PO was away
- **Asked:** "work on the model improvement (current branch), log slopguard feedback, see you
  for the PR". Claude planned first (plan mode). #11 did not meet the Definition of Ready and
  duplicated #12. Training lives in the notebook, and #10's PR #47 is still open. The PO
  approved the plan. *Connectors:* gh CLI, wiki (git).
- **Refinement by the harness.** Claude rewrote #11 as "Compare candidate churn models and pick
  the best ranker": story, 4 Given/When/Then criteria, named metric (precision in the top 10%,
  because Retention calls the top ~500 each week), 5 SP, Sprint 3, In progress. It removed
  `needs-refinement` and closed #12 as a duplicate. #11 was already a sub-issue of #3.
  *Connectors:* gh CLI (issues API, Projects).
- **Result: no model change.** `tulip_churn.compare` runs 5 candidates on the same folds.
  Gradient boosting (current) 0.801 AUC / 0.611 top-10% precision, XGBoost 0.799 / 0.603,
  logistic regression 0.757. The synthetic data comes from a known formula, whose own score is
  0.810 / 0.628. So the current model is within about 1 point of the best any model can do.
  ADR-002 (wiki) keeps gradient boosting. Better results need new signal (#36), not a new
  algorithm.
- *Lesson:* "try XGBoost" was answered with a ceiling measurement instead of a model swap. An
  improvement ticket should name the metric *and* check how much room is left before it is
  estimated.
- *Miss:* `xgboost` pulled a ~300 MB CUDA wheel (`nvidia-nccl`) on Linux. Claude switched to
  `xgboost-cpu`, then made it a dev dependency, because XGBoost did not win.
- *Miss:* the documented wiki push (`git push origin master`) failed: the wiki is cloned over
  HTTPS and the gh CLI is set to SSH. It worked with
  `git -c credential.helper='!gh auth git-credential' push`.
- **slopguard feedback:** no blocks. `compare.py` was written as 13 small functions from the
  start (complexity ≤ 4, ≤ 15 statements, ≤ 4 args, settings in a `CompareConfig` dataclass),
  and a manual `slopguard hook stop` returned clean. The only lint hit was a ruff E501 (line
  length) on one signature. *Observation:* slopguard did not flag the untyped fixtures in
  `tests/conftest.py`, although the project rule wants type hints in `tests/`.
- **PR.** Opened via `/review-publish-pr` with theunis as reviewer (author of #47 and assignee
  of #10, where the chosen model gets wired into `train.py`). #11 moved to In review.
  *Connectors:* gh CLI.
- **Findings logged (`log-finding`).** #59 "Enforce type hints with ruff ANN rules" (PBI, P3,
  Backlog + `needs-refinement`): `ruff --select ANN` finds 33 missing hints. Too big for the
  fast path, and enabling a lint rule is a team decision. The broken wiki-push instruction was
  fixed in the repo: PR #60 (`chore/wiki-push-credentials`, `/setup` runs `gh auth setup-git`),
  with AdamAlansary as reviewer. *Connectors:* gh CLI (issues, Projects).
- **Correction: slopguard never ran on the #11 code.** The PO asked why it did not fire.
  Reading its source showed that the Stop hook only checks files `git status` shows as changed.
  Claude had committed `compare.py` during the turn, so at Stop the tree was clean and the hook
  let everything through without checking. "No blocks" above meant *not checked*, not *clean*.
  The code met the limits only because Claude had read `[tool.slopguard]` and run the hook by
  hand before committing.
- *Lesson:* a guard built for "Claude edits, the human commits" is silently off when the agent
  commits on its own, which is exactly what `work-on-pbi` and `log-finding` do. A green check
  with nothing checked looks like a pass.
- **Fix.** A `PreToolUse` hook (`.claude/hooks/slopguard-on-commit.sh`) runs the slopguard
  checks before every `git commit` Claude makes, and exit 2 blocks the commit. Tested with a
  probe file: it blocks a 9-branch, 5-argument function, and it lets clean commits and other git
  commands through. Upstream issue opened on kimzed/python-slopguard.
- **Reset for a rerun.** At the PO's request the #11 code was taken off the branch (the
  comparison module, tests, report and xgboost dependency) and the branch was force-pushed.
  PR #58 was closed, and #11 went back to In progress so the PO can rerun the task with the new
  hook.

### #11 rerun — with the slopguard commit hook active
- Rebuilt `compare.py`, `tests/test_compare.py` and `reports/model_comparison.md` from scratch
  on `feat/11-improve-model`, this time with the `PreToolUse` `git commit` hook live. Two
  commits (`ed388d4`, `8621bb5`); **slopguard did not block either one**, this time because it
  genuinely ran (verified: the hook's `jq` payload strips `stop_hook_active` and it fires on
  every commit, not just at Stop). *Connectors:* gh CLI, git.
- **Reproducibility gap found during the rerun, not a slopguard finding.** `GradientBoostingClassifier`
  and `XGBClassifier` had no `random_state`, so results drifted run to run. Two runs of the new
  module gave XGBoost 0.799 ROC AUC once and 0.762 the next — a 0.037 swing, close to the 0.05
  leakage-investigation threshold the PBI itself sets. Seeded both estimators; the report is now
  stable across runs. The pick (gradient boosting) does not change either way.
  *Lesson:* an unseeded non-deterministic model is a correctness bug a lint/complexity guard
  like slopguard cannot see — worth a manual re-run check, not just one green run, before trusting
  a comparison's numbers.
- **Wiki.** ADR-002 refreshed with the reproducible numbers and moved from "Proposed" to
  "Accepted", pushed directly to `tulip-churn.wiki` (`gh auth setup-git` was needed again to
  push over https). *Connectors:* git / gh CLI.
- **PR.** Opened PR #61 (replaces the closed #58) with theunis as reviewer, same rationale as
  before. #11 moved to In review. *Connectors:* gh CLI (Projects).
