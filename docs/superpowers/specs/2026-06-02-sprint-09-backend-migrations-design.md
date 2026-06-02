# Sprint 09 Backend Migrations Design

## Context

Sprint 08 documented MindFlow's PostgreSQL data model and kept AutoRepost behind an external adapter boundary. Sprint 09 turns that schema into executable backend structure without connecting to production PostgreSQL or publishing platforms.

## Options Considered

### Recommended: Python FastAPI, SQLAlchemy, and Alembic

This matches AutoRepost's Python/FastAPI shape, keeps a narrow future integration path, and gives the project mature migration tooling. It also keeps the frontend independent while the backend foundation settles.

### Alternative: Node API with Prisma

This would align with the existing frontend toolchain, but it creates a split from AutoRepost's Python runtime and adds an ORM/migration choice before the project has backend conventions.

### Alternative: Migration SQL only

This is the smallest possible step, but it postpones backend boundaries and would make Sprint 10 choose the application stack again.

## Chosen Architecture

- `backend/app/` owns service code.
- `backend/app/main.py` exposes the FastAPI app and a small health endpoint.
- `backend/app/settings.py` owns environment configuration and requires `DATABASE_URL` when a database URL is requested.
- `backend/app/db/models.py` owns SQLAlchemy metadata and table definitions.
- `backend/migrations/` owns Alembic configuration, environment wiring, and versioned migrations.
- `backend/tests/` verifies observable schema and configuration behavior.

## Data Model

The SQLAlchemy model mirrors `docs/architecture/postgresql-schema.md`:

- `topics`
- `personas`
- `drafts`
- `draft_assets`
- `platform_accounts`
- `platform_previews`
- `schedules`
- `publish_jobs`
- `publish_job_events`

The model uses PostgreSQL-oriented types where the product needs them, including UUID primary keys, `timestamptz`, `jsonb`, and text arrays. Status values remain text columns with check constraints rather than PostgreSQL enums, so early migrations stay simple and reversible.

## Configuration

The backend reads environment variables through a typed settings object. `DATABASE_URL` is documented in `.env.example`, but no real value is committed. Tests verify that database-dependent access fails loudly when `DATABASE_URL` is missing.

## Migration Verification

Sprint 09 uses Alembic offline SQL generation as the migration verification target. This proves the migration can render PostgreSQL DDL without requiring the user's deployed PostgreSQL server or storing credentials locally.

Live migration application is intentionally deferred until credentials, backup expectations, and environment handling are confirmed.

## Error Handling

- Missing `DATABASE_URL` raises a clear configuration error.
- The health endpoint does not claim database connectivity.
- Alembic offline migration checks fail the repository verification if migrations cannot render.

## Testing

Tests cover:

- FastAPI health endpoint behavior.
- Settings behavior around `DATABASE_URL`.
- SQLAlchemy metadata table coverage.
- Important constraints and indexes for core workflow tables.
- Alembic offline SQL generation through `scripts/check.sh`.

## Out of Scope

- Product CRUD APIs.
- Frontend API integration.
- Production PostgreSQL connection.
- AutoRepost calls.
- Authentication and account ownership.
