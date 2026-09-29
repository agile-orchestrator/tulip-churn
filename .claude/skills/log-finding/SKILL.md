---
name: log-finding
description: Log something that is off, noticed while working on another task (a bug, hard-coded value, stale output, leaking feature, failing or flaky check, deprecation, docs that no longer match the code), as a Bug or PBI on the Tulip Churn board, without waiting for the user's OK. Use whenever you spot a problem outside the scope of the item you are working on.
argument-hint: <what you noticed, with file:line>
---

The team wants every problem noticed along the way on the board, so nothing gets lost in a chat
reply. Log it yourself: the user has pre-approved creating these items, so there is **no
confirmation step** (unlike `create-pbi`). Keep going with the current task afterwards.

## 1. Decide where it belongs

| What you noticed | Where it goes |
|---|---|
| Inside the scope of the item you are working on | Fix it in the current branch; no new item |
| Code, data, model, CI or docs problem outside that scope | **Bug** or **PBI** (this skill) |
| Board state is wrong (status, labels, Sprint field, missing type or parent) | Do not create an issue. List it in your report and offer to fix it |
| A command, skill or instruction in this repo is wrong or out of date | Fix the instruction (`CLAUDE.md`, `.claude/skills/`, `.claude/commands/`) on a `chore/` branch |
| Your own mistake in this session (wrong branch base, bad commit) | Fix it and mention it; no item |

**Bug** when something is broken or gives wrong results (a crash, wrong numbers, a leak,
a path that only works on one machine). **PBI** for everything else (cleanup, deprecation,
missing test or docs).

Do not fix an out-of-scope problem in the current branch: it keeps PRs focused and reviewable.
Only exception: the current item cannot be finished without it. Then say so in the PR.

## 2. Check it is not already on the board

```bash
gh issue list --state all --limit 200 --search "<2-3 keywords>" --json number,title,state
```

If an open item already covers it, add a comment with the new evidence
(`gh api repos/agile-orchestrator/tulip-churn/issues/<n>/comments -f body=...`) instead of a
duplicate. If a closed one covers it, create a new item and reference the old one.

## 3. Draft from facts only

Write the body to a file in the scratchpad directory. Use only what you observed: file and
line, the command you ran, its output, the metric you measured. Do not invent a user need, an
impact or a number to fill a heading. Write "unknown" or leave it as an open question.

**Bug** (`.github/ISSUE_TEMPLATE/bug.yml`), title `[Bug] <what is wrong>`:

- **Parent feature**: `#n`, or "to be decided"
- **What happened**: with `file:line` and evidence
- **Expected behaviour**
- **Steps to reproduce**
- **User story**: As a / I want / So that
- **Acceptance criteria**: Given/When/Then, including a test in `tests/`
- **Technical notes**
- **Open questions**: mark each blocking or non-blocking
- **How it was found**: which task or PR you were working on (`#n`)
- **Severity**: low, medium, high, critical
- **Estimate (suggested)**: 1, 2, 3, 5 or 8

**PBI** (`.github/ISSUE_TEMPLATE/pbi.yml`): the same headings as in the `create-pbi` skill
(parent, user story, acceptance criteria, technical notes, dependencies and open questions,
estimate, priority), plus **How it was found**. Title is a short imperative sentence.

For model or data findings, also name the affected metric with its current value and say
whether the data is available at scoring time (see the Definition of Ready).

## 4. Create it

Follow step 4 of the `create-pbi` skill (create, set issue type, link parent, add to board,
set fields by option name), with these differences:

- Bug: `--label bug`, issue type `Bug`. PBI: `--label pbi`, issue type `Task`. Add an area
  label if one fits (`data`, `model`, `api`, `ci`, `docs`).
- **Status**: **In refinement** if the draft meets the entry bar in `CLAUDE.md`, otherwise
  **Backlog** with `needs-refinement`. You do not need to ask before parking it in Backlog.
- Add `needs-refinement` as well if Definition of Ready items are still open. Estimates are
  only suggestions until the team refines the item.
- **Priority**: set the field. P0 only for wrong results or outages in production, security or
  compliance problems. Say which priority you chose and why in the report.
- **Never** set Sprint, Story Points or **Ready**. That is for the team and the PO.

Verify with step 5 of `create-pbi`.

## 5. Tell the user

- **P0 or security/compliance finding:** tell the user right away, before carrying on.
- **Everything else:** list it at the end of your reply under **Logged along the way**:
  `#n title: status, priority, one line on why`.
- List board-state problems (from step 1) separately, with the fix you would make.
