# codex-project-template

A minimal, reusable repository template for running software delivery with Codex using:

- externalized project rules
- sprint contracts
- progress handoff
- QA handoff
- a shared verification entrypoint

## What This Template Gives You

- `AGENTS.md`: stable project rules for Codex
- `docs/spec.md`: product and system intent
- `docs/progress.md`: current state and next step
- `docs/contracts/`: sprint-by-sprint contracts
- `docs/qa/`: QA reports and release notes
- `scripts/check.sh`: one verification entrypoint
- `.agents/skills/`: optional local skills for high-frequency workflows

## Recommended Usage

1. Copy this template into a new project repository.
2. Edit `AGENTS.md` with project-specific constraints.
3. Replace `docs/spec.md` with the real product scope.
4. Create the first sprint from `docs/contracts/sprint-template.md`.
5. Teach Codex to use the loop:
   - read `AGENTS.md`
   - read `docs/spec.md`
   - read `docs/progress.md`
   - implement only the active sprint contract
   - run `./scripts/check.sh`
   - update `docs/progress.md`
   - write QA findings to `docs/qa/`

## Core Idea

This template is built around a lightweight harness:

1. Put state in files, not just in chat.
2. Work in small, verifiable sprint contracts.
3. Separate implementation from QA review.
4. Keep a single verification command.
5. Record progress so another Codex session can continue cleanly.

## Suggested First Sprint

For a brand new project, start with a contract that creates:

- the main user journey
- the minimum test or smoke check
- the initial project progress log

## Notes

- This template is intentionally small.
- Add more structure only after the loop becomes useful.
