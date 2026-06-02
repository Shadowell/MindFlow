# Sprint 09 Contract: Backend Skeleton and PostgreSQL Migrations

## Goal

Create the first backend foundation for MindFlow using a small Python FastAPI stack, with SQLAlchemy models and Alembic migrations for the Sprint 08 PostgreSQL schema. The sprint should make the database shape executable and reviewable without connecting to the user's deployed PostgreSQL server yet.

## In Scope

- Add a `backend/` Python project using FastAPI, SQLAlchemy, Alembic, and pytest.
- Add application settings that require an explicit `DATABASE_URL` when the backend needs a database connection.
- Add SQLAlchemy models for topics, personas, drafts, draft assets, platform accounts, platform previews, schedules, publish jobs, and publish job events.
- Add the initial Alembic migration for the documented MVP PostgreSQL schema.
- Add tests that verify required tables, indexes, constraints, and Alembic offline SQL generation.
- Update `scripts/check.sh` so repository verification includes backend tests and migration checks.
- Update project progress and add a Sprint 09 QA report.

## Out of Scope

- Connecting to the deployed PostgreSQL server.
- Storing production database credentials in the repository.
- Adding draft, preview, schedule, or publish job HTTP CRUD APIs.
- Calling AutoRepost or moving AutoRepost code into MindFlow.
- Connecting Douyin, Weibo, Xiaohongshu, OpenAI, or other external production APIs.
- Adding authentication or user ownership columns.

## Deliverables

- `backend/pyproject.toml`
- `backend/app/`
- `backend/migrations/`
- `backend/tests/`
- Updated `scripts/check.sh`
- Updated `.env.example`
- Updated `docs/spec.md`
- Updated `docs/progress.md`
- `docs/superpowers/specs/2026-06-02-sprint-09-backend-migrations-design.md`
- `docs/qa/sprint-09-backend-migrations-report.md`

## Done Means

- The backend has a minimal FastAPI entrypoint and health endpoint.
- SQLAlchemy metadata includes every table from the Sprint 08 schema.
- The initial Alembic migration can render PostgreSQL SQL offline without requiring live database credentials.
- Tests confirm important table names, status constraints, foreign keys, and indexes.
- `./scripts/check.sh` runs frontend checks plus backend tests, compile checks, and Alembic offline SQL generation.
- Repository verification passes.

## Verification

```bash
./scripts/check.sh
git diff --check
rg -n "sprint-09|alembic|SQLAlchemy|FastAPI|DATABASE_URL|publish_jobs" backend docs scripts .env.example
```

Manual or QA checks:

- Confirm no production PostgreSQL URL or secret is committed.
- Confirm migrations model the Sprint 08 schema without sharding, CQRS, event sourcing, or speculative denormalized read models.
- Confirm AutoRepost remains out of runtime scope for this sprint.
- Confirm backend tests do not require the user's deployed PostgreSQL server.

## Risks / Notes

- Alembic offline SQL generation proves migration rendering, not application against a live PostgreSQL instance.
- The first backend API surface is intentionally minimal; product CRUD APIs should be added in Sprint 10 after the schema foundation is verified.
- Authentication remains a later sprint, so this schema stays single-operator.

## Handoff

- Next likely step: add draft, platform preview, schedule, and publish job APIs backed by the new database layer, then wire the frontend away from mock state.
