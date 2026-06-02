# Product Spec

## Product Summary

MindFlow is an AI-assisted content creation workbench for planning, drafting, previewing, and scheduling image-text posts across Douyin, Weibo, and Xiaohongshu. The current implementation includes a frontend workbench wired to backend APIs, plus a Python backend foundation with PostgreSQL migrations and product APIs for topics, personas, backend draft composition, drafts, platform previews, schedules, and publish jobs. AI generation, production database connection, and platform publishing are not connected yet.

The repository still keeps the Codex project-template harness: sprint contracts, progress notes, QA reports, and engineering standards remain the source of truth for incremental delivery.

## Users

- Individual creators who publish recurring social content.
- Small content operations teams that need a lightweight drafting and scheduling surface.
- Developers using Codex to build the MindFlow product incrementally.

## Core User Journeys

1. Review trending topics and choose one as the current creation theme.
2. Select an account persona and generate a draft image-text post.
3. Edit the generated title, body, tags, and image structure.
4. Preview how the draft reads on Douyin, Weibo, and Xiaohongshu.
5. Add the draft to a publishing schedule and prepare it for a future publishing queue.
6. Continue implementation through sprint contracts, verification, and progress notes.

## Product Priorities

1. Make the creation workflow visible and usable before backend integration.
2. Keep the UI operational, dense, and reviewable rather than marketing-oriented.
3. Support Douyin, Weibo, and Xiaohongshu as first-class target platforms.
4. Preserve a path to integrate the existing `/Users/jie.feng/wlb/AutoRepost` capability behind a publishing queue.
5. Use PostgreSQL for persisted product data because the user's server is already deployed.
6. Keep commodity modules lightweight and avoid premature architecture patterns.
7. Preserve the Codex harness so work can continue across sessions without relying on chat history.

## Technical Shape

- Frontend: Vite + React + TypeScript under `frontend/`.
- Current frontend state: operational prototype with backend-loaded topic/persona inputs, backend draft composition, and backend API calls for draft, preview, schedule, and publish job persistence.
- Backend: Python FastAPI under `backend/`, with SQLAlchemy metadata, Alembic migrations, health endpoint, and product APIs for topics, personas, deterministic draft composition, drafts, platform previews, schedules, and publish jobs.
- Storage: PostgreSQL planned for product data, with the MVP schema documented in `docs/architecture/postgresql-schema.md` and executable migrations under `backend/migrations/`; markdown files and repository history for delivery state.
- AI generation: not connected yet.
- Platform integrations: Douyin, Weibo, and Xiaohongshu planned; no live API connection yet.
- Legacy publishing: `/Users/jie.feng/wlb/AutoRepost` is documented as an external Weibo publishing adapter in `docs/architecture/autorepost-integration.md`; it is not the MindFlow source of truth.
- Standards: markdown guidance under `docs/standards/` for Python, Java, database design, frontend work, and reusable commodity modules.
- Auth selection: documentation-only decision matrix and stack recipes remain available for future implementation sessions.

## Constraints

- Do not overwrite existing Sprint 04-06 documentation when adding product code.
- Keep prototype work static until backend contracts are defined.
- Do not connect production platform credentials without explicit approval and secret-handling design.
- Do not store platform credentials, cookies, browser login state, or Playwright user data in PostgreSQL.
- Match database design complexity to the current product scale; avoid sharding, CQRS, or denormalized read models without evidence.
- Prefer mature lightweight integrations for commodity modules such as authentication.

## Non-Goals

- Building a marketing landing page.
- Implementing real AI generation in the prototype sprint.
- Connecting the deployed PostgreSQL server before credentials, backup expectations, and environment handling are confirmed.
- Connecting Douyin, Weibo, or Xiaohongshu APIs before platform adapter requirements are defined.
- Migrating AutoRepost code into MindFlow during the MVP backend work.
- Replacing project-specific engineering judgment with the harness.

## Acceptance Direction

The immediate frontend acceptance flow is now: load topics and personas from backend APIs, choose one of each in the workbench, compose and persist the draft plus platform previews through `POST /api/compositions/drafts`, then create a schedule and publish job through the backend. The next acceptance direction is to connect the backend to a deployed PostgreSQL environment after environment handling is confirmed, or add missing backend APIs for assets and provider-backed AI generation.

## Open Questions

- Which AI provider and prompt contract should be used for real draft generation?
- How should deployed PostgreSQL credentials and environment-specific secrets be provided outside the repository?
- What account and credential model is required for Douyin, Weibo, and Xiaohongshu publishing?
