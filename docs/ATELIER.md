# KAISER / Atelier — implementation notes

A personal portfolio must feel personal. The interactive page is not a scorecard or a template of badges; its motion and information graphics come from project-specific, source-linked data.

## Architecture

The deployed GitHub Pages site is a deterministic, dependency-free, static app:

- experience/index.html — semantic content, structured sections, search dialog and SVG stage
- experience/styles.css — editorial design tokens, responsive layout and motion semantics
- experience/data.js — bilingual public project records, tech tags and evidence links
- experience/app.js — SVG graph, pointer interaction, rendering and command search
- experience/favicon.svg and experience/cover.svg — self-authored SVG assets

GitHub README pages sanitize script execution, so the README remains a visual doorway to the separately deployed Pages application.

## Interaction design

- Domain-to-project edges are curated (not an inferred skill score).
- SVG node dragging updates Bezier paths with screen-to-SVG coordinate conversion.
- Animated particles follow the same geometry with requestAnimationFrame, avoiding per-frame layout reads.
- Scroll-triggered reveals are progressive enhancement; no-JS readers still see the primary content.
- An on-demand command palette opens with Cmd/Ctrl+K, /, or the search icon.
- The archive supports local string matching across both languages and technology tags.
- Labels and descriptions use DOM text APIs rather than HTML interpolation.
- Motion honors prefers-reduced-motion and loops avoid work when off-screen.
- All proof links are authored with known public repository URLs.

## Source boundaries

The profile does not expose private source or imply all systems are production-ready.

- CardCraft: playable Steam demo and public engineering cases; game source remains private.
- Zhixu: verification notes report 120 backend and 33 frontend tests for 2026-10-08, not a coverage percentage.
- MigrationWitness: evidence describes a specific PostgreSQL/pg-osc reproduction, not all migrations.
- Research projects are versioned artifacts, not automatically peer-reviewed publications.

## Validation

CI runs source checks and JavaScript syntax tests, then a real Chromium smoke run for desktop and mobile layouts, language switching, local search, graph interactions, command palette and reduced-motion preferences. Screenshots are kept as workflow artifacts for visual review.

## Rollback

Git history contains the prior single-file experience; restore it from the prior main commit. Pages publishes only the experience folder.

## System blueprints (V6)

The casebook is a source-linked, keyboard-accessible interaction layer rather than an unrelated animation. Six public projects have bilingual conceptual flow models in `experience/blueprints.js`: CardCraft, Zhixu, WiFiScope, MigrationWitness, Construction Cost Analyzer, and ReproShift. Four additional projects use smaller, deliberately non-speculative overview models from `experience/data.js`.

The standalone `experience/casebook.js` renderer builds SVG stage nodes and cubic connection paths from the model. It provides numbered HTML stage controls for touch and assistive technology, a native modal dialog for focus containment, synchronized language changes and deep links such as `?case=zhixu`. Each diagram marks the difference between a conceptual architecture and actual runtime measurements and links back to public code or records.

## Quality gates added in V6

- JS syntax checks and Python source/claim-integrity tests run in CI.
- Playwright Chromium checks the existing project explorer, its drag/reset behavior, a keyboard command search, the casebook, deep links, Chinese/English labels, and 390px mobile interactions.
- `axe-core` checks WCAG 2.0/2.1 A/AA issues with serious and critical impacts treated as CI failures; it does not certify full WCAG 2.2 conformance or replace human review.
- A local resource transfer budget is checked in browser CI. This is a laboratory budget; real-user LCP, INP and CLS require field measurements.
- Screenshots from real Chromium runs are retained as test artifacts for editorial review.

The point of these gates is to catch regressions rather than to claim an arbitrary score or universal production certification.

## Comparative notebook (V7)

`experience/compare.js` renders a side-by-side comparison of any two **public** projects using the existing ten-record bilingual data source. It shows independently sourced focus, tech, proof, and known limits; shared areas are simply set intersections of the four curated `domains` labels. No ranking, benchmark, inferred causal link, or fabricated graph weight is calculated. The visual connector is explicitly labeled conceptual; the full text is available in adjacent semantic sections.

The comparison is deep-linkable via `?compare=<project-id>,<project-id>#compare`. Change/swap/preset controls preserve unrelated URL query parameters, restore state through browser history, and provide a copyable link. `experience/app.js` renders a native-button **mobile project index** while retaining the draggable SVG for wider screens. Without scripting, the SVG fallback remains available and scrollable.

V7 acceptance adds Playwright tests for comparison selection, shared-label counts, deep links, swaps, bilingual copy, touch-sized project cards, map filtering, no page horizontal overflow, and automated accessibility auditing. The asset budget includes the comparison module; browser timings are *not* claimed as measured Core Web Vitals.
