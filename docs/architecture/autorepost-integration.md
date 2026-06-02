# AutoRepost Integration Boundary

## Decision

MindFlow should integrate `/Users/jie.feng/wlb/AutoRepost` as an external publishing adapter for Weibo. MindFlow should not move AutoRepost code, browser data, Chrome extensions, JSON queue files, or Playwright session management into this repository during the MVP backend work.

## Why

AutoRepost is already a mixed Python, FastAPI, Playwright, browser-profile, and extension project. Its useful capability is publishing to Weibo through a persistent browser session. Its queue and history are operational state, not product truth.

MindFlow needs stable product state for drafts, schedules, previews, and publish jobs. PostgreSQL should own that state, and AutoRepost should be called only when a MindFlow publish job needs a Weibo adapter action.

## Relevant AutoRepost Capabilities

Observed files:

- `/Users/jie.feng/wlb/AutoRepost/weibo_api_playwright_final.py`
- `/Users/jie.feng/wlb/AutoRepost/docs/ARCHITECTURE.md`
- `/Users/jie.feng/wlb/AutoRepost/README.md`

Relevant endpoints:

| Endpoint | Use In MindFlow | Notes |
| --- | --- | --- |
| `GET /status` | Health and login visibility | Returns whether browser is open and Weibo appears logged in. |
| `POST /api/weibo/publish` | Queue or immediately publish Weibo content | Primary integration point. Use queue mode by default. |
| `GET /api/queue/status` | Adapter queue visibility | Useful for operator diagnostics, not as MindFlow source of truth. |
| `GET /api/queue/tasks` | Adapter queue visibility | Useful for reconciliation when a `legacy_task_id` exists. |
| `GET /api/queue/history` | Adapter history visibility | Best-effort reconciliation only. |

AutoRepost request shape for Weibo:

```json
{
  "content": "发布的内容",
  "with_timestamp": false,
  "images": ["https://example.com/image.jpg"],
  "local_images": ["/path/to/local/image.jpg"],
  "immediate": false
}
```

AutoRepost queue-mode response shape:

```json
{
  "success": true,
  "message": "任务已加入队列，当前队列位置: 1",
  "task_id": "task_20240101120000_abc123",
  "queue_position": 1
}
```

## MindFlow Adapter Contract

The future MindFlow backend should expose an internal publishing service with one narrow operation:

```text
enqueuePublishJob(publish_job_id)
```

For a Weibo job using AutoRepost, the service should:

1. Load `publish_jobs`, `platform_previews`, `draft_assets`, and `platform_accounts`.
2. Check the publish job is `scheduled` or `queued`.
3. Check AutoRepost health through `GET /status`.
4. Build an AutoRepost request:
   - `content`: platform preview body, with title included only if the Weibo preview requires it.
   - `images`: remote image URLs from draft assets.
   - `local_images`: local paths from ready draft assets.
   - `with_timestamp`: false by default.
   - `immediate`: false by default.
5. Call `POST /api/weibo/publish`.
6. Store `legacy_task_id`, `queue_position`, and response payload in `publish_jobs.adapter_payload`.
7. Transition MindFlow status to `queued`.
8. Write a `publish_job_events` row.

MindFlow should not call AutoRepost's destructive queue endpoints, such as clear queue or delete task, until a later sprint defines operator controls and safety checks.

## Status Mapping

| MindFlow status | Trigger |
| --- | --- |
| `scheduled` | User selected a future publish time. |
| `queued` | AutoRepost accepted the request and returned `task_id`. |
| `publishing` | Reconciliation sees the task processing, or a future worker starts direct publishing. |
| `published` | AutoRepost history or operator confirmation shows success. |
| `failed` | AutoRepost rejects the request, reports repeated failure, or reconciliation cannot recover after retry policy. |
| `cancelled` | User cancels before the adapter starts, or operator marks the job cancelled. |

AutoRepost currently has two important limitations:

- Its queue load path deletes the queue file on service startup, so MindFlow must not assume adapter queue persistence across restarts.
- Its in-memory history is not a durable audit log, so MindFlow must record publish job events in PostgreSQL.

## Error Handling

Recommended first implementation behavior:

- `401` or "未登录": mark platform account `expired`, keep job `scheduled` or mark `failed` based on user action policy, and write a publish event.
- `503` queue full: leave job `scheduled`, record the error, and retry later.
- `5xx` publish error: increment `retry_count`; mark `failed` when `retry_count >= max_retries`.
- Image download/upload failure: record `last_error` and event payload; do not silently publish text-only unless the user explicitly requests that behavior.
- Unknown AutoRepost response: mark `failed` and keep raw bounded response in `adapter_payload`.

## Security Boundary

Do not store these in PostgreSQL:

- Weibo password
- Cookies
- Browser profile files
- Playwright user data directory
- Chrome extension secrets
- API tokens for future direct platform integrations

Allowed non-secret fields:

- `platform_accounts.display_name`
- `platform_accounts.external_account_id`
- `platform_accounts.connection_status`
- `publish_jobs.legacy_task_id`
- AutoRepost queue position and bounded response metadata

## Out Of Scope For The First Integration

- Direct Douyin publishing.
- Direct Xiaohongshu publishing.
- AutoRepost code migration into MindFlow.
- Managing AutoRepost's Chrome extensions from MindFlow.
- Clearing or mutating AutoRepost's queue from MindFlow.
- Production secret management.

## Next Implementation Slice

Create backend migrations for the Sprint 08 schema, then implement:

- `GET /api/drafts`
- `POST /api/drafts`
- `PUT /api/drafts/{id}`
- `POST /api/drafts/{id}/schedule`
- `GET /api/publish-jobs`

Only after that should MindFlow add a Weibo AutoRepost adapter that calls `POST /api/weibo/publish`.
