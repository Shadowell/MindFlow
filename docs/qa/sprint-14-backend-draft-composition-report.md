# QA Report: Sprint 14 Backend Draft Composition

## Scope

Sprint 14 verifies that the backend can compose a deterministic draft and platform previews from a persisted topic and active persona.

## Result

PASS

## Automated Checks

```bash
PYTHONPATH=. python3 -m pytest tests/test_draft_composition_api.py -q
./scripts/check.sh
git diff --check
rg -n "sprint-14|/api/compositions/drafts|DraftComposition|backend_template_composer" backend docs
```

Expected repository check coverage:

- Frontend tests, build, and lint pass.
- Backend Python sources compile.
- Backend pytest suite passes, including the new composition API tests.
- Alembic still renders the PostgreSQL migration offline.

## Manual Checks

- Confirmed the composition test creates a topic and active persona through existing APIs before composing.
- Confirmed `POST /api/compositions/drafts` creates a persisted draft with `generation_source = "backend_template_composer"`.
- Confirmed the endpoint creates one platform preview for each selected platform.
- Confirmed inactive personas are rejected with an explicit `Active persona not found` error.
- Confirmed no AI provider, API key, deployed PostgreSQL credential, platform credential, or AutoRepost runtime call was added.
- Confirmed frontend generation remains unchanged for this sprint.

## Findings

No blocking findings.

## Known Gaps

- Frontend `生成图文` still uses local composition logic.
- The backend composer is deterministic template output, not AI generation.
- A fresh backend database still needs topics and personas created before composition can run.
- The deployed PostgreSQL server has not received migrations.

## Handoff

Next sprint should wire the frontend generation action to `POST /api/compositions/drafts`, then continue toward provider-backed AI composition.
