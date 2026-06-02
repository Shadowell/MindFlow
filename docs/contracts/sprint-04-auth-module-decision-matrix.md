# Sprint 04 Contract: Auth Module Decision Matrix

## Goal

Add a compact authentication module decision matrix so future Codex sessions can choose a lightweight, stack-appropriate auth integration without defaulting to custom credential handling or enterprise IAM.

## In Scope

- Add a concise auth selection matrix to `docs/standards/reusable-modules.md`.
- Cover the existing lightweight recommendations: Supabase Auth, Better Auth, Auth.js, django-allauth, and FastAPI Users.
- Call out when to escalate to enterprise IAM or a custom implementation.
- Update product spec and progress handoff.
- Add a QA report for this documentation sprint.

## Out of Scope

- Adding application code, auth dependencies, environment variables, or provider configuration.
- Selecting a single auth provider for every future project.
- Writing stack-specific auth implementation recipes.
- Adding automated lint or CI enforcement for documentation guidance.
- Enterprise SSO, LDAP, SAML, or custom password/session-token design.

## Deliverables

- Updated `docs/standards/reusable-modules.md`.
- Updated `docs/spec.md` and `docs/progress.md`.
- `docs/qa/sprint-04-auth-module-decision-matrix-report.md`.

## Done Means

- A future Codex session can pick an auth starting point from a small decision matrix.
- The matrix preserves email-first authentication as the default for personal and small projects.
- Custom credential storage and enterprise IAM remain escalation paths, not defaults.
- Verification has been run through `./scripts/check.sh`.

## Verification

```bash
./scripts/check.sh
```

Manual or QA checks:

- Confirm the matrix maps common project stacks to lightweight auth choices.
- Confirm every recommendation requires checking current docs, maintenance, license, and fit at implementation time.
- Confirm custom auth and enterprise IAM are not presented as default choices.

## Risks / Notes

- Auth packages and hosted provider behavior change quickly, so project-specific implementation should recheck official docs and release health before dependency selection.
- The matrix is a selection aid only; it does not replace stack-specific implementation recipes.

## Handoff

- Next likely step: add stack-specific auth recipes after a real target stack is selected.
