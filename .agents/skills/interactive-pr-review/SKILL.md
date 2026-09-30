---
name: interactive-pr-review
description: Help a developer interactively understand and review another contributor's Tulip Churn pull request: explain code changes, trace behavior, identify risks, and answer follow-up questions. Use when asked to review, walk through, explain, or discuss someone else's PR or diff.
argument-hint: "<PR number, URL, branch, or current diff>"
---

Act as a collaborative, read-only reviewer for a pull request authored by someone other than
the user. Help the developer understand the change and decide what needs attention. Do not
post comments, approve, request changes, merge, alter the PR, or modify code unless the user
explicitly asks.

## 1. Establish the review target

Resolve `$ARGUMENTS` to a pull request, branch, or current working-tree diff. For a PR, read
its author, title, description, linked issue, changed files, commits, review state, CI status,
and full diff. Confirm the PR is not authored by the authenticated user; route self-authored
PRs to `self-pr-review`.

Read the relevant issue and Definition of Done when they clarify the intended behavior. For a
branch or local diff, establish the base revision. State the review target and whether the
available information is complete; a PR description does not prove the implementation meets it.

## 2. Walk through the change

Give a concise map of the changed behavior, affected users, changed components, relevant data
or control flow, tests, and requirements. Use precise file and line references when available.
Explain unfamiliar code in plain language, then invite the developer to choose a file,
function, scenario, test, or concern to explore.

## 3. Investigate questions

Answer follow-up questions by tracing the actual code and diff. Compare before and after
behavior, including error and edge cases; check acceptance criteria; and look for regressions,
incorrect assumptions, missing validation, data leakage, unsafe logging, API compatibility
problems, and untested cases.

Distinguish confirmed defects from concerns, questions, and suggestions. State evidence and
practical impact. Keep the discussion incremental: answer the question at hand before offering
a wider review.

## 4. Report findings

For each actionable finding, provide severity, file and line, trigger or scenario, impact, and
a concrete fix direction. Do not invent findings or claim a concern is verified without
evidence. If the user later asks to publish feedback, restate the target and action before
posting it and record the GitHub operation in `docs/ai-harness-scrum-log.md`.
