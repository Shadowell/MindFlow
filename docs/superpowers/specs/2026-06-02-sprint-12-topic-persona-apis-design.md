# Sprint 12 Topic and Persona APIs Design

## Context

Sprint 11 wired the frontend workflow to backend draft, preview, schedule, and publish job APIs. The left-column inputs still come from static frontend arrays. Sprint 12 adds backend API surfaces for those inputs without changing the frontend yet.

## API Shape

- `POST /api/topics`
  - Creates a topic with title, source platform, optional source URL, heat score, signal, and raw metadata.
- `GET /api/topics`
  - Lists topics ordered by `discovered_at desc`.
- `POST /api/personas`
  - Creates an active persona template.
- `GET /api/personas`
  - Lists active personas ordered by creation time.

## Data Access

The implementation uses SQLAlchemy Core against existing `topics` and `personas` metadata. Runtime access uses the existing `DATABASE_URL` session dependency, while tests inject an isolated SQLite database.

## Error Handling

- Request validation rejects invalid heat scores and missing required fields.
- Persona listing returns active personas only.
- The sprint does not add delete or archive endpoints.

## Testing

Tests cover:

- Creating and listing topics.
- Topic ordering by discovery time.
- Creating personas.
- Active-only persona listing.

Repository checks continue to run frontend tests/build/lint, backend compile, backend pytest, and Alembic offline migration rendering.

## Out of Scope

- Frontend wiring.
- Real trend ingestion.
- AI generation.
- Authentication and ownership.
- AutoRepost or platform publishing.
