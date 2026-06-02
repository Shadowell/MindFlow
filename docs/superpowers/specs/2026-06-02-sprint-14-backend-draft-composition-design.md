# Sprint 14 Design: Backend Draft Composition API

## Endpoint

`POST /api/compositions/drafts`

Request:

- `topic_id`: persisted topic id
- `persona_id`: active persona id
- `platforms`: one or more of `douyin`, `weibo`, `xiaohongshu`

Response:

- `draft`: created `DraftResponse`
- `platform_previews`: created `PlatformPreviewResponse[]`

## Behavior

The endpoint reads the selected topic and persona through SQLAlchemy Core. It rejects missing topics and inactive or missing personas with explicit HTTP errors.

For a valid request, it creates:

- one `drafts` row
- one `platform_previews` row for each selected platform

The draft uses:

- `status = "generated"`
- `generation_source = "backend_template_composer"`
- `topic_id` and `persona_id` from the request

The preview rows use:

- `validation_status = "valid"`
- platform-specific title/body/hints derived from the same topic/persona inputs
- `validation_details.source = "backend_template_composer"`

## Why Template Composition

This sprint establishes the backend contract without adding an AI provider, prompt format, secret handling, billing risk, or model behavior. A future sprint can replace the deterministic composer behind the same API boundary.

## Tests

Add isolated backend API tests with an in-memory SQLite database:

- success: create topic/persona, compose a draft for three platforms, assert persisted draft/previews
- rejection: inactive persona cannot be used for composition

## Out of Scope

- Frontend generation wiring
- AI provider calls
- Image assets
- Deployed PostgreSQL migration execution
- AutoRepost runtime integration
