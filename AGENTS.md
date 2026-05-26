# AGENTS.md

## Purpose

This repository uses Codex as a delivery partner. Codex should work incrementally, keep project state in files, and avoid treating the chat history as the only source of truth.

## Files To Read First

Before substantial work, read:

1. `README.md`
2. `docs/spec.md`
3. `docs/progress.md`
4. the active contract under `docs/contracts/`

When work touches a specific technology area, also read the relevant standard before planning or editing:

- Python: `docs/standards/python.md`
- Java: `docs/standards/java.md`
- Database schema, migrations, queries, or persistence: `docs/standards/database.md`
- Frontend UI, web apps, or browser behavior: `docs/standards/frontend.md`
- Common modules such as authentication, user management, payments, subscriptions, admin panels, email, file uploads, or notifications: `docs/standards/reusable-modules.md`

## Operating Rules

1. Work only within the current sprint contract unless explicitly told to expand scope.
2. Prefer small, reviewable changes over broad rewrites.
3. Update `docs/progress.md` after each meaningful implementation step.
4. Do not call work done without running the relevant checks, or clearly documenting what was not checked.
5. If requirements, architecture, or API contracts change, update `docs/spec.md` and the active contract in the same change.
6. Do not add fallback behavior, compatibility layers, mocks, or silent error handling unless the user explicitly requests it.
7. Match database design complexity to the project's actual scale. Avoid sharding, CQRS, denormalized read models, or other large-system patterns without evidence and explicit approval.
8. For personal or small projects, prefer mature lightweight integrations for commodity modules. Email registration/login should be the default authentication path unless the user asks for another flow.

## Standard Loop

Use this delivery loop for non-trivial tasks:

1. Read the current project state.
2. Select or create a sprint contract.
3. Implement only that slice.
4. Run verification.
5. Record QA findings if needed.
6. Update progress and next step.

## Done Criteria

A sprint is done only when:

- the agreed scope is implemented
- verification has been run or explicitly deferred
- known gaps are documented
- the repository is left in a coherent state for the next session

## Verification

Preferred entrypoint:

```bash
./scripts/check.sh
```

If project-specific commands exist, add them to `scripts/check.sh`.

## When To Pause

Pause and ask for confirmation when:

- the change affects security, billing, or production data
- the task requires a cross-cutting rewrite
- the current contract conflicts with the new request
- success criteria are too vague to verify
