# Sprint 08 Design: PostgreSQL Schema and AutoRepost Boundary

## Context

Sprint 07 produced a static frontend prototype for the MindFlow AI content creation workbench. The next decision is where product state lives and how the existing `/Users/jie.feng/wlb/AutoRepost` capability should be integrated.

The approved direction is to make PostgreSQL the MindFlow source of truth and treat AutoRepost as an external Weibo publishing adapter.

## Design Options Considered

### Recommended: PostgreSQL Source Of Truth, AutoRepost Adapter

MindFlow stores topics, personas, drafts, assets, platform previews, schedules, platform accounts, publish jobs, and publish events in PostgreSQL. AutoRepost is called only when a Weibo publish job needs to be queued or reconciled.

This keeps MindFlow's business state durable while reusing AutoRepost's working Playwright publishing capability.

### Alternative: Move AutoRepost Into MindFlow

This would centralize code, but it would also bring browser profiles, Chrome extensions, Playwright session handling, JSON queues, and operational state into the app too early.

### Alternative: Build API First Without Schema

This could produce endpoints quickly, but it would force the data model to emerge accidentally from mock frontend state and adapter responses.

## Chosen Architecture

- PostgreSQL owns product records and publish job lifecycle.
- AutoRepost remains an external service boundary.
- MindFlow stores AutoRepost `task_id` only as `publish_jobs.legacy_task_id`.
- MindFlow records every status transition in `publish_job_events`.
- Sensitive credentials and browser login state remain outside PostgreSQL.

## Data Flow

1. User creates or edits a draft.
2. MindFlow stores the draft and platform previews.
3. User schedules a platform publish.
4. MindFlow creates a `publish_jobs` row.
5. A future backend worker reads due jobs.
6. For Weibo jobs, the worker calls AutoRepost `POST /api/weibo/publish`.
7. MindFlow stores the returned `legacy_task_id` and marks the job `queued`.
8. Reconciliation or operator confirmation marks the job `published` or `failed`.

## Error Handling

- AutoRepost unavailable: keep product state in PostgreSQL and record the error on the job.
- AutoRepost queue full: keep the job scheduled and retry within policy.
- Login expired: mark the platform account expired and write a publish event.
- Adapter response unknown: fail conservatively and preserve bounded response metadata.

## Verification

Sprint 08 is documentation-only. Verification is:

- `./scripts/check.sh`
- `git diff --check`
- `rg` checks for core schema and AutoRepost boundary terms

## Implementation Handoff

The next sprint should create backend migrations and draft/schedule API endpoints from the schema documents. It should not connect production platform APIs until credentials and rate-limit behavior are designed.
