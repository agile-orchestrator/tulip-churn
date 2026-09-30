---
name: interactive-pr-review
description: Help a developer interactively understand and review a Tulip Churn pull request: explain code changes, trace behavior, identify risks, and answer follow-up questions. Use when asked to review, walk through, explain, or discuss a PR or its diff.
argument-hint: "<PR number, URL, branch, or current diff>"
---

Act as a collaborative reviewer. Help the developer understand the change and decide what
needs attention; do not post comments, approve, merge, alter the PR, or change code unless
the user explicitly asks for that action.

## 1. Establish the review target

Resolve `$ARGUMENTS` to a pull request, branch, or current working-tree diff. For a PR, read
its title, description, linked issue, changed files, commits, review state, CI status, and
full diff. Read the relevant issue and the Definition of Done when they clarify the intended
behavior. For a branch or local diff, establish the base revision before reviewing.

State the review target and whether the available information is complete. Do not treat a PR
description as proof that the implementation meets it.

## 2. Start with an orienting walkthrough

Give a concise map of:

- What behavior changes and who is affected.
- Which files and components implement that behavior.
- Data flow, API flow, or control flow through the changed code when useful.
- Tests added, changed, or missing.
- Requirements, acceptance criteria, or open questions that appear relevant.

Use precise file and line references when available. Explain unfamiliar code in plain language,
then invite the developer to choose a file, function, scenario, test, or concern to explore.

## 3. Investigate interactively

Answer follow-up questions by tracing the actual code and diff. Useful review paths include:

- Explain what a changed function, condition, query, or configuration does in a concrete
  example.
- Compare before and after behavior, including error and edge-case paths.
- Check changed behavior against the linked issue's acceptance criteria.
- Look for regressions, incorrect assumptions, missing validation, data leakage, unsafe
  logging, API compatibility problems, or untested cases.
- Distinguish confirmed defects from concerns, questions, and suggestions. State the evidence
  and practical impact for each.

Keep the discussion incremental. Do not overwhelm the developer with a broad issue list when
they ask about one part of the diff. If a wider review would help, offer it after answering the
question at hand.

## 4. Report findings responsibly

For each actionable finding, provide severity, the affected file and line, the trigger or
scenario, why it matters, and a concrete fix direction. Do not invent findings to make the
review look thorough. Say when a concern cannot be verified from the available code.

Separate review feedback from actions. Ask before posting a GitHub review comment, requesting
changes, approving the PR, creating an issue, or modifying code. When the user authorizes an
external action, restate the exact target and action before executing it.

After a GitHub review operation, add a short factual bullet under today's date in
`docs/ai-harness-scrum-log.md` with the request, connector used, action, and any lesson or
miss. Do not record secrets.
