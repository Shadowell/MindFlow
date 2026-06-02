# QA Report: Sprint 06 Django django-allauth Recipe

## Sprint

`docs/contracts/sprint-06-django-allauth-recipe.md`

## Verdict

- `PASS`

## Scope Checked

- Django/django-allauth recipe exists under `docs/standards/recipes/`.
- Reusable module standard links to the recipe.
- Recipe is documentation-only and does not add application dependencies.
- Recipe preserves email-first authentication as the default.
- Recipe covers settings alignment, custom user model checks, account flows, email delivery, rate limits, session behavior, and verification.
- Progress handoff mentions Sprint 06.

## Evidence

- Commands run:

```bash
./scripts/check.sh
rg -n "django-allauth|email-first|password reset|protected views|signed-cookie|rate limits|Django admin|custom user model|CSRF|email backend" docs/standards/recipes/django-allauth.md docs/standards/reusable-modules.md docs/contracts/sprint-06-django-allauth-recipe.md
```

```text
[check] repository root: /Users/jie.feng/wlb/MindFlow
[check] done
```

- Manual checks:
  - Confirmed the recipe references official django-allauth quickstart, account introduction, account configuration, rate limits, email, advanced usage, and Django auth docs.
  - Confirmed the recipe says not to use signed-cookie sessions for allauth account flows.
  - Confirmed the recipe keeps social login, headless APIs, MFA, SSO, payments, and organization auth out of the default path.
  - Confirmed verification includes sign-up, email verification, sign-in, sign-out, password reset, protected views, Django admin login, user model linkage, email delivery, and rate limits.
  - Confirmed no Django app, package manifest, settings file, migration, email credential, or URL route was added.

## Findings

- Automated enforcement is intentionally not included because this template does not contain a Django application.

## Follow-Up Required

- Recheck django-allauth and Django official docs and package versions before using the recipe in a real implementation session.

## Notes For Next Sprint

- Add a Better Auth recipe when a TypeScript project with an owned database needs one.
