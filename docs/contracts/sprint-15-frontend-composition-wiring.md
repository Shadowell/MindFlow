# Sprint 15 Contract: Frontend Composition API Wiring

## Goal

Wire the frontend `生成图文` action to the Sprint 14 backend composition endpoint so draft creation no longer uses local frontend template logic.

## In Scope

- Add typed frontend API client coverage for `POST /api/compositions/drafts`.
- Track the selected backend topic id in the workbench.
- Require a selected backend topic and active persona before generation.
- Replace local draft body/title/tag composition with `MindFlowApi.composeDraft`.
- Use the returned draft as the editor content and persisted draft id.
- Use the returned platform previews in the platform preview panel after generation.
- Keep schedule creation working with the draft created by the composition endpoint.
- Add frontend tests proving composition endpoint usage and backend error handling.
- Keep existing backend, frontend, and Alembic checks passing.
- Update product spec, progress, and QA report.

## Out of Scope

- Changing the backend composition endpoint.
- Connecting OpenAI or any other AI provider.
- Connecting deployed PostgreSQL.
- Creating or editing topics/personas from the frontend.
- Creating assets or image generation.
- Calling AutoRepost or any live platform API.

## Deliverables

- Updated `frontend/src/api.ts`
- Updated `frontend/src/App.tsx`
- Updated `frontend/src/App.test.tsx`
- Any small CSS updates needed for generated preview display
- Updated `docs/spec.md`
- Updated `docs/progress.md`
- `docs/superpowers/specs/2026-06-02-sprint-15-frontend-composition-wiring-design.md`
- `docs/qa/sprint-15-frontend-composition-wiring-report.md`

## Done Means

- Clicking `生成图文` calls `POST /api/compositions/drafts`.
- The request includes the selected `topic_id`, `persona_id`, and all supported platforms.
- The editor displays the backend-composed draft.
- The preview panel can display backend-returned platform previews.
- The old local template composer is removed from runtime.
- `./scripts/check.sh` passes.

## Verification

```bash
./scripts/check.sh
git diff --check
rg -n "sprint-15|composeDraft|/api/compositions/drafts|backend_template_composer" frontend docs
```

Manual or QA checks:

- Confirm no frontend fallback local composer remains.
- Confirm generation is disabled or errors clearly when no backend topic/persona is selected.
- Confirm desktop and mobile layouts remain usable.
- Confirm deployed PostgreSQL, AI providers, and AutoRepost remain out of runtime scope.

## Risks / Notes

- Users need at least one backend topic and one active backend persona before the generation button can run.
- The backend composition result is still deterministic template output, not provider-backed AI.

## Handoff

- Next likely step: configure safe deployed PostgreSQL runtime handling, or introduce provider-backed AI composition behind the backend composition boundary.
