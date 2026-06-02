# Sprint 15 Design: Frontend Composition API Wiring

## API Client

Add `MindFlowApi.composeDraft(payload)` for:

`POST /api/compositions/drafts`

Payload:

- `topic_id`
- `persona_id`
- `platforms`

Response:

- `draft`
- `platform_previews`

## Workbench State

The workbench adds:

- `selectedTopicId`
- `generatedPreviews`

When topics load, the first backend topic becomes both the composer text and selected topic id. Clicking a topic updates both fields. Manually editing the topic input clears the selected topic id because the backend composition endpoint requires a persisted topic.

## Generation

The `生成图文` button calls the backend composition endpoint with the selected topic/persona and all supported platforms. The returned draft is formatted into the editor, and `persistedDraftId` is set from the returned draft id.

The frontend no longer calls:

- `POST /api/drafts`
- `PUT /api/drafts/{draft_id}/platform-previews/{platform}`

from the generation action.

## Preview Panel

Before generation, the panel keeps the existing platform guidance placeholders. After generation, returned platform previews override the placeholders for title, body, hints, and validation status.

## Tests

Frontend tests prove:

- generation calls `/api/compositions/drafts`
- payload includes selected topic/persona ids and supported platforms
- backend-composed draft text appears in the editor
- schedule creation still uses the returned draft id
- composition errors render as visible alerts

## Out of Scope

- Backend changes
- AI provider calls
- Production database connection
- AutoRepost runtime integration
