# Reusable Module Integration Standard

## Purpose

Use this standard before implementing common product modules such as authentication, user management, payments, subscriptions, admin panels, email delivery, file uploads, and notifications.

For personal projects, MVPs, and small products, prefer integrating mature lightweight modules over generating custom commodity code. The goal is to save implementation time and token budget while reducing security and maintenance risk.

## Source Baseline

- [Supabase Auth: password-based auth](https://supabase.com/docs/guides/auth/passwords)
- [Supabase Auth overview](https://supabase.com/docs/guides/auth/)
- [Better Auth: basic usage](https://better-auth.com/docs/basic-usage)
- [Better Auth: email](https://better-auth.com/docs/concepts/email)
- [Auth.js documentation](https://authjs.dev/)
- [django-allauth documentation](https://docs.allauth.org/)
- [FastAPI Users documentation](https://fastapi-users.github.io/fastapi-users/)
- [FastAPI Users repository](https://github.com/fastapi-users/fastapi-users)
- [Stripe samples](https://docs.stripe.com/samples)
- [Stripe Checkout](https://stripe.com/payments/checkout)
- [Stripe Billing customer portal](https://docs.stripe.com/billing/subscriptions/customer-portal)
- [OWASP Cheat Sheet Series](https://owasp.org/www-project-cheat-sheets/)

## Default Decision Rule

Do not hand-roll common modules unless the user explicitly asks for custom implementation or the integration cannot satisfy the verified requirement.

Preferred order:

1. Official SDK, hosted component, or official sample.
2. Mature open-source library with active maintenance and clear documentation.
3. Small stack-specific boilerplate used as reference, not blindly copied.
4. Custom code only for the business-specific layer around the integration.

## Stack Recipes

Read these recipes only when their stack matches the project:

- [Django django-allauth](recipes/django-allauth.md)
- [Next.js Supabase Auth](recipes/nextjs-supabase-auth.md)

## Lightweight Project Defaults

Use these defaults for individual developers, personal products, small SaaS projects, internal tools, and early MVPs.

### Authentication

Default authentication should be email-first:

- Email and password.
- Email verification when the module supports it.
- Password reset flow.
- Optional magic link or one-time password if it reduces friction.
- Optional social login only after email login works.

Read this decision matrix before choosing an auth module. It is a selection aid, not a stack-specific recipe.

| Project shape | Default starting point | Use when | Check before implementation |
| --- | --- | --- | --- |
| Supabase-backed app | Supabase Auth | The project already uses Supabase database, edge functions, or hosted auth is acceptable. | Email verification settings, redirect URLs, row-level security policies, local development flow, and what user data leaves the app. |
| TypeScript or Next.js app with an owned database | Better Auth | The app wants email/password, verification, password reset, sessions, and database ownership without adopting a larger IAM product. | Current adapter support, migrations, email provider setup, `baseURL` configuration, and session storage behavior. |
| Next.js app with simple OAuth or session needs | Auth.js | Provider login and framework-level session integration matter more than owning a full email/password module. | Current App Router support, adapter compatibility, callback behavior, credentials-provider fit, and runtime constraints. |
| Django app | django-allauth | The project already uses Django and can build on Django's auth conventions. | Email backend, account settings, social provider configuration, custom user model compatibility, and admin workflow. |
| FastAPI API | FastAPI Users | The project needs ready-made user routes and accepts a stable maintenance-mode library. | Maintenance-mode status, database backend, cookie versus bearer transport, password reset and verification routes, and OpenAPI exposure. |
| Multiple apps or enterprise identity | Keycloak or external IdP | The product already requires SSO, OIDC/SAML, centralized identity, or directory integration. | Operational ownership, backup and upgrade path, IdP availability, tenant model, and support burden. |
| Requirement cannot be met by a mature module | Custom business-specific layer only | The unique requirement sits around auth, not inside password hashing, session tokens, or reset-token design. | Written approval, threat model, OWASP guidance, test plan, and why existing modules cannot satisfy the requirement. |

When two lightweight choices fit, pick the one that removes the most moving parts from the current stack. If Supabase is already the backend, Supabase Auth usually wins. If the app owns its database and is TypeScript-first, Better Auth is usually the first candidate. If the stack is Django, prefer django-allauth before introducing a cross-stack auth service.

Avoid by default:

- Custom password storage.
- Custom session token formats.
- Custom email verification and reset token design.
- Enterprise SSO as the first implementation.
- Multi-tenant organization auth unless the product already needs organizations.

### User Management

For small projects, user management should start minimal:

- User profile table or model linked to the auth user.
- Basic account page for email, display name, and password reset.
- Admin-only user lookup if truly needed.
- Role field only when the product has at least two real permission levels.

Avoid by default:

- Full RBAC matrices.
- User impersonation.
- Organization hierarchies.
- Audit systems beyond the actual compliance or debugging need.

### Payments

Default payment integration should use hosted or official flows:

- Stripe Checkout for payment collection.
- Stripe Customer Portal for subscription management.
- Stripe webhooks for confirmed payment and subscription state.
- Store only the local state needed for product access.

Recommended starting points:

- Official Stripe samples for one-time payments and subscriptions.
- Stripe Checkout and Customer Portal before building custom payment UI.

Avoid by default:

- Custom card collection UI.
- Hand-written subscription state machines.
- Complex billing platforms such as Lago or Kill Bill unless pricing is usage-based, invoice-heavy, or operationally complex.
- Treating an archived SaaS boilerplate as a default dependency.

## Escalation Paths

Use heavier modules only when the project has matching requirements.

- Keycloak: use for enterprise SSO, multiple applications, OIDC/SAML, LDAP/AD, or centralized identity.
- Directus, AdminJS, or Strapi: use when the project needs a real back-office UI or content/data management.
- Lago or Kill Bill: use when billing involves usage metering, invoices, multiple products, complex pricing, or finance operations.

These are escalation paths, not defaults for personal projects.

## Selection Checklist

Before choosing a reusable module, record:

- Target stack and runtime.
- Required flow: email/password, magic link, subscription, admin user lookup, etc.
- Maintenance status and latest release health.
- License and self-hosting constraints.
- Data ownership and vendor lock-in risk.
- Required environment variables and secrets.
- Webhook or callback URLs.
- Local development story.
- Verification path.

## Implementation Rules

1. Integrate the smallest module that satisfies the current requirement.
2. Keep business rules outside the vendor integration when possible.
3. Keep secrets in environment variables, never in source files.
4. Add webhook handlers only for events the product actually consumes.
5. Do not add fallback auth, mock payment success, or silently ignore provider errors without explicit user approval.
6. If the module is archived, deprecated, or in maintenance mode, document that fact before using it.
7. If the module stores user or payment data externally, document what data leaves the application.

## Verification

For auth:

- Sign up with email.
- Verify email if enabled.
- Sign in.
- Sign out.
- Reset password.
- Confirm protected routes reject unauthenticated users.

For payments:

- Create checkout session in test mode.
- Complete test payment.
- Receive and verify webhook signature.
- Update local access state only after trusted provider confirmation.
- Open customer portal when subscriptions are supported.

For admin/user management:

- Confirm non-admin users cannot access admin operations.
- Confirm admin actions are visible and reversible where appropriate.
