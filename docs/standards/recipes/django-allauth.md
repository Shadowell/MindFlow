# Recipe: Django django-allauth

## Purpose

Use this recipe when a personal, MVP, or small product uses Django and needs email-first registration, login, account management, and password reset without custom credential handling.

This recipe is documentation-only. It tells a future implementation session what to read, what to choose, and what to verify; it does not install dependencies or create application files in this template repository.

## Source Baseline

Recheck these official sources before implementation:

- [django-allauth documentation](https://docs.allauth.org/en/latest/)
- [django-allauth quickstart](https://docs.allauth.org/en/dev/installation/quickstart.html)
- [django-allauth regular accounts introduction](https://docs.allauth.org/en/latest/account/introduction.html)
- [django-allauth account configuration](https://docs.allauth.org/en/latest/account/configuration.html)
- [django-allauth account rate limits](https://docs.allauth.org/en/latest/account/rate_limits.html)
- [django-allauth sending email](https://docs.allauth.org/en/latest/common/email.html)
- [django-allauth advanced account usage](https://docs.allauth.org/en/latest/account/advanced.html)
- [Django authentication documentation](https://docs.djangoproject.com/en/stable/topics/auth/)

## Use This When

- The app is a server-rendered Django project or Django is the primary backend.
- Django's session authentication fits the product.
- Email/password sign-up, email verification, sign-in, sign-out, password reset, and account email management satisfy the first release.
- The product can use django-allauth's account views and templates, with light project-specific styling.

## Do Not Use This When

- The first release is a non-Django frontend that needs a dedicated headless auth API.
- The product already depends on an external identity provider for enterprise SSO, LDAP, SAML, or centralized identity.
- The project uses a custom user model that has not been designed before migrations are created.
- The requirement is only Django admin access; Django's built-in auth may be enough.

## Recommended Starting Path

For a new Django project, decide on the user model before the first migration. If the project wants email as the visible account identifier and does not need usernames, align django-allauth with that choice instead of collecting a username by default.

For an existing Django project, inspect the current `AUTH_USER_MODEL`, installed apps, authentication backends, middleware, URL routing, templates, email backend, and session engine before adding django-allauth.

Start with regular `allauth.account` support. Add social providers, MFA, user sessions, or headless APIs only when the product has a verified need for them.

## Implementation Checkpoints

1. Confirm the stack.
   - Django version and supported Python version.
   - Current `AUTH_USER_MODEL` and whether migrations already exist.
   - Whether the app is server-rendered Django, Django REST, or a hybrid.

2. Install the smallest needed package.
   - Use `django-allauth` for regular email/password accounts.
   - Use optional extras only when social providers or headless APIs are in scope.
   - Record the exact package version chosen during implementation.

3. Wire Django settings deliberately.
   - Add the required `allauth` and `allauth.account` apps.
   - Keep Django's model backend so Django admin login still works.
   - Add allauth's authentication backend for account login.
   - Add allauth account middleware if current docs require it.
   - Include `allauth.urls` under a predictable account path.
   - Do not use signed-cookie sessions for allauth account flows, because account secrets can be stored in the session.

4. Configure email-first accounts.
   - Set the login method to email when the product uses email-first accounts.
   - Align sign-up fields with the login method.
   - Require email when it is the account identifier.
   - Decide whether users must verify email before sign-in.
   - Keep uniqueness and case-handling decisions explicit.

5. Configure account flows.
   - Confirm sign-up, login, logout, password reset, password change, and email management routes.
   - Configure redirect URLs for login, logout, sign-up, email confirmation, and password reset.
   - Keep state-changing logout or confirmation behavior aligned with current allauth guidance.
   - Keep onboarding state in application tables, not in allauth internals.

6. Configure email delivery.
   - Use a real email backend in staging and production.
   - Keep provider credentials in environment variables.
   - Customize email templates only after the default flow works.
   - Verify password-reset and confirmation emails render correctly in text and HTML when both are provided.

7. Keep product authorization outside account plumbing.
   - Link product profile data to the Django user model.
   - Add roles only when the product has real permission levels.
   - Use Django permissions, groups, or a small project-owned role field before building a custom RBAC matrix.
   - Do not use unverified email addresses as authorization proof.

8. Preserve security defaults.
   - Keep rate limits enabled unless there is a written reason to change them.
   - Do not implement custom password hashing, reset tokens, email confirmation tokens, or session formats.
   - Protect Django admin login separately from public allauth views.
   - Use CSRF protection on form-based flows.

## Verification

Run the project-specific checks, then manually verify:

- A new user can sign up with email and password.
- Email verification works when enabled.
- The user can sign in with the configured login method.
- The user can sign out without using a state-changing GET flow unless the project explicitly accepted that risk.
- Password reset sends an email and completes through the configured route.
- Password change works for an authenticated user.
- Protected views reject anonymous users.
- Django admin login still works for staff users.
- User profile data links to the configured user model.
- Existing migrations are not broken by auth model assumptions.
- Account emails are sent through the intended backend in staging or production.
- Rate limits remain enabled for login, failed login, sign-up, password reset, and email confirmation actions unless explicitly changed.

## Handoff Notes

- Record the exact django-allauth and Django docs used during implementation.
- Record the package version and selected optional extras.
- Document account-related settings by name and purpose.
- Document every custom template and adapter override.
- Document how staff/admin login is protected if the public login flow changes.
