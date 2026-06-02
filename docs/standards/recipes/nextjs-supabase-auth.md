# Recipe: Next.js Supabase Auth

## Purpose

Use this recipe when a personal, MVP, or small product uses Next.js and Supabase, and needs email-first authentication without custom credential or session handling.

This recipe is documentation-only. It tells a future implementation session what to read, what to choose, and what to verify; it does not install dependencies or create application files in this template repository.

## Source Baseline

Recheck these official sources before implementation:

- [Supabase Auth overview](https://supabase.com/docs/guides/auth/)
- [Supabase Auth password-based auth](https://supabase.com/docs/guides/auth/passwords)
- [Use Supabase Auth with Next.js](https://supabase.com/docs/guides/auth/quickstarts/nextjs)
- [Supabase server-side auth](https://supabase.com/docs/guides/auth/server-side)
- [Supabase local development](https://supabase.com/docs/guides/local-development)
- [Supabase row-level security](https://supabase.com/docs/guides/database/postgres/row-level-security)

## Use This When

- The app is a Next.js App Router project or is willing to follow the current Supabase App Router guidance.
- Supabase is already the database or hosted auth provider.
- Email/password sign-up, email verification, sign-in, sign-out, and password reset satisfy the first release.
- User-owned rows can be protected with Supabase row-level security policies.

## Do Not Use This When

- The app must own all auth data and cannot use Supabase-hosted Auth.
- The first release requires enterprise SSO, LDAP, SAML, or centralized identity across multiple applications.
- The product needs complex organization auth before it has a real organization model.
- The project is not using Supabase for data or auth; use the decision matrix in `docs/standards/reusable-modules.md` again.

## Recommended Starting Path

For a new Next.js project, prefer Supabase's current `with-supabase` Next.js template because it starts from the official App Router path and includes cookie-based auth wiring.

For an existing Next.js project, follow the current server-side auth docs instead of copying stale snippets. Create distinct browser and server Supabase clients using the current Supabase package guidance, keep sessions in cookies for server-rendered routes, and use the PKCE flow where the docs require it.

Environment variables should use the current Supabase key model from the official docs. Public browser-safe values can be exposed with `NEXT_PUBLIC_` names. Secret or service-role keys must stay server-only and must not be referenced from client components.

## Implementation Checkpoints

1. Confirm the stack.
   - Next.js version and App Router status.
   - Supabase project URL and key type.
   - Whether the app starts from the official template or adds auth to an existing app.

2. Configure email-first auth.
   - Enable email/password sign-up.
   - Decide whether email confirmation is required for sign-in.
   - Configure redirect URLs for local, preview, and production environments.
   - Configure password reset email redirects before exposing the flow.

3. Add server-side session handling.
   - Use the current Supabase server-side auth package and docs.
   - Store sessions in cookies for server-rendered access.
   - Keep browser clients and server clients separate.
   - Do not pass service-role keys to client components.

4. Add user data boundaries.
   - Store product profile data in an app-owned table linked to the Supabase auth user.
   - Enable row-level security before user data becomes reachable from the client.
   - Write policies with `auth.uid()` for user-owned rows.
   - Do not use user-editable metadata as an authorization source.

5. Set up local development.
   - Use Supabase CLI local development when the project needs local Auth, migrations, or edge functions.
   - Keep local secrets in environment files ignored by git.
   - Do not expose the local Supabase stack on an untrusted network.

6. Keep product logic outside the provider.
   - Let Supabase handle credentials, tokens, email verification, and password reset.
   - Keep plan access, onboarding state, roles, and product-specific profile fields in application tables.
   - Add admin operations only after a real admin workflow exists.

## Verification

Run the project-specific checks, then manually verify:

- A new user can sign up with email and password.
- Email confirmation works when enabled.
- The user can sign in.
- The user can sign out.
- Password reset sends an email and completes through the configured redirect.
- Protected routes reject unauthenticated users.
- Server-rendered pages can read the authenticated session only through the server-side auth path.
- Row-level security blocks another user from reading or mutating private rows.
- Browser code cannot access secret or service-role keys.
- Local development works without using production credentials.

## Handoff Notes

- Record the exact Supabase docs and package versions used during implementation.
- Document whether the project uses the official template or existing-app integration path.
- Document auth-related environment variables by name, never by value.
- Document every database policy added for user-owned data.
