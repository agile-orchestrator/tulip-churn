# 📋 Project Overview

## Business problem

About one in five retail customers leaves Tulip Bank each year. The Retention team currently reacts only when a customer has already asked to close their account, which is usually too late. We want a **ranked early-warning list** of customers likely to leave, so advisors can reach out proactively.

## Objectives (v1)

- Predict the probability that a customer leaves in the next quarter
- Expose the score through an API the CRM can call
- Give the Retention team a weekly list of at-risk customers
- Pass Compliance review (model card, audit logging, no sensitive data in logs)

## Success metrics

| Metric | Target |
|---|---|
| ROC AUC on hold-out | ≥ 0.80 |
| Voluntary churn, retail segment | from ~20% to 17% within two quarters |
| Scoring latency | < 1 s per customer |

## Stakeholders

| Role | Name | Interest |
|---|---|---|
| Product Owner (Retail Banking) | Marieke De Vries | Owns the backlog, prioritises value for the Retention team |
| Retention team lead | Tom Verhoeven | Primary user of the at-risk list |
| Compliance officer | Ana Costa | Model governance, GDPR, fairness |
| Data scientist | Lotte Peeters | Data, features, model |
| ML engineer | Youssef Amrani | API, CI, deployment |

## Scope

- **In:** retail customers in France, Germany and Spain
- **Out:** business banking, automated outreach (advisors always make the call)

## Timeline

- Sprint 1 (2026-08-31 to 2026-09-13): data pipeline, baseline model, CI
- Sprint 2 (2026-09-14 to 2026-09-27): scoring API, audit logging, container, model card
- Pilot with the Retention team: November 2026
