# Sprint 12 Contract: Topic and Persona APIs

## Goal

Add backend APIs for MindFlow's editorial topics and persona templates so the remaining static frontend inputs have a persisted backend surface ready for future wiring.

## In Scope

- Add FastAPI routes for:
  - creating topics
  - listing topics by newest discovered time
  - creating personas
  - listing active personas
- Add Pydantic request/response schemas for topics and personas.
- Add isolated backend API tests using a local test database setup.
- Keep existing draft, preview, schedule, publish job, frontend, and Alembic checks passing.
- Update product spec, progress, and QA report.

## Out of Scope

- Wiring the frontend left column to topic/persona APIs.
- Connecting to deployed PostgreSQL.
- Adding real trend ingestion, AI generation, or platform scraping.
- Adding authentication, ownership, or workspace membership.
- Adding destructive delete endpoints.
- Calling AutoRepost or any live platform API.

## Deliverables

- `backend/app/api/content_inputs.py`
- Updated `backend/app/schemas.py`
- Backend tests for topic and persona API behavior.
- Updated `docs/spec.md`
- Updated `docs/progress.md`
- `docs/superpowers/specs/2026-06-02-sprint-12-topic-persona-apis-design.md`
- `docs/qa/sprint-12-topic-persona-apis-report.md`

## Done Means

- A caller can create and list topics through the API.
- A caller can create and list active personas through the API.
- Tests prove topic/persona API persistence through SQLAlchemy instead of frontend mock state.
- `./scripts/check.sh` passes.

## Verification

```bash
./scripts/check.sh
git diff --check
rg -n "sprint-12|/api/topics|/api/personas|TopicResponse|PersonaResponse" backend docs
```

Manual or QA checks:

- Confirm API tests do not require the user's deployed PostgreSQL server.
- Confirm no production credentials are committed.
- Confirm frontend wiring remains out of scope for this sprint.
- Confirm AutoRepost remains out of runtime scope.

## Risks / Notes

- Topics and personas are single-operator records until authentication or ownership is added later.
- These APIs do not ingest real platform trend data; they support manual or future upstream writes.

## Handoff

- Next likely step: wire the frontend hotspot and persona panels to these APIs, then add a backend draft-composition endpoint.
