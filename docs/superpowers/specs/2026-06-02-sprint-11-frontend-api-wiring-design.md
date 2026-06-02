# Sprint 11 Frontend API Wiring Design

## Context

Sprint 10 added backend APIs for drafts, platform previews, schedules, and publish jobs. The frontend still uses local state for the full creation workflow. Sprint 11 connects the existing workbench to those backend endpoints.

## Chosen Scope

The current UI remains a dense content-operations workbench. The sprint changes the workflow state, not the visual direction:

1. Topic and persona selection stay local because backend APIs for topics and personas do not exist yet.
2. `生成图文` still composes draft text locally, then persists the canonical draft through `POST /api/drafts`.
3. The frontend upserts platform previews for all three platforms through `PUT /api/drafts/{draft_id}/platform-previews/{platform}`.
4. `加入排期` calls `POST /api/drafts/{draft_id}/schedules` for the selected platform.
5. The right column shows returned schedule and publish job state.

## API Client

`frontend/src/api.ts` owns fetch calls and type definitions. It reads `VITE_API_BASE_URL`, defaulting to `/api`. It throws a clear error for non-2xx responses so the UI can render backend failures explicitly.

## UI State

The UI tracks:

- selected topic and persona
- locally composed draft text
- persisted draft id
- selected platform
- API loading state
- API error text
- latest schedule response

There is no silent mock fallback when backend persistence fails.

## Testing

Frontend tests mock `fetch` and verify:

- generation posts a draft and upserts platform previews
- schedule creation posts selected platform and renders returned publish job state
- failed backend calls show an error

Repository checks continue to run frontend tests, frontend build, frontend lint, backend tests, and Alembic offline migration rendering.

## Out of Scope

- Backend topics/personas APIs.
- Live PostgreSQL connection.
- Browser E2E with a running backend.
- AutoRepost or platform publishing.
