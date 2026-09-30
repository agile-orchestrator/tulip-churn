---
name: pr-review
description: Review a Tulip Churn pull request with the appropriate workflow for its author: self-review with approved comments, or interactive read-only review of another contributor's PR. Use when asked to review, explain, discuss, or self-review a PR or diff.
argument-hint: "<PR number, URL, branch, or current diff>"
---

Resolve the review target and identify the authenticated GitHub user and PR author when a PR
is available. Select one workflow and read only that reference:

- For a PR authored by the user, read [review your own PR](references/review-own-pr.md).
- For a PR authored by another contributor, read [review someone else's PR](references/review-other-pr.md).

For a branch or local diff with no PR author, ask whether the user is reviewing their own work
or another contributor's work before choosing a workflow. Never post comments, approve,
request changes, merge, alter a PR, or modify code unless the selected workflow and the user
explicitly authorize that action.
