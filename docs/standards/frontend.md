# Frontend Development Standard

## Purpose

Use this standard when adding or changing frontend code. Build usable product screens first, keep implementation accessible and maintainable, and avoid decorative complexity that does not serve the workflow.

## Source Baseline

- [MDN: Web performance](https://developer.mozilla.org/en-US/docs/Web/Performance)
- [MDN: CSS and JavaScript accessibility best practices](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/CSS_and_JavaScript)
- [W3C: WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [React documentation](https://react.dev/)
- [Next.js project structure](https://nextjs.org/docs/app/getting-started/project-structure)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [ESLint configuration documentation](https://eslint.org/docs/latest/use/configure/)
- [Prettier options documentation](https://prettier.io/docs/options.html)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Rules

1. Build the actual user workflow as the first screen for apps and tools. Do not create a marketing landing page unless the user asked for one.
2. Use semantic HTML and accessible controls before custom interaction patterns.
3. Meet WCAG-oriented basics: visible focus states, labels for inputs, meaningful button text or accessible names, sufficient contrast, and keyboard operability.
4. Keep components small and purpose-driven. Extract shared components after duplication is real.
5. Prefer TypeScript for non-trivial frontend projects unless the existing project is JavaScript-only.
6. Use framework routing, data fetching, and rendering conventions instead of hand-rolled alternatives.
7. In React and Next.js, keep client components limited to interactive UI that needs browser state or effects.
8. Avoid global state until local state, props, URL state, or server data are insufficient.
9. Use images and visual assets deliberately. Avoid generic decorative backgrounds when the product, data, or workflow needs clarity.
10. Validate and encode user-controlled data before rendering or sending it to APIs.
11. Keep linting and formatting automated through the existing project tooling. If no tooling exists, add it only when frontend work becomes real enough to justify it.

## Design Expectations

- Operational tools should favor dense but readable layouts, predictable navigation, and fast scanning.
- Consumer, creative, or game experiences may use richer visual treatment when it supports the purpose.
- Cards are for repeated items, modals, and framed tools. Do not nest cards inside cards.
- Text must fit its container across desktop and mobile.
- Responsive behavior should be designed with explicit layout constraints, not accidental wrapping.

## Performance Expectations

- Optimize the critical path: avoid unnecessary client JavaScript, large unused assets, and render-blocking work.
- Use framework image, font, and bundle optimization features when available.
- Measure before adding complex performance machinery.

## Verification

When frontend code exists, `./scripts/check.sh` should eventually run the project-selected checks, such as:

```bash
npm run lint
npm run build
```

For visual or interaction-heavy work, verify in a real browser and record what was checked.
