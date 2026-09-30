# Work on a GitHub PBI (Product Backlog Item)

**Skill**: Complete a PBI from the GitHub project board following agile best practices and the Definition of Done.

## Outcome

Implement a PBI end-to-end: understand requirements, create a feature branch, implement with tests, open a PR that meets the Definition of Done, and move the issue through the board workflow.

---

## Instructions

### 1. Read and Understand the PBI

```bash
# View the issue with all details
gh issue view <issue-number> --repo <owner/repo>

# Check the parent feature if referenced
gh issue view <parent-issue-number> --repo <owner/repo>
```

**Extract:**
- User story (As a... I want... So that...)
- Acceptance criteria (Given/When/Then)
- Technical notes and constraints
- Dependencies and open questions
- Estimate (story points)
- Parent feature/epic

**Read referenced documentation:**
- Definition of Ready (verify the PBI meets it)
- Definition of Done (this is your completion checklist)
- Any linked ADRs or design docs

### 2. Verify Definition of Ready

Before starting work, confirm the PBI meets all DoR criteria:
- [ ] Title is a short imperative sentence
- [ ] Has a complete user story
- [ ] Has testable acceptance criteria
- [ ] Estimated in story points
- [ ] Linked to parent feature
- [ ] Dependencies listed, none blocking
- [ ] Priority set

If DoR is not met, move the issue back to "In refinement" and comment with missing items.

### 3. Move Issue to "In Progress"

```bash
# Get project and field IDs
gh project field-list <project-number> --owner <org> --format json

# Move issue to "In progress"
gh project item-edit \
  --project-id <project-id> \
  --id <item-id> \
  --field-id <status-field-id> \
  --single-select-option-id <in-progress-option-id>
```

Or use the GitHub UI to drag the issue to "In progress" column.

**Self-assign the issue:**
```bash
gh issue edit <issue-number> --add-assignee @me
```

### 4. Create Feature Branch

```bash
# Branch naming: feat/<issue>-short-slug or fix/<issue>-short-slug
git checkout -b feat/24-migrate-notion-to-wiki

# Verify you're on the right branch
git branch --show-current
```

### 5. Implement the Requirements

**Development cycle:**

1. **For each acceptance criterion:**
   - Write a failing test first (TDD)
   - Implement the minimum code to pass
   - Refactor if needed
   - Commit with conventional commit message

2. **Commit messages:**
   ```bash
   git commit -m "feat: add wiki sidebar navigation

   - Create _Sidebar.md with links to all pages
   - Update Home.md to reference sidebar

   Addresses #24"
   ```

   **Conventional commit types:**
   - `feat:` new feature
   - `fix:` bug fix
   - `test:` add/update tests
   - `docs:` documentation changes
   - `refactor:` code refactoring
   - `chore:` build/tooling changes

3. **Run tests and linting:**
   ```bash
   # From CLAUDE.md conventions
   uv run pytest
   uv run ruff check .
   ```

### 6. Verify Against Acceptance Criteria

Go through each acceptance criterion:
- [ ] Manually test the Given/When/Then scenario
- [ ] Automated test exists and passes
- [ ] Edge cases handled

**For this codebase specifically:**
- Feature logic must work at scoring time (no future data/target leakage)
- Personal/sensitive data never logged
- Every behavior change has a test

### 7. Check Definition of Done

Before opening a PR, verify:

**Code:**
- [ ] All acceptance criteria met
- [ ] New behavior covered by tests
- [ ] CI will be green (run locally first)

**Model changes (if applicable):**
- [ ] Metrics compared with previous version
- [ ] Unexpectedly large improvements investigated
- [ ] Model card updated

**Documentation:**
- [ ] README or wiki pages updated if behavior changed
- [ ] Architecture decisions recorded as ADR if significant

### 8. Check Issue for Comments and Updates

Before opening the PR, check if there are any comments or updates on the issue that need to be addressed:

```bash
# View the issue with all comments
gh issue view <issue-number> --comments
```

**Review for:**
- Questions from stakeholders or team members
- Additional requirements or clarifications
- Scope changes or adjustments to acceptance criteria
- Blockers or dependencies that were added

**Actions:**
- Address any unresolved questions in your implementation
- Update code/docs if requirements changed
- Reply to comments explaining what was done
- Update the issue description if acceptance criteria changed during implementation

**Example:**
```bash
# If there's a comment asking about a specific edge case:
gh issue comment <issue-number> --body "Addressed in commit abc123: added validation for empty input"
```

### 9. Open Pull Request

```bash
# Push branch
git push -u origin feat/24-migrate-notion-to-wiki

# Create PR using template
gh pr create \
  --title "Migrate Notion docs to GitHub Wiki" \
  --body-file <(cat <<'EOF'
## What
Migrates project documentation from Notion to GitHub Wiki.

## Why
Closes #24

Docs will sit next to code and board, be versionable, and remove Notion dependency.

## Changes
- Add 8 wiki pages from Notion (Home, Project Overview, Data Dictionary, DoR, DoD, ADR-001, Model Card, How We Work)
- Add _Sidebar.md for navigation
- Update CLAUDE.md, README.md, and 10 other files to reference wiki instead of Notion
- Remove notion MCP server from .mcp.json
- Review and exclude confidential content

## Testing
- [ ] Manual: All wiki links work
- [ ] Manual: No confidential content in wiki pages
- [ ] Manual: All repo file references point to wiki
- [ ] `git grep -il notion` returns only archived references

## Checklist
- [ ] All acceptance criteria met
- [ ] Tests passing locally
- [ ] Documentation updated
- [ ] No confidential data exposed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)
```

