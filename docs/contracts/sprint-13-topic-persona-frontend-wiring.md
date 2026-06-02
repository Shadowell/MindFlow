# Sprint 13 Contract: Frontend Topic and Persona API Wiring

## Goal

Wire the frontend hotspot and persona panels to the Sprint 12 backend APIs so the workbench no longer depends on static local topic/persona mock data.

## In Scope

- Add typed frontend API client methods for:
  - `GET /api/topics`
  - `GET /api/personas`
- Load topics and personas when the workbench opens.
- Render backend topics in the hotspot panel.
- Render backend active personas in the account persona panel.
- Use the selected backend persona when generating the local draft text.
- Show explicit loading, empty, and error states for topic/persona loading.
- Add frontend tests for topic/persona API loading and selection.
- Keep existing draft, preview, schedule, backend, and Alembic checks passing.
- Update product spec, progress, and QA report.

## Out of Scope

- Creating topics or personas from the frontend.
- Connecting deployed PostgreSQL.
- Adding real trend ingestion, AI generation, or platform scraping.
- Adding authentication, ownership, workspace membership, or permissions.
- Calling AutoRepost or any live platform API.
- Adding frontend fallback mock topic/persona data when the backend is unavailable.

## Deliverables

- Updated `frontend/src/api.ts`
- Updated `frontend/src/App.tsx`
- Updated `frontend/src/App.test.tsx`
- Any small CSS updates needed for loading/empty/error states
- Updated `docs/spec.md`
- Updated `docs/progress.md`
- `docs/superpowers/specs/2026-06-02-sprint-13-topic-persona-frontend-wiring-design.md`
- `docs/qa/sprint-13-topic-persona-frontend-wiring-report.md`

## Done Means

- The frontend calls `/api/topics` and `/api/personas` on load.
- API topics populate the hotspot buttons and clicking a topic fills the composer theme.
- API personas populate the persona buttons and the selected persona changes the composer voice.
- Missing or failed topic/persona responses are visible to the user instead of silently using local mock data.
- `./scripts/check.sh` passes.

## Verification

```bash
./scripts/check.sh
git diff --check
rg -n "sprint-13|listTopics|listPersonas|/api/topics|/api/personas" frontend docs
```

Manual or QA checks:

- Confirm no frontend static topic/persona fallback remains.
- Confirm topic/persona loading tests mock backend responses instead of local arrays.
- Confirm the page remains responsive and does not overlap on desktop or mobile.
- Confirm deployed PostgreSQL and AutoRepost remain out of runtime scope.

## Risks / Notes

- A fresh backend database can legitimately return empty topic/persona lists until records are created through API calls or a future admin/import flow.
- The draft body is still composed locally in the frontend; only the input data source moves to backend APIs in this sprint.

## Handoff

- Next likely step: add a backend draft-composition endpoint so frontend draft generation can move out of local template logic.
