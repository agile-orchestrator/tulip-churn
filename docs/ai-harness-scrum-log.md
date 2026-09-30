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
