# Sprint 03 Contract: Lightweight Reusable Modules

## Goal

Add guidance for integrating mature, lightweight reusable modules in personal or small projects, especially email-first authentication, user management, and simple payments, so Codex does not spend unnecessary tokens generating fragile commodity code.

## In Scope

- Add a reusable module selection standard.
- Prioritize personal/small-project needs over enterprise IAM.
- Prefer email registration/login as the default authentication path.
- Define when to use mature integrations versus custom implementation.
- Update project rules and progress handoff.

## Out of Scope

- Adding any concrete authentication, payment, or admin dependency to this template.
- Building a reusable module registry with automated checks.
- Enterprise SSO, LDAP, SAML, sharding, or complex billing implementation.

## Deliverables

- `docs/standards/reusable-modules.md`
- Updated `AGENTS.md`, `docs/spec.md`, `docs/progress.md`, and README references.
- QA report for the sprint.

## Done Means

- Future Codex sessions know to prefer lightweight integrations for common modules.
- Email-first authentication is documented as the default for personal/small projects.
- Heavy enterprise options are documented as escalation paths, not defaults.
- Verification has been run through `./scripts/check.sh`.

## Verification

```bash
./scripts/check.sh
```

Manual or QA checks:

- Confirm guidance favors small-project integration over custom auth/payment code.
- Confirm enterprise IAM and complex billing are not default recommendations.

## Risks / Notes

- Actual module choice still depends on the selected project stack and license requirements.
- Current source links should be rechecked before implementation because auth/payment packages change quickly.

## Handoff

- Next likely step: add stack-specific reusable module recipes after the first real project chooses its stack.
