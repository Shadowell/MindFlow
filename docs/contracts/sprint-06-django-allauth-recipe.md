# Sprint 06 Contract: Django django-allauth Recipe

## Goal

Add a stack-specific reusable module recipe for a small Django application using django-allauth, so future Codex sessions can implement email-first account registration and login without custom credential, token, or password-reset handling.

## In Scope

- Create a concise recipe under `docs/standards/recipes/`.
- Cover when the recipe applies and when it does not.
- Document the recommended django-allauth starting path for a server-rendered Django project.
- Document implementation checkpoints for email/password auth, email verification, password reset, session behavior, custom user model alignment, rate limits, email delivery, and verification.
- Link the recipe from `docs/standards/reusable-modules.md`.
- Update product spec and progress handoff.
- Add a QA report for this documentation sprint.

## Out of Scope

- Creating a Django project in this repository.
- Installing django-allauth or Python dependencies.
- Adding real settings, migrations, email backend credentials, or URL routes.
- Implementing social login, headless APIs, MFA, SSO, payments, or organization auth.
- Replacing project-specific security review or threat modeling.

## Deliverables

- `docs/standards/recipes/django-allauth.md`
- Updated `docs/standards/reusable-modules.md`
- Updated `docs/spec.md` and `docs/progress.md`
- `docs/qa/sprint-06-django-allauth-recipe-report.md`

## Done Means

- A future Codex session has a clear Django/django-allauth recipe to read after the reusable module matrix points to django-allauth.
- The recipe preserves email-first authentication as the default.
- The recipe requires official docs and current package behavior to be rechecked before implementation.
- Verification has been run through `./scripts/check.sh`.

## Verification

```bash
./scripts/check.sh
```

Manual or QA checks:

- Confirm the recipe is documentation-only and does not add app dependencies.
- Confirm the recipe uses official django-allauth and Django docs as its source baseline.
- Confirm the recipe includes verification for sign-up, email verification, sign-in, sign-out, password reset, protected views, session behavior, and email delivery.
- Confirm custom password storage, custom reset-token handling, and signed-cookie session storage are not recommended.

## Risks / Notes

- django-allauth configuration names and supported Django/Python versions can change, so implementation sessions must recheck official docs and package versions.
- Headless django-allauth and social providers are useful escalation paths, but they are not defaults for this recipe.

## Handoff

- Next likely step: add a Better Auth recipe when a TypeScript project with an owned database asks for it.
