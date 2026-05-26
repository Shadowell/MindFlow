# Sprint 02 Contract: Development Standards

## Goal

Add lightweight, source-backed development standards for Python, Java, database design, and frontend work so future Codex sessions can follow consistent engineering rules without bloating the harness.

## In Scope

- Add standards documents for Python, Java, database design, and frontend development.
- Include source references for each standards area.
- Add database design guidance that scales with project size and explicitly avoids premature complexity.
- Update project operating rules so Codex reads the relevant standards before implementation.
- Update progress and QA handoff files.

## Out of Scope

- Enforcing every standard with tooling in this sprint.
- Choosing one application stack for all future projects.
- Adding framework-specific templates, generators, or CI.
- Introducing fallback implementations, mocks, or compatibility layers.

## Deliverables

- `docs/standards/python.md`
- `docs/standards/java.md`
- `docs/standards/database.md`
- `docs/standards/frontend.md`
- Updated `AGENTS.md`, `docs/spec.md`, `docs/progress.md`, and README references.
- QA report for this documentation sprint.

## Done Means

- A future Codex session can identify which standard to read for a requested technology stack.
- The database standard includes small, medium, and large project design expectations.
- Verification has been run through `./scripts/check.sh`.
- Known gaps are documented.

## Verification

```bash
./scripts/check.sh
```

Manual or QA checks:

- Confirm each standards document includes source references.
- Confirm project rules point to the standards directory.
- Confirm database guidance warns against over-design without evidence.

## Risks / Notes

- These standards are intentionally concise. They should guide implementation decisions, not replace stack-specific engineering judgment.
- Tooling enforcement should be added only after a real project proves which stack is active.

## Handoff

- Next likely step: add optional check hooks for whichever stack the first real project chooses.
