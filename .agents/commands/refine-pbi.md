---
description: Check a backlog item against the Definition of Ready and propose a refinement
argument-hint: <issue number>
---
Fetch issue #$ARGUMENTS and the [Definition of Ready](https://github.com/agile-orchestrator/tulip-churn/wiki/Definition-of-Ready) from the wiki. Report which DoR
criteria are missing, and whether it meets the entry bar for In refinement in `CLAUDE.md`
(if not, say what is missing and that it stays in Backlog with `needs-refinement`). If the item is too big or vague, propose a split into smaller PBIs with
user stories and acceptance criteria. Ask before editing or creating issues.
