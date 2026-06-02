# QA Report: Sprint 11 Frontend API Wiring

## Scope

Sprint 11 verifies that the frontend workbench uses Sprint 10 backend APIs for draft creation, platform preview persistence, schedule creation, and publish job display.

## Result

PASS

## Automated Checks

```bash
./scripts/check.sh
git diff --check
rg -n "sprint-11|MindFlowApi|VITE_API_BASE_URL|/api/drafts|publish_jobs" frontend docs
```

Expected repository check coverage:

- Frontend tests, build, and lint pass.
- Backend Python sources compile.
- Backend pytest suite passes.
- Alembic still renders the PostgreSQL migration offline.

## Manual Checks

- Confirmed `生成图文` calls `POST /api/drafts` and platform preview upsert endpoints in frontend tests.
- Confirmed `加入排期` calls `POST /api/drafts/{draft_id}/schedules` in frontend tests.
- Confirmed backend failures render an explicit `role="alert"` error state.
- Confirmed the frontend does not silently fall back to mock persistence.
- Confirmed no production database URL, platform credential, or AutoRepost runtime call was added.
- Browser smoke with Vite on `127.0.0.1:5173` confirmed the first screen renders and backend failure appears as a visible alert when no backend is running.

## Findings

No blocking findings.

## Known Gaps

- The frontend still depends on static local topics, personas, and draft text composition.
- A running backend with a configured database is required for real browser persistence.
- The deployed PostgreSQL server has not received migrations.
- AutoRepost and live platform publishing remain out of scope.

## Handoff

Next sprint should configure safe PostgreSQL runtime/deployment handling or add backend APIs for topics, personas, assets, and AI generation.
