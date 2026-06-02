# Sprint 14 Contract: Backend Draft Composition API

## Goal

Add a backend draft-composition API that turns a persisted topic and active persona into a persisted draft plus platform previews. This moves the composition boundary out of the frontend without connecting AI yet.

## In Scope

- Add a FastAPI route for composing a draft from:
  - `topic_id`
  - `persona_id`
  - selected platforms
- Validate that the topic exists.
- Validate that the persona exists and is active.
- Persist the generated draft with `generation_source = "backend_template_composer"`.
- Persist platform previews for the selected platforms.
- Return the created draft and platform previews.
- Add Pydantic request/response schemas for the composition endpoint.
- Add isolated backend API tests using a local test database.
- Keep existing frontend, backend, and Alembic checks passing.
- Update product spec, progress, and QA report.

## Out of Scope

- Wiring the frontend generation button to this endpoint.
- Connecting OpenAI or any other AI provider.
- Connecting deployed PostgreSQL.
- Creating assets or image generation.
- Scheduling, publish job creation, or AutoRepost calls.
- Adding authentication, ownership, workspace membership, or permissions.

## Deliverables

- `backend/app/api/compositions.py`
- Updated `backend/app/main.py`
- Updated `backend/app/schemas.py`
- Backend tests for successful composition and inactive persona rejection.
- Updated `docs/spec.md`
- Updated `docs/progress.md`
- `docs/superpowers/specs/2026-06-02-sprint-14-backend-draft-composition-design.md`
- `docs/qa/sprint-14-backend-draft-composition-report.md`

## Done Means

- A caller can `POST /api/compositions/drafts` with a topic, persona, and platforms.
- The endpoint creates exactly one draft and one platform preview per selected platform.
- The response includes the created draft and previews.
- The endpoint rejects missing topics or inactive personas with explicit errors.
- `./scripts/check.sh` passes.

## Verification

```bash
./scripts/check.sh
git diff --check
rg -n "sprint-14|/api/compositions/drafts|DraftComposition|backend_template_composer" backend docs
```

Manual or QA checks:

- Confirm no AI provider, API key, or model setting is introduced.
- Confirm no deployed PostgreSQL credential is required.
- Confirm frontend generation remains unchanged for this sprint.
- Confirm AutoRepost remains out of runtime scope.

## Risks / Notes

- The composed copy is deterministic template output, intended as a backend contract placeholder for a future AI provider.
- The endpoint uses single-operator records until authentication or ownership is added later.

## Handoff

- Next likely step: wire the frontend `生成图文` action to `POST /api/compositions/drafts`.
