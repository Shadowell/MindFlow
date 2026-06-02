# Sprint 13 Design: Frontend Topic and Persona API Wiring

## API Client

Add typed client coverage for:

- `MindFlowApi.listTopics()` -> `GET /api/topics`
- `MindFlowApi.listPersonas()` -> `GET /api/personas`

The client keeps the same base URL and error handling introduced in Sprint 11.

## Workbench State

The workbench owns:

- `hotTopics`
- `personas`
- `topic`
- `selectedPersonaId`
- `isLoadingInputs`
- `inputError`

On mount, the frontend requests topics and personas in parallel. Successful responses replace local arrays. Topic text is initialized from the first backend topic only when the composer theme is still empty. Persona selection is initialized to the first backend persona when no currently selected persona exists in the response.

## Empty and Error States

The frontend does not keep static local topic/persona fallback data.

- Loading: show a compact loading row inside the relevant panel.
- Empty topics: show that the backend has no available hotspots.
- Empty personas: show that no active persona is available and disable generation.
- Fetch failure: show a visible error state with the backend message.

## Draft Generation

Generation remains local in Sprint 13, but it must use the selected backend persona. If no persona is selected, generation stops with a visible error message.

## Tests

Frontend tests mock backend topic/persona list responses before testing draft creation and scheduling. New coverage proves:

- `/api/topics` and `/api/personas` are requested on load.
- API topics and personas render in the left panels.
- Clicking an API topic fills the composer theme.

## Out of Scope

- Frontend create/update forms for topics or personas.
- Backend draft-composition endpoint.
- Deployed PostgreSQL connection.
- AutoRepost runtime integration.
