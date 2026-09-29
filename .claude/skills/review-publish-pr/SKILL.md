---
name: review-publish-pr
description: Review the work on a PBI branch against the issue's acceptance criteria and the Definition of Done, then push the branch, open the PR from the template linked to the issue and move the item to In review. Use when asked to review a finished PBI, check that everything is done, or push and open the PR for the current branch.
argument-hint: [issue number, defaults to the one in the branch name]
---

Review the current branch for the issue in `$ARGUMENTS` (or the number in the branch name,
`feat/<n>-slug` / `fix/<n>-slug`), then publish it as a PR. Stop and ask if the branch is
`main` or has no issue number.

The review comes first. Only publish when the user has asked to, or agrees after seeing the
review. Never merge, approve, close the issue or move it to Done: the DoD needs a reviewer
other than the author.

## 1. Gather

```bash
N=<issue>
BR=$(git branch --show-current)
gh issue view $N --json title,body,labels,state,projectItems
git status -sb                                   # uncommitted work? unpushed commits?
git log --oneline main..HEAD
git diff --stat main...HEAD && git diff main...HEAD
gh pr list --head $BR --state all                # a PR may already exist
cat .github/pull_request_template.md
```

Read the **Definition of Done** (Notion page under "Tulip Bank — Churn Early-Warning", or the
GitHub Wiki once migrated). Do not use the "(backup)" copy.

If there is uncommitted work, ask whether it belongs in the PR before going on.

## 2. Review

- **Acceptance criteria:** go through every Given/When/Then of the issue. For each one say
  met, not met or dropped, with the evidence (file and line, test, or live check). When a
  criterion depends on something outside the repo (connector, Slack channel, Gmail label,
  scheduled routine, board field), check its live state with the matching tool rather than
  trusting the code.
- **Scope:** flag changes outside the issue's scope and in-scope items with no change.
- **Code:** read the diff for bugs and for the conventions in `CLAUDE.md` (feature logic in
  `features.py` that works at scoring time, a test for every behaviour change, Conventional
  Commit messages). For a large diff, run `/code-review` on the branch.
- **Checks:** run them locally when Python changed:

  ```bash
  uv run ruff check .
  uv run pytest -q
  ```

  With no Python changes, write "N/A, no Python changes" instead.
- **Definition of Done:** go through each item. Model changes also need metrics compared
  with the previous version, a leakage check for large gains and the model card updated.

Report in this order: what is done, what blocks (with the fix), smaller points. Keep it short
and say plainly whether the PBI is ready for a PR. If the user decides to drop or accept an
item, record that in the PR body instead of changing the issue.

## 3. Publish

Push, then create or update the PR. Fill the template in a scratchpad file:

- **What:** one or two sentences.
- `Closes #<n>`.
- **How to test:** concrete steps a reviewer can follow.
- Notes on anything dropped or done differently from the issue, as agreed with the user.
- **Checklist:** tick only what is true. Write "N/A" with the reason instead of ticking an
  item that does not apply. Leave unmet items unticked.
- End with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

Title: Conventional Commit style, like the commits (`feat: ...`, `fix: ...`).

```bash
git push -u origin $BR
gh pr create --base main --head $BR --title "<title>" --body-file <file>
# or, if a PR is already open: gh pr edit <pr> --body-file <file>
```

## 4. Move the item to In review

Look the ids up by name, never hard-code them:

```bash
FIELDS=$(gh project field-list 1 --owner agile-orchestrator --format json)
PROJECT_ID=$(gh project view 1 --owner agile-orchestrator --format json --jq .id)
STATUS_FIELD=$(jq -r '.fields[] | select(.name=="Status") | .id' <<<"$FIELDS")
IN_REVIEW=$(jq -r '.fields[] | select(.name=="Status") | .options[] | select(.name=="In review") | .id' <<<"$FIELDS")
ITEM=$(gh project item-list 1 --owner agile-orchestrator --format json -L 200 \
  --jq ".items[] | select(.content.number==$N) | .id")
gh project item-edit --project-id $PROJECT_ID --id $ITEM --field-id $STATUS_FIELD \
  --single-select-option-id $IN_REVIEW
```

## 5. Verify and report

```bash
gh pr view <pr> --json url,closingIssuesReferences --jq '{url, closes:[.closingIssuesReferences[].number]}'
gh project item-list 1 --owner agile-orchestrator --format json -L 200 \
  --jq ".items[] | select(.content.number==$N) | .status"
```

`closes` must contain the issue number and the status must be `In review`; fix it before
reporting if not. Report the PR URL, the linked issue, the board status and anything left
for the reviewer or the user (for example live resources to clean up).
