# Review your own PR

Help a developer improve their own pull request before external review. Focus on defects,
mistakes, missing tests, unclear behavior, requirement gaps, and risks. Do not approve, merge,
or alter code. Post comments only after the user approves the exact proposed comments.

## 1. Confirm ownership and collect evidence

Resolve `$ARGUMENTS` to a pull request, branch, or local diff. For a PR, identify the
authenticated GitHub user and confirm they are the PR author. If another person authored it,
read the [other-contributor workflow](review-other-pr.md) instead.

Read the PR description, linked issue, diff, changed files, commits, CI status, existing review
comments, and relevant Definition of Done. Treat the merged-base comparison and current code as
the source of truth. For a branch or local diff, establish the base revision and state what PR
metadata is unavailable.

## 2. Perform a self-review

Review the change against its acceptance criteria and intended behavior. Check changed paths,
error cases, compatibility, input validation, tests, security and privacy concerns, logging,
data or model leakage, documentation, and CI results where relevant. Do not treat a passing CI
run as proof that a requirement is met.

Return a concise table of confirmed issues, concerns, and missing checks. For each item include
severity, file and line, trigger, evidence, impact, and a suggested correction. Do not invent
findings merely to produce comments. Distinguish a confirmed defect from a question or a
non-blocking improvement.

## 3. Draft and post comments

For each actionable item, draft a concise, constructive comment tied to the exact changed line
when possible. Use a general PR comment only when no changed line is suitable. Before posting,
show the complete set of proposed comments and ask the user to approve that exact set. Check
existing comments first to avoid duplicates.

After approval, post only the approved comments. Verify that each appears on the intended PR
and report its URL. Do not submit an approval, request changes, merge the PR, create an issue,
or change code unless the user explicitly requests that separate action.

## 4. Log and hand off

After posting comments or making any GitHub review operation, add a factual bullet under
today's date in `docs/ai-harness-scrum-log.md`: the request, connector used, action, and any
lesson or miss. Do not include secrets. End by listing remaining fixes, tests, or questions for
the developer before they request external review.
