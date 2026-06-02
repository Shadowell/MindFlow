# QA Report: Sprint 15 Frontend Composition Wiring

## Scope

Sprint 15 verifies that the frontend generation action calls the backend composition endpoint instead of composing draft text locally.

## Result

PASS

## Automated Checks

```bash
npm run test
./scripts/check.sh
git diff --check
rg -n "sprint-15|composeDraft|/api/compositions/drafts|backend_template_composer" frontend docs
```

Expected repository check coverage:

- Frontend tests, build, and lint pass.
- Backend Python sources compile.
- Backend pytest suite passes.
- Alembic still renders the PostgreSQL migration offline.

## Manual Checks

- Confirmed frontend tests require `POST /api/compositions/drafts` during generation.
- Confirmed the composition payload includes selected `topic_id`, `persona_id`, and all supported platforms.
- Confirmed the editor displays backend-composed draft text from the response.
- Confirmed the platform preview panel can display backend-returned platform preview data.
- Confirmed schedule creation still uses the returned persisted draft id.
- Confirmed no local frontend template composer, AI provider, API key, deployed PostgreSQL credential, platform credential, or AutoRepost runtime call was added.
- Browser smoke with Vite on `127.0.0.1:5173` confirmed the workbench renders responsive panels and explicit backend loading errors when no backend is running.

## Findings

No blocking findings.

## Known Gaps

- The backend composition result is deterministic template output, not provider-backed AI generation.
- A fresh backend database still needs topics and personas created before frontend generation can run.
- The deployed PostgreSQL server has not received migrations.
- AutoRepost remains documented as an external Weibo adapter, not a runtime dependency.

## Handoff

Next work needs either safe deployed PostgreSQL environment details or an explicit AI provider/prompt contract decision.
