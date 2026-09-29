# 🏁 Definition of Done

A backlog item is **Done** when all of the following are true.

## Code

- [ ] All acceptance criteria are met
- [ ] Code merged to `main` through a pull request that references the issue (`Closes #n`)
- [ ] At least one reviewer other than the author approved the PR
- [ ] CI is green (ruff + pytest)
- [ ] New behaviour is covered by tests

## Model changes

- [ ] Metrics are compared with the previous version and reported in the PR
- [ ] Unexpectedly large improvements are investigated before merging (check for leakage)
- [ ] Model card updated

## Documentation

- [ ] README or Notion pages updated if behaviour changed
- [ ] Architecture decisions recorded as an ADR

## Board

- [ ] Issue closed and item moved to **Done** on the Tulip Churn Board