**PR title format:**
- Use the PBI title or a clear summary
- Don't include issue number in title (it's in the description)

**PR body must include:**
- "Closes #<issue-number>" to auto-link and close on merge
- What changed and why
- Testing done
- DoD checklist

### 10. Request Review

```bash
# Add reviewers (if team members are known)
gh pr edit --add-reviewer <username>

# Move issue to "In review"
# (manually via GitHub UI or using gh project commands)
```

**Self-review first:**
- Read the diff on GitHub
- Check for debug code, TODOs, commented code
- Verify commit messages are clear
- Test the PR branch one more time

### 11. Address Review Comments

```bash
# Make changes based on feedback
git add .
git commit -m "fix: address review comments

- Update sidebar links to use exact filenames
- Add missing confidentiality check"

git push
```

**Respond to each review comment:**
- Acknowledge and implement
- Or explain why you're taking a different approach
- Mark conversations as resolved when done

### 12. Merge and Close

Once approved and CI is green:

```bash
# Merge via GitHub UI or CLI
gh pr merge --squash --delete-branch

# Verify issue auto-closed
gh issue view <issue-number>
```

**After merge:**
- [ ] Issue moved to "Done" (should happen automatically)
- [ ] Branch deleted (--delete-branch does this)
- [ ] Feature deployed/available
- [ ] Product Owner notified if needed

---

## Common Commands

### Project Board Operations

```bash
# List issues in a sprint/status
gh issue list --label sprint-3 --state open

# View project board
gh project item-list <project-number> --owner <org> --format json

# Add issue to project
gh project item-add <project-number> --owner <org> --url <issue-url>
```

### Issue Management

```bash
# Create new issue
gh issue create --title "Title" --body "Body" --label pbi

# Edit issue
gh issue edit <number> --add-label bug --milestone "Sprint 3"

# Comment on issue
gh issue comment <number> --body "Status update"

# Link sub-issue to parent
gh api repos/<org>/<repo>/issues/<parent>/sub_issues -X POST \
  -F sub_issue_id=$(gh api repos/<org>/<repo>/issues/<child> --jq .id)
```

### Branch and Commit Tips

```bash
# Amend last commit (if not pushed yet)
git commit --amend --no-edit

# Interactive rebase to clean up commits
git rebase -i HEAD~3

# Stash changes temporarily
git stash
git stash pop
```

---

## Troubleshooting

### PBI Not Ready
**Symptom:** Missing acceptance criteria, unclear requirements, blocking dependencies

**Action:**
1. Comment on issue with specific questions
2. Move back to "In refinement" or "Backlog"
3. Add `needs-refinement` label
4. Tag Product Owner for clarification

### Failing Tests
**Symptom:** CI fails after pushing

**Action:**
1. Pull latest main: `git pull origin main`
2. Rebase your branch: `git rebase main`
3. Run tests locally: `uv run pytest`
4. Fix issues and force push: `git push --force-with-lease`

### Merge Conflicts
**Symptom:** Can't merge due to conflicts with main

**Action:**
```bash
git fetch origin
git rebase origin/main
# Resolve conflicts in files
git add .
git rebase --continue
git push --force-with-lease
```

### PR Too Large
**Symptom:** Reviewer says PR is too big

**Action:**
1. Split into multiple smaller PRs
2. Create new branches from main for each part
3. Update issue to track the split
4. First PR merges, then second builds on it

---

## Quality Checklist

Before marking a PBI as done:

- [ ] All acceptance criteria met and tested
- [ ] Code reviewed and approved
- [ ] CI green (all tests pass, linting clean)
- [ ] Documentation updated (README, wiki, ADRs)
- [ ] No confidential data exposed
- [ ] PR merged to main
- [ ] Issue closed and moved to "Done"
- [ ] Branch deleted
- [ ] Product Owner or stakeholder notified if needed

---

## Example: Complete Workflow

```bash
# 1. Read the PBI
gh issue view 24 --repo agile-orchestrator/tulip-churn

# 2. Self-assign and move to "In progress"
gh issue edit 24 --add-assignee @me

# 3. Create branch
git checkout -b feat/24-migrate-notion-to-wiki

# 4. Implement (multiple commits)
# ... do work ...
git add .
git commit -m "feat: add wiki pages from Notion"

git add .
git commit -m "docs: update repo files to reference wiki"

# 5. Run tests
uv run pytest
uv run ruff check .

# 6. Push and create PR
git push -u origin feat/24-migrate-notion-to-wiki
gh pr create --title "Migrate Notion docs to GitHub Wiki" --body "Closes #24\n\n[description]"

# 7. Request review
gh pr edit --add-reviewer teammate

# 8. Address feedback and merge
# ... review cycle ...
gh pr merge --squash --delete-branch

# 9. Verify done
gh issue view 24  # Should show "CLOSED"
```
