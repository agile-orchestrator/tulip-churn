---
name: post-merge-docs
description: Detect and update Tulip Churn documentation made outdated by a merged pull request. Use after a PR merges, or when asked to check whether documentation still matches a merged change.
argument-hint: "[merged PR number, URL, or 'latest']"
---

Keep documentation accurate after a merged change without guessing at behavior or publishing
live wiki edits without approval.

## 1. Establish the merged change

Resolve `$ARGUMENTS` to a pull request. If it is omitted, identify the most recently merged
PR. Confirm that it is merged, then read its title, body, linked issue, merge commit, changed
files, and diff. If it is not merged, stop and explain that this skill applies after merge.

Treat the merged diff and the resulting `main` code as the source of truth. Identify behavior,
configuration, commands, API contracts, model or data assumptions, workflow rules, and user
steps that changed. Do not infer a documentation change solely from a renamed file or a
format-only diff.

## 2. Check likely documentation

Start with documentation directly related to the changed code, then check these sources only
when the diff makes them relevant:

- `README.md` for setup, usage, commands, and public behavior.
- `AGENTS.md` and `.agents/skills/` for repository workflow or automation changes.
- `docs/` and `.github/` for maintained local guidance, templates, and CI instructions.
- The separate `../tulip-churn.wiki` clone for project overview, data dictionary, model card,
  Definition of Ready/Done, ADRs, or meeting notes.

For every possible mismatch, verify the claim against the code or the merged diff. Report a
table with the documentation source, current claim, evidence, status (current, outdated, or
uncertain), and proposed edit. Call out missing documentation that the merged change requires.

## 3. Update after review

Show the proposed edits and wait for the user's approval before changing documentation.

- For repository documentation, create a dedicated `docs/<short-slug>` branch from updated
  `origin/main`, make only the approved edits, run `git diff --check`, and open a PR. Do not
  amend the merged implementation PR.
- For wiki documentation, pull the separate wiki clone first. Show the exact wiki diff and
  push only after the user explicitly approves the wiki publication; wiki pushes go live
  immediately and cannot use a PR.
- If an assertion cannot be verified, leave it unchanged and report the question rather than
  writing a plausible replacement.

After any GitHub or wiki operation, add a factual bullet under today's date in
`docs/ai-harness-scrum-log.md`: the request, connectors used, what changed, and any lesson or
miss. Do not include credentials or sensitive data.

## 4. Verify and report

For repository changes, verify the documentation PR contains only approved documentation and
log changes. For wiki changes, verify the pushed commit and the updated page content. Report
the PR or wiki commit, the documentation sources checked, updates made, and unresolved items.
