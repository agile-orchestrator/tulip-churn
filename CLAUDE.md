# Tulip Bank — churn early-warning

Predicts which retail customers are likely to leave Tulip Bank so the Retention team can
contact them first. Small Python repo: data loading, feature engineering, a scikit-learn
model and a FastAPI scoring service.

## Where things live

| What | Where |
|---|---|
| Code | this repo (`agile-orchestrator/tulip-churn`) |
| Backlog, sprints, board | GitHub Project **Tulip Churn Board** (org `agile-orchestrator`, project #1) |
| Documentation (overview, data dictionary, DoR, DoD, ADRs, model card, meeting notes) | [GitHub Wiki](https://github.com/agile-orchestrator/tulip-churn/wiki) |

Read the wiki **Definition of Ready** before creating or refining backlog items and the
**Definition of Done** before opening or reviewing a PR.

## Reading and editing the wiki

The wiki is a separate git repo (`agile-orchestrator/tulip-churn.wiki`, branch `master`), not
a folder of this one. Keep a local clone **next to** this repo at `../tulip-churn.wiki`, never
inside it (`/setup` creates it). GitHub has no wiki API, so read and edit the local files:

```bash
git -C ../tulip-churn.wiki pull                 # always pull before reading or editing
cat ../tulip-churn.wiki/Definition-of-Ready.md
# edit, then commit and push; there are no PRs, a push goes live at once
git -C ../tulip-churn.wiki add -A
git -C ../tulip-churn.wiki commit -m "docs: update wiki page"
git -C ../tulip-churn.wiki push origin master
```

Wiki changes cannot go in the same PR as the code they describe: push them separately and
mention them in the PR.

## Commands

First time, or something looks broken: run `/setup` (`.claude/skills/setup/SKILL.md`).

```bash
uv sync
uv run python scripts/generate_data.py          # data/raw/Churn_Modelling.csv
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/01_exploration.ipynb
uv run uvicorn tulip_churn.api:app --reload
uv run pytest
uv run ruff check .
```

## Code conventions

- Python 3.11+, src layout, `ruff` for lint (line length 100).
- Feature logic goes in `features.py` and must work at scoring time, when the target is unknown.
- Every behaviour change comes with a test in `tests/`.

## Scrum workflow

**Hierarchy:** Epic → Feature → PBI (issue type Task) / Bug. Link children as GitHub
sub-issues of their parent and also set the matching label (`epic`, `feature`, `pbi`, `bug`).

**Board columns (Status field):** Backlog → In refinement → Ready → In progress → In review → Done.
A new item goes to **In refinement** only when it meets the entry bar below; otherwise it
stays in **Backlog**. It moves to **Ready** only when it meets the full Definition of Ready.

**Entry bar for In refinement** (no content invented to pass it):
- short imperative title
- user story (As a / I want / So that)
- at least one testable acceptance criterion (Given/When/Then)
- a candidate parent feature, or a note that one is still to be decided
- open questions listed

If an item misses any of these, do not put it in In refinement: tell the user which points
are missing and that it needs more work first. With their OK, park it in **Backlog** with the
`needs-refinement` label.

**Other project fields:** Sprint (iteration), Story Points (1, 2, 3, 5, 8, 13), Priority (P0–P3).

**Writing a PBI:**
- Title: short imperative ("Make decision threshold configurable").
- Body: user story (As a / I want / So that) + testable acceptance criteria (Given/When/Then)
  + technical notes + estimate. Use the templates in `.github/ISSUE_TEMPLATE/`.
- Vague items ("Improve model") get the `needs-refinement` label and stay in Backlog.

**Found something off? Log it.** Whenever you notice a problem outside the scope of your
current task (a bug, hard-coded value, stale output, leaking feature, flaky check, deprecation,
docs that no longer match the code), put it on the board with the `log-finding` skill. Don't
ask first and don't fix it in the current branch. Findings always go to **Backlog** with
`needs-refinement`, never straight to In refinement. This overrides the "with their OK" above.
If the fix is only a few lines (no open decisions, no retrain), don't wait: fix it right away
on its own branch and open a PR with a reviewer, as described in the skill. Wrong board state
goes in your report, not in a new issue. Wrong instructions in this repo get fixed on a
`chore/` branch. Report P0 findings right away and everything else at the end of your reply.

**Branches:** `feat/<issue>-short-slug`, `fix/<issue>-short-slug`, `chore/<slug>`.
Branch from an up-to-date `main` (`git fetch origin` first, branch from `origin/main`), never
from another feature or chore branch.
**Commits:** Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`, `refactor:`).
**PRs:** fill `.github/pull_request_template.md`, reference the issue with `Closes #n`,
request a reviewer (a collaborator other than the author, picked as in the `log-finding`
skill), and move the item to **In review**. `/review-publish-pr` reviews the branch and does
all of this.
**Merging:** squash merge only (the repo allows no merge commits or rebase merges), so each PR
lands on `main` as one commit. Give the PR a Conventional Commit title, since it becomes that
commit's message: `gh pr merge <n> --squash`.

## Board operations with the gh CLI

```bash
gh issue list --label pbi --state open
# `gh issue view` and `gh pr edit` fail here (Projects classic deprecation error); use the API:
gh api repos/agile-orchestrator/tulip-churn/issues/<n> --jq '.title, .body'
gh api repos/agile-orchestrator/tulip-churn/pulls/<pr>/requested_reviewers -X POST -f 'reviewers[]=<login>'
gh issue create --title "..." --label pbi --body-file body.md
gh project item-list 1 --owner agile-orchestrator --format json
gh project item-add 1 --owner agile-orchestrator --url <issue-url>
gh project field-list 1 --owner agile-orchestrator --format json   # field + option ids
gh project item-edit --project-id <id> --id <item-id> --field-id <status-field> \
  --single-select-option-id <option-id>
# sub-issues
gh api repos/agile-orchestrator/tulip-churn/issues/<parent>/sub_issues -X POST \
  -F sub_issue_id=$(gh api repos/agile-orchestrator/tulip-churn/issues/<child> --jq .id)
```

Custom slash commands for common scrum tasks are in `.claude/commands/`.

## Presentation log

We are preparing a talk on using an AI harness for the scrum lifecycle. After any scrum
operation that goes through the connectors (GitHub board, Notion, Slack, Gmail, Chrome) — e.g.
creating or moving items, refinement, sprint planning, reviews, setup — add a short bullet to
`docs/ai-harness-scrum-log.md` under today's date: what was asked, what the harness did, which
connectors, and any lesson or miss. Keep it factual and never log secrets.
