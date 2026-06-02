# Sprint 05 Contract: Next.js Supabase Auth Recipe

## Goal

Add the first stack-specific reusable module recipe for a small Next.js application using Supabase Auth, so future Codex sessions can integrate email-first authentication from official guidance without inventing credential or session handling.

## In Scope

- Create a concise recipe under `docs/standards/recipes/`.
- Cover when the recipe applies and when it does not.
- Document the recommended Supabase starting path for a new Next.js App Router project.
- Document implementation checkpoints for email/password auth, server-side session handling, row-level security, local development, and verification.
- Link the recipe from `docs/standards/reusable-modules.md`.
- Update product spec and progress handoff.
- Add a QA report for this documentation sprint.

## Out of Scope

- Creating a Next.js app in this repository.
- Installing Supabase, Next.js, or npm dependencies.
- Adding real Supabase project keys, environment variables, migrations, or database policies.
- Implementing social login, SSO, MFA, payments, or organization auth.
- Replacing project-specific security review or threat modeling.

## Deliverables

- `docs/standards/recipes/nextjs-supabase-auth.md`
- Updated `docs/standards/reusable-modules.md`
- Updated `docs/spec.md` and `docs/progress.md`
- `docs/qa/sprint-05-nextjs-supabase-auth-recipe-report.md`

## Done Means

- A future Codex session has a clear Next.js/Supabase auth recipe to read after the reusable module matrix points to Supabase Auth.
- The recipe preserves email-first authentication as the default.
- The recipe requires official docs and current package behavior to be rechecked before implementation.
- Verification has been run through `./scripts/check.sh`.

## Verification

```bash
./scripts/check.sh
```

Manual or QA checks:

- Confirm the recipe is documentation-only and does not add app dependencies.
- Confirm the recipe uses official Supabase docs as its source baseline.
- Confirm the recipe includes verification for sign-up, sign-in, sign-out, password reset, protected routes, RLS behavior, and local development.
- Confirm secrets and service-role keys are not placed in client-side guidance.

## Risks / Notes

- Supabase Auth and Next.js server-side integration details can change, so implementation sessions must recheck official docs and package versions.
- `@supabase/ssr` has historically carried beta or unstable API notes; the recipe should treat it as a current-docs dependency, not a frozen abstraction.

## Handoff

- Next likely step: add a Django/django-allauth recipe or a Better Auth recipe after a real target stack asks for it.
