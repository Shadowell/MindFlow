# Sprint 08 Contract: PostgreSQL Schema and AutoRepost Boundary

## Goal

Define the first persisted data model and publishing integration boundary for MindFlow, so the next implementation sprint can turn the static workbench prototype into a backend-backed workflow without prematurely moving AutoRepost code into this repository.

## In Scope

- Document the MVP PostgreSQL schema for topics, personas, drafts, assets, platform previews, schedules, platform accounts, publish jobs, and publish job events.
- Document table relationships, required constraints, status values, and initial indexes for the core workflow.
- Document how `/Users/jie.feng/wlb/AutoRepost` should be integrated as an external publishing adapter for Weibo.
- Record which AutoRepost APIs are relevant to MindFlow and which capabilities remain out of scope.
- Update product spec and progress handoff.
- Add a QA report for this documentation sprint.

## Out of Scope

- Creating a backend application.
- Creating real database migrations.
- Connecting to the deployed PostgreSQL server.
- Calling AutoRepost from MindFlow code.
- Moving AutoRepost code, browser profiles, queue JSON files, or extension code into MindFlow.
- Connecting Douyin, Weibo, or Xiaohongshu production APIs.
- Storing platform passwords, cookies, browser login state, API tokens, or other secrets in PostgreSQL.

## Deliverables

- `docs/architecture/postgresql-schema.md`
- `docs/architecture/autorepost-integration.md`
- `docs/superpowers/specs/2026-06-02-sprint-08-postgresql-autorepost-design.md`
- Updated `docs/spec.md`
- Updated `docs/progress.md`
- `docs/qa/sprint-08-postgresql-schema-and-autorepost-boundary-report.md`

## Done Means

- A future implementation sprint can create migrations from the documented schema without guessing entity ownership.
- The schema keeps PostgreSQL as MindFlow's source of truth for drafts, schedules, and publish job state.
- AutoRepost is clearly treated as an external adapter, not as the main persistence layer.
- Relevant AutoRepost endpoints and status mapping are documented.
- Sensitive platform credentials are explicitly excluded from PostgreSQL in this sprint.
- Repository verification passes.

## Verification

```bash
./scripts/check.sh
git diff --check
rg -n "publish_jobs|platform_previews|AutoRepost|legacy_task_id|PostgreSQL" docs/spec.md docs/progress.md docs/architecture docs/contracts/sprint-08-postgresql-schema-and-autorepost-boundary.md docs/qa/sprint-08-postgresql-schema-and-autorepost-boundary-report.md
```

Manual or QA checks:

- Confirm the schema avoids sharding, CQRS, event sourcing, read replicas, and speculative denormalized read models.
- Confirm no Sprint 08 deliverable stores platform credentials, cookies, or browser login state.
- Confirm AutoRepost remains an external service boundary.
- Confirm future implementation work is limited to migrations/API wiring rather than production publishing.

## Risks / Notes

- AutoRepost currently keeps queue state and history in memory/JSON files, so MindFlow should not rely on it as the product source of truth.
- AutoRepost's browser session and login state are operational concerns and must stay outside the database.
- Real platform publishing will still require credential handling, rate-limit policy, retry semantics, and security review.

## Handoff

- Next likely step: implement a small backend skeleton with migrations for the documented schema, then expose draft and schedule APIs that the existing frontend can call.
