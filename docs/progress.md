# Progress Log

## Current Baseline

- Branch: `main`
- Harness status: `active`
- Last verified state: `Sprint 08 PostgreSQL schema and AutoRepost boundary verified with ./scripts/check.sh`

## Active Contract

- `docs/contracts/sprint-08-postgresql-schema-and-autorepost-boundary.md`

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

## Verification Evidence

- `./scripts/check.sh` passed for Sprint 08. Summary:

```text
[check] repository root: /Users/jie.feng/wlb/MindFlow
[check] frontend test
Test Files  1 passed (1)
Tests  3 passed (3)
[check] frontend build
vite v8.0.16 building client environment for production...
✓ built
[check] frontend lint
[check] done
```

- `git diff --check` passed.
- `rg -n "publish_jobs|platform_previews|AutoRepost|legacy_task_id|PostgreSQL" ...` confirmed the Sprint 08 schema and integration terms are present across spec, progress, architecture, contract, and QA docs.

## Known Gaps

- The frontend is still a static prototype; it does not connect to PostgreSQL, OpenAI, or platform APIs.
- PostgreSQL migrations and backend APIs are not implemented yet; Sprint 08 is documentation-only.
- AutoRepost is not migrated into MindFlow; it is intentionally documented as an external Weibo publishing adapter.
- Java, Python, and database checks are not yet active because those application areas do not contain code yet.
- Reusable module choices still need to be rechecked at implementation time because auth/payment packages change quickly.

## Recommended Next Steps

1. Choose the backend stack and implement migrations for the Sprint 08 PostgreSQL schema.
2. Add draft, platform preview, schedule, and publish job APIs that the frontend can call.
3. Add the Weibo AutoRepost adapter only after persisted publish jobs exist.
