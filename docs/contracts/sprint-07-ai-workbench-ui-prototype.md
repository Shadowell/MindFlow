# Sprint 07 Contract: AI Workbench UI Prototype

## Goal

Build a static frontend prototype for the MindFlow AI content creation workbench so the product direction can be reviewed visually before backend, PostgreSQL, OpenAI, or platform publishing integrations are connected.

## In Scope

- Create a Vite + React + TypeScript app under `frontend/`.
- Make the first screen a usable AI creation workbench, not a marketing page.
- Include hot topic selection, persona templates, a generated-copy editor, Douyin/Weibo/Xiaohongshu platform previews, and a schedule queue entry point.
- Use local mock data and React state for the prototype workflow.
- Add automated frontend tests for the key prototype interactions.
- Update `scripts/check.sh` so repository verification runs frontend checks.
- Preserve existing Sprint 04-06 documentation and recipe changes.

## Out of Scope

- Connecting to PostgreSQL.
- Calling OpenAI or any other model provider.
- Connecting Douyin, Weibo, or Xiaohongshu APIs.
- Migrating or refactoring `/Users/jie.feng/wlb/AutoRepost`.
- Replacing the existing Sprint 04-06 documentation work.
- Implementing authentication, billing, file uploads, or production deployment.

## Deliverables

- `frontend/` Vite React TypeScript prototype.
- `frontend/src/App.tsx` and CSS for the workbench UI.
- `frontend/src/App.test.tsx` interaction tests.
- Updated `scripts/check.sh`.
- Updated `docs/spec.md` and `docs/progress.md`.
- `docs/qa/sprint-07-ai-workbench-ui-prototype-report.md`.

## Done Means

- Opening the frontend lands directly on the AI creation workbench.
- Clicking a hot topic fills the creation topic.
- Clicking generate fills a mock image-text draft and marks it generated.
- Platform preview tabs switch between Douyin, Weibo, and Xiaohongshu.
- The schedule action shows the selected publish time and queued state.
- Desktop layout has three non-overlapping columns.
- Mobile layout is single-column and has no horizontal overflow.
- Repository verification passes.

## Verification

```bash
cd frontend
npm test
npm run build
npm run lint
cd ..
./scripts/check.sh
```

Manual or QA checks:

- Browser smoke check at `http://127.0.0.1:5173/`.
- Desktop viewport: confirm three columns do not overlap and no horizontal overflow exists.
- Mobile viewport: confirm single-column layout and no horizontal overflow.
- Click through hot topic selection, generation, Xiaohongshu preview, and schedule queue.

## Risks / Notes

- The prototype intentionally uses mock data and local state, so it does not prove backend contracts or publishing reliability.
- The AutoRepost integration is represented only by a Legacy publishing entry point in the UI.
- Real platform publishing will need API contracts, credential handling, audit logs, rate limit behavior, and retry semantics before implementation.

## Handoff

- Next likely step: define the backend API and PostgreSQL schema for topics, personas, drafts, platform previews, schedules, and publish jobs, then decide how `/Users/jie.feng/wlb/AutoRepost` is integrated behind the publishing queue.
