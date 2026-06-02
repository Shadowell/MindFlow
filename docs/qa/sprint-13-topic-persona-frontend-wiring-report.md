# QA Report: Sprint 13 Frontend Topic and Persona API Wiring

## Scope

Sprint 13 verifies that the MindFlow frontend loads hotspot topics and persona templates from Sprint 12 backend APIs instead of static local mock data.

## Result

PASS

## Automated Checks

```bash
npm run test
./scripts/check.sh
git diff --check
rg -n "sprint-13|listTopics|listPersonas|/api/topics|/api/personas" frontend docs
```

Expected repository check coverage:

- Frontend tests, build, and lint pass.
- Backend Python sources compile.
- Backend pytest suite passes.
- Alembic still renders the PostgreSQL migration offline.

## Manual Checks

- Confirmed frontend tests mock `GET /api/topics` and `GET /api/personas` before generation and schedule flows.
- Confirmed backend topics populate hotspot buttons and clicking a topic fills the composer theme.
- Confirmed backend personas populate the persona panel and selected persona tone appears in the workbench.
- Confirmed static frontend topic/persona fallback arrays were removed from runtime.
- Confirmed explicit loading, empty, and error states exist for topic/persona loading.
- Confirmed no deployed PostgreSQL credential, platform credential, or AutoRepost runtime call was added.
- Browser smoke with Vite on `127.0.0.1:5173` confirmed the workbench renders and shows explicit backend topic/persona loading errors when no backend is running.

## Findings

No blocking findings.

## Known Gaps

- Draft text is still composed by local frontend template logic.
- A fresh backend database needs topics and personas created before the input panels show selectable records.
- The deployed PostgreSQL server has not received migrations.
- Real trend ingestion, AI draft generation, and live platform publishing remain out of scope.

## Handoff

Next sprint should add a backend draft-composition endpoint, then wire the frontend generation action to that endpoint.
