# Progress Log

## Current Baseline

- Branch: `main`
- Harness status: `active`
- Last verified state: `Sprint 10 backend product APIs verified with ./scripts/check.sh`

## Active Contract

- `docs/contracts/sprint-10-backend-product-apis.md`

## Latest Completed Work

- Added source-backed development standards for Python, Java, database design, and frontend development.
- Updated project rules so future Codex sessions read relevant standards before technology-specific work.
- Added scale-based database design guidance to avoid premature architecture.
- Added lightweight reusable module guidance for personal/small projects, with email-first authentication as the default.
- Added Sprint 04 contract for a compact authentication module decision matrix.
- Added matrix coverage for Supabase Auth, Better Auth, Auth.js, django-allauth, FastAPI Users, enterprise IAM escalation, and custom-auth escalation.
- Added Sprint 04 QA report with manual checks and verification evidence.
- Added Sprint 05 contract for the first stack-specific reusable module recipe.
- Added a documentation-only Next.js/Supabase Auth recipe covering email-first auth, server-side sessions, row-level security, local development, and verification.
- Added Sprint 05 QA report with manual checks and verification evidence.
- Added Sprint 06 contract for a Django/django-allauth reusable module recipe.
- Added a documentation-only Django/django-allauth recipe covering email-first accounts, settings alignment, custom user model checks, account flows, email delivery, rate limits, and verification.
- Added Sprint 06 QA report with manual checks and verification evidence.
- Added Sprint 07 contract for a MindFlow AI content workbench frontend prototype.
- Added `frontend/` with Vite, React, TypeScript, lucide icons, Vitest, Testing Library, and a static AI creation workbench.
- Added mock UI workflows for hot topic selection, persona choice, image-text draft generation, Douyin/Weibo/Xiaohongshu previews, and schedule queue status.
- Updated `scripts/check.sh` so repository checks run frontend test, build, and lint.
- Added Sprint 07 QA report with automated and browser smoke verification evidence.
- Added Sprint 08 contract for PostgreSQL schema and AutoRepost integration boundary documentation.
- Added `docs/architecture/postgresql-schema.md` with the MVP schema for topics, personas, drafts, draft assets, platform accounts, platform previews, schedules, publish jobs, and publish job events.
- Added `docs/architecture/autorepost-integration.md` documenting AutoRepost as an external Weibo publishing adapter, not the MindFlow source of truth.
- Added the Sprint 08 design note under `docs/superpowers/specs/`.
- Added Sprint 08 QA report with documentation and verification evidence.
- Added Sprint 09 contract for a Python FastAPI backend skeleton and PostgreSQL migrations.
- Added `backend/` with FastAPI health endpoint, settings validation, SQLAlchemy metadata, Alembic configuration, and the initial PostgreSQL schema migration.
- Added backend tests covering health behavior, `DATABASE_URL` validation, schema table/constraint/index coverage, and Alembic offline SQL rendering.
- Updated `scripts/check.sh` so repository checks run backend compile, backend tests, and Alembic offline migration generation.
- Added `.env.example` guidance for `DATABASE_URL` without committing real credentials.
- Added Sprint 09 design note and QA report.
- Added Sprint 10 contract for database-backed backend product APIs.
- Added draft API routes for create, list, and detail reads.
- Added platform preview upsert API routes.
- Added schedule creation API that creates publish jobs for selected platforms with existing previews.
- Added SQLAlchemy session dependency and Pydantic request/response schemas.
- Added isolated backend API tests using a local SQLite test database while keeping PostgreSQL Alembic verification.
- Added Sprint 10 design note and QA report.

## Verification Evidence

- `./scripts/check.sh` passed for Sprint 10. Summary:

```text
[check] repository root: /Users/jie.feng/wlb/MindFlow
[check] frontend test
Test Files  1 passed (1)
Tests  3 passed (3)
[check] frontend build
vite v8.0.16 building client environment for production...
✓ built
[check] frontend lint
[check] backend compile
[check] backend tests
11 passed
[check] backend alembic offline migration
[check] done
```

- `git diff --check` passed.
- `rg -n "sprint-10|/api/drafts|platform_previews|publish_jobs|DATABASE_URL" backend docs scripts` confirmed the Sprint 10 API and persistence terms are present across code, docs, and scripts.

## Known Gaps

- The frontend is still a static prototype; it does not call the backend, PostgreSQL, OpenAI, or platform APIs.
- The backend has product APIs for drafts, platform previews, schedules, and publish jobs, but the frontend is not wired to them yet.
- The deployed PostgreSQL server is not connected yet; migrations were verified through Alembic offline SQL generation.
- AutoRepost is not migrated into MindFlow; it is intentionally documented as an external Weibo publishing adapter.
- Java checks are not active because the project does not contain Java application code.
- Reusable module choices still need to be rechecked at implementation time because auth/payment packages change quickly.

## Recommended Next Steps

1. Wire the frontend prototype away from mock-only state toward the Sprint 10 backend APIs.
2. Configure a safe deployed PostgreSQL environment outside the repository and apply migrations after credentials and backup expectations are confirmed.
3. Add the Weibo AutoRepost adapter only after persisted publish jobs exist in the deployed environment.
