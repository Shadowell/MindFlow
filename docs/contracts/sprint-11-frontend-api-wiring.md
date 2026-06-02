# Sprint 11 Contract: Frontend API Wiring

## Goal

Wire the MindFlow frontend workbench to the Sprint 10 backend APIs for the core creation workflow. The sprint should keep the current operational UI but persist generated drafts, platform previews, schedules, and publish jobs through HTTP calls instead of purely local mock state.

## In Scope

- Add a typed frontend API client for Sprint 10 endpoints:
  - `POST /api/drafts`
  - `GET /api/drafts`
  - `GET /api/drafts/{draft_id}`
  - `PUT /api/drafts/{draft_id}/platform-previews/{platform}`
  - `POST /api/drafts/{draft_id}/schedules`
- Update the React workbench so generating content creates a backend draft and platform previews.
- Update the schedule action so it creates a backend schedule and publish jobs.
- Show explicit loading and error states when backend calls are in progress or fail.
- Keep static hot topic, persona, and local draft-composition data where no backend API exists yet.
- Add frontend tests that prove the UI calls the backend API and renders persisted schedule/job state.
- Add Vite dev proxy configuration for `/api` to the local backend.
- Update product spec, progress, and QA report.

## Out of Scope

- Connecting to deployed PostgreSQL.
- Starting or configuring a production backend service.
- Adding backend topic, persona, AI generation, or asset APIs.
- Calling AutoRepost, OpenAI, Douyin, Weibo, or Xiaohongshu APIs.
- Adding authentication or account ownership.
- Changing the visual design direction beyond states required for API wiring.

## Deliverables

- `frontend/src/api.ts`
- Updated `frontend/src/App.tsx`
- Updated `frontend/src/App.test.tsx`
- Updated `frontend/vite.config.ts`
- Updated `docs/spec.md`
- Updated `docs/progress.md`
- `docs/superpowers/specs/2026-06-02-sprint-11-frontend-api-wiring-design.md`
- `docs/qa/sprint-11-frontend-api-wiring-report.md`

## Done Means

- Clicking `生成图文` creates a draft through the frontend API client.
- The frontend upserts platform previews for Douyin, Weibo, and Xiaohongshu after draft creation.
- Clicking `加入排期` creates a backend schedule and publish job for the selected platform.
- Backend failures are visible to the user as an error state.
- Frontend tests verify API requests and resulting UI state.
- `./scripts/check.sh` passes.

## Verification

```bash
./scripts/check.sh
git diff --check
rg -n "sprint-11|MindFlowApi|VITE_API_BASE_URL|/api/drafts|publish_jobs" frontend docs
```

Manual or QA checks:

- Confirm the frontend does not silently fall back to mock persistence if the backend fails.
- Confirm static mock data remains limited to topics, personas, and local content composition.
- Confirm no production API credentials or database URLs are committed.
- Confirm AutoRepost remains out of runtime scope.

## Risks / Notes

- The frontend can call backend APIs only when a backend process with a configured database is running.
- The backend still has no topic, persona, asset, or AI-generation endpoints, so those inputs remain static for now.

## Handoff

- Next likely step: configure a safe local/deployed backend runtime with PostgreSQL credentials outside the repository, then run an end-to-end browser smoke test against real persisted data.
