# 🗓️ Sprint 3 Planning

**Date:** 2026-09-29
**Attendees:** kimzed, theunis, AdamAlansary, swachmann, jasperkrebbers

**Planning for: Sprint 3** (2026-09-28 to 2026-10-11), the sprint already in progress. The new team arrived mid-sprint, so this planning covers the days left in Sprint 3, not the next sprint. Sprint board: [Sprint 3](https://github.com/orgs/agile-orchestrator/projects/1/views/4)

## Context

- Sprint 3: 2026-09-28 to 2026-10-11. Planning held one day late, on 2026-09-29.
- New team: the previous team has left. Four new engineers joined: theunis, AdamAlansary, swachmann, jasperkrebbers.
- Deadline: pilot with the German Retention team in November 2026 (see [[Q4-Goals-with-the-PO]] and the [[Project-Overview]]). That leaves Sprint 3, Sprint 4 (2026-10-12 to 2026-10-25) and part of Sprint 5 before the pilot.

## Capacity

- All four engineers work full time this sprint: 4 people × 10 working days = 40 person-days.
- Velocity of the previous team (two engineers; for reference only): Sprint 1 closed 12 pts, Sprint 2 closed 8 of 26 committed.
- First sprint for the new team, so part of the time goes to onboarding. Estimated capacity: 16–20 pts.

## Sprint goal (proposed)

The model gives real scores at scoring time, training is reproducible from `train.py`, CI is reliably green, and the audit logging required by Compliance is merged.

## Sprint backlog

| # | Item | Pts | Prio | Status | Note |
|---|---|---|---|---|---|
| 34 | [Bug] Account-closure feature leaks the target; model scores ~0% in production | 3 | P0 | Ready | Do before or together with #10 |
| 14 | Log scoring requests for audit | 3 | P1 | In review | PR #23 green; needs review |
| 10 | Port notebook training into train.py | 5 | P1 | Ready | New AC: `/model-card` builds the model card from `models/metrics.json` |
| 20 | [Bug] CI intermittently red on test_split_keeps_churn_rate | 2 | P1 | Ready | Good first ticket |
| 29 | Flag deadline emails to the PO with a ready-to-run Claude Code instruction | 8 | P3 | Ready | Team tooling (#28) |

Committed: 21 pts, above the estimated 16–20 pts. If the sprint runs short, #29 is the first to drop.

## Findings

- Target leakage in the CRM account-closure feature (#8): `AccountClosureRequested` is derived from the churn label in training and is always 0 at scoring time. This explains the AUC of 1.0 and the near-0% scores the Retention team saw. The AUC of 1.0 must not be used in steering-committee material.
- The two stakeholder meetings (Sep 15, Sep 18) have not been processed to the backlog yet. The pilot requirements (configurable threshold, weekly ranked list, reasons per customer, 30-day contact exclusion, fairness analysis) are not on the board.

## Decisions

- Leakage fixed in Sprint 3 as P0 bug #34; #8 reopened and linked to it.
- #15 Containerise the scoring API: out of Sprint 3, planned for Sprint 4 (no point deploying before the leakage fix). Status back to Ready; WIP branch `feat/15-dockerfile` kept.
- #17 Draft model card for v1: planned for Sprint 4, after #34 (correct metrics), #10 (`/model-card` from `models/metrics.json`) and Ana's fairness checklist.
- #24 Migrate Notion docs to GitHub Wiki (8 pts): added to Sprint 3. First reported done and closed; the check afterwards found it only partly done (8 wiki pages exist; meeting notes, `_Sidebar.md`, repo references to Notion and archiving Notion are still open). Reopened and set to In progress. Sprint total with #24: 29 pts, well above the 16–20 pts estimate.
- #29 added to Sprint 3.
- The Sprint 4 iteration does not exist on the board yet, so #15 and #17 have no Sprint set.

## Follow-ups

- [ ] Process the Sep 15 and Sep 18 stakeholder notes into backlog items and refine them during Sprint 3, so the pilot items are Ready for Sprint 4
- [ ] Assign owners to the Sprint 3 items
- [ ] Confirm the sprint goal
