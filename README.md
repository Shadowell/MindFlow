# codex-project-template

A minimal, reusable repository template for building a development harness for Codex-driven coding. The template is designed to help a project move from ad hoc prompting to a repeatable loop with planning, execution, QA, and handoff.

## Project Goal

This project exists to become a practical harness for coding with Codex. The goal is not only to store prompts, but to provide a lightweight operating system for software delivery with:

- externalized project rules
- sprint contracts
- progress handoff
- QA handoff
- a shared verification entrypoint
- room for future skills, automation, and evaluator-style review

## Design Source

This template is influenced by Anthropic's article:

- [Harness design: Building long-running applications with LLMs](https://www.anthropic.com/engineering/harness-design-long-running-apps)

The article is recorded in this repository for future reference here:

- [docs/references/harness-design-long-running-apps.md](docs/references/harness-design-long-running-apps.md)

The most important ideas carried into this template are:

- break long work into small sprint-sized contracts
- separate planning, implementation, and evaluation logic
- pass state through files instead of relying on chat history
- verify work explicitly before calling it complete

## What This Template Gives You

- `AGENTS.md`: stable project rules for Codex
- `docs/spec.md`: product and system intent
- `docs/progress.md`: current state and next step
- `docs/contracts/`: sprint-by-sprint contracts
- `docs/qa/`: QA reports and release notes
- `docs/references/`: design references and source notes
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

## Iteration Plan

This repository should evolve in small steps instead of trying to become a full harness at once.

### Phase 1: Minimal Delivery Harness

- Keep `AGENTS.md`, `spec`, `progress`, `contracts`, and `qa` files stable.
- Use `scripts/check.sh` as the single verification entrypoint.
- Prove the loop works on a real project.

### Phase 2: Stronger Verification

- Add project-specific smoke checks.
- Add browser or API acceptance checks where appropriate.
- Improve the QA report so evaluator-style review becomes more useful.

### Phase 3: Skill Extraction

- Turn repeated tasks into local skills.
- Start with contract-writing and QA-review skills.
- Add more skills only when a workflow becomes truly repetitive.

### Phase 4: Background Execution

- Add automation-friendly conventions.
- Define when tasks can continue without human supervision.
- Use worktrees or background runs only after verification is stable.

### Phase 5: Plugin or Team Distribution

- Package the harness for reuse across projects or teams.
- Move from a local template to a distributable plugin only after the workflows are proven.

## Suggested First Sprint

For a brand new project, start with a contract that creates:

- the main user journey
- the minimum test or smoke check
- the initial project progress log

## Notes

- This template is intentionally small.
- Add more structure only after the loop becomes useful.
- Prefer recording design rationale in `docs/references/` instead of burying it in chat history.
