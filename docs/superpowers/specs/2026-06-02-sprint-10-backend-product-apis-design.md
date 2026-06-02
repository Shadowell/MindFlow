# Sprint 10 Backend Product APIs Design

## Context

Sprint 09 added a FastAPI backend skeleton, SQLAlchemy metadata, and PostgreSQL Alembic migrations. Sprint 10 adds the first product API slice on top of that foundation.

## Chosen Scope

This sprint focuses on the core workbench persistence path:

1. Create a draft.
2. Add or replace platform previews for Douyin, Weibo, and Xiaohongshu.
3. Create a schedule for selected platforms.
4. Create publish job rows for those scheduled platforms.
5. Read draft detail with the related previews, schedules, and publish jobs.

The frontend remains mock-only for this sprint. AutoRepost remains an external adapter boundary and is not called.

## API Shape

- `POST /api/drafts`
  - Creates the canonical draft.
- `GET /api/drafts`
  - Lists recent drafts.
- `GET /api/drafts/{draft_id}`
  - Reads one draft plus previews, schedules, and publish jobs.
- `PUT /api/drafts/{draft_id}/platform-previews/{platform}`
  - Upserts one platform-specific preview.
- `POST /api/drafts/{draft_id}/schedules`
  - Creates one schedule and one publish job for each requested platform.

The schedule endpoint requires an existing preview for each requested platform. That keeps publish jobs tied to concrete platform content rather than guessing render output.

## Data Access

The backend uses SQLAlchemy Core against the existing table metadata. Runtime database access uses `DATABASE_URL`; tests inject an isolated local database session dependency.

PostgreSQL remains the product target. Tests use a local SQLite database only to verify API behavior without relying on the user's deployed server. PostgreSQL migration rendering still runs through Alembic in `./scripts/check.sh`.

## Error Handling

- Missing draft returns `404`.
- Unsupported platform returns request validation failure.
- Scheduling a platform without a saved preview returns `400`.
- Database access uses explicit sessions and commits only after a complete operation.

## Testing

Sprint 10 uses TDD for:

- Draft create/list/detail.
- Preview upsert.
- Schedule creation with publish jobs.
- Missing-preview schedule failure.

The repository-level check continues to run frontend tests/build/lint, backend compile, backend pytest, and Alembic offline migration rendering.

## Out of Scope

- Frontend API integration.
- Live PostgreSQL connection.
- Authentication and ownership.
- AutoRepost enqueueing.
- Real AI generation.
