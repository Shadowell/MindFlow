# QA Report: Sprint 05 Next.js Supabase Auth Recipe

## Sprint

`docs/contracts/sprint-05-nextjs-supabase-auth-recipe.md`

## Verdict

- `PASS`

## Scope Checked

- Next.js/Supabase Auth recipe exists under `docs/standards/recipes/`.
- Reusable module standard links to the recipe.
- Recipe is documentation-only and does not add application dependencies.
- Recipe preserves email-first authentication as the default.
- Recipe covers server-side sessions, row-level security, local development, and implementation-time verification.
- Product spec and progress handoff mention stack recipes and Sprint 05.

## Evidence

- Commands run:

```bash
./scripts/check.sh
rg -n "Next.js Supabase Auth|server-side auth|row-level security|service-role|password reset|sign out|protected routes" docs/standards/recipes/nextjs-supabase-auth.md docs/standards/reusable-modules.md docs/contracts/sprint-05-nextjs-supabase-auth-recipe.md
```

```text
[check] repository root: /Users/jie.feng/wlb/MindFlow
[check] done
```

- Manual checks:
  - Confirmed the recipe references official Supabase Auth, Next.js quickstart, server-side auth, local development, and row-level security docs.
  - Confirmed the recipe says secret or service-role keys must stay server-only and out of client components.
  - Confirmed verification includes sign-up, email confirmation, sign-in, sign-out, password reset, protected routes, server-rendered session access, RLS behavior, secret-key exposure, and local development.
  - Confirmed no Next.js app, package manifest, environment file, or Supabase project configuration was added.

## Findings

- Automated enforcement is intentionally not included because this template does not contain a Next.js application.

## Follow-Up Required

- Recheck Supabase official docs and package versions before using the recipe in a real implementation session.

## Notes For Next Sprint

- Add a Django/django-allauth recipe or a Better Auth recipe when a real target stack needs it.
