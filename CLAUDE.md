# Tulip Bank — churn early-warning

Predicts which retail customers are likely to leave Tulip Bank so the Retention team can
contact them first. Small Python repo: data loading, feature engineering, a scikit-learn
model and a FastAPI scoring service.

## Where things live

| What | Where |
|---|---|
| Code | this repo (`agile-orchestrator/tulip-churn`) |
| Backlog, sprints, board | GitHub Project **Tulip Churn Board** (org `agile-orchestrator`, project #1) |
| Documentation (overview, data dictionary, DoR, DoD, ADRs, model card, meeting notes) | Notion workspace **Tulip Bank**, page "Tulip Bank — Churn Early-Warning" (via the `notion` MCP server) |

Read the Notion **Definition of Ready** before creating or refining backlog items and the
**Definition of Done** before opening or reviewing a PR.

## Commands

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

**Branches:** `feat/<issue>-short-slug`, `fix/<issue>-short-slug`, `chore/<slug>`.
**Commits:** Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`, `refactor:`).
**PRs:** fill `.github/pull_request_template.md`, reference the issue with `Closes #n`,
move the item to **In review**. `/review-publish-pr` reviews the branch and does all three.

## Board operations with the gh CLI

```bash
gh issue list --label pbi --state open
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
