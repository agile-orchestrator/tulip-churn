# 🏛️ ADR-001: Use FastAPI for the scoring service

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-08 |
| **Deciders** | Youssef Amrani, Lotte Peeters, Marieke De Vries |

## Context

The Retention team's CRM needs to request a churn score for one customer at a time, synchronously, when an advisor opens a customer file. The model is a scikit-learn pipeline in Python. The internal platform runs containers and expects an HTTP service with a health endpoint.

## Options considered

1. **FastAPI** — Python, async, request validation with Pydantic, OpenAPI docs generated automatically
2. **Flask** — Python, well known, but validation and docs need extra libraries
3. **Batch only** (nightly scores in a table) — simplest, but scores would be up to a day old and the CRM team wants live scores
4. **Managed model serving** on the cloud platform — not approved yet for customer data

## Decision

Use **FastAPI** with a single `POST /score` endpoint and `GET /health`. The model is loaded once from `models/model.joblib`.

## Consequences

- Input validation comes for free and the CRM team gets an OpenAPI spec at `/docs`
- The model file must be available where the service runs (see the Containerise PBI)
- A batch export for the weekly at-risk list is still needed and will be a separate job, not part of the API
