# Sprint 10 Contract: Backend Product APIs

## Goal

Add the first database-backed product API slice for MindFlow so drafts, platform previews, schedules, and publish jobs can be created and read through FastAPI. The sprint should prove the backend workflow with isolated tests while keeping production PostgreSQL credentials and platform publishing out of scope.

## In Scope

- Add FastAPI routes for:
  - creating drafts
  - listing recent drafts
  - reading one draft with platform previews, schedules, and publish jobs
  - upserting platform previews for a draft
  - creating a schedule for a draft and the matching publish jobs
- Add Pydantic request/response schemas for the Sprint 10 API surface.
- Add SQLAlchemy session and engine wiring that uses `DATABASE_URL` for runtime database-backed operations.
- Add isolated backend API tests using a local test database setup.
- Keep the existing PostgreSQL Alembic migration verification passing.
- Update product spec, progress, and QA report.

## Out of Scope

- Connecting to the deployed PostgreSQL server.
- Committing real database credentials or platform secrets.
- Applying migrations against production or staging PostgreSQL.
- Wiring the frontend to the backend APIs.
- Calling AutoRepost or any Douyin, Weibo, Xiaohongshu, OpenAI, or other external API.
- Adding authentication, user ownership, or workspace membership.
- Adding destructive delete endpoints.

## Deliverables

- `backend/app/api/`
- `backend/app/db/session.py`
- `backend/app/schemas.py`
- Backend tests for draft, preview, schedule, and publish job API behavior.
- Updated `docs/spec.md`
- Updated `docs/progress.md`
- `docs/superpowers/specs/2026-06-02-sprint-10-backend-product-apis-design.md`
- `docs/qa/sprint-10-backend-product-apis-report.md`

## Done Means

- A caller can create a draft through the API.
- A caller can upsert platform-specific previews for that draft.
- A caller can create a schedule for selected platforms and receive publish jobs backed by persisted rows.
- A caller can read a draft detail response that includes previews, schedules, and publish jobs.
- Backend tests prove the API persists and reads data through SQLAlchemy instead of mock state.
- `./scripts/check.sh` passes.

## Verification

```bash
./scripts/check.sh
git diff --check
rg -n "sprint-10|/api/drafts|platform_previews|publish_jobs|DATABASE_URL" backend docs scripts
```

Manual or QA checks:

- Confirm the API tests do not require the user's deployed PostgreSQL server.
- Confirm no real production credentials are committed.
- Confirm AutoRepost remains out of runtime scope.
- Confirm the frontend remains unchanged unless a later sprint explicitly wires it to the API.

## Risks / Notes

- SQLite-backed tests validate API behavior locally, while Alembic still validates PostgreSQL migration rendering.
- The API is single-operator for now because authentication remains a later sprint.
- The schedule endpoint creates publish jobs but does not enqueue them to AutoRepost.

## Handoff

- Next likely step: wire the frontend workbench to the new backend API or connect the backend to the deployed PostgreSQL environment after credentials and deployment handling are confirmed.
