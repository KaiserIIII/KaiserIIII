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

## Hands-on reliability lab (V8)

The most important change is from describing systems to *demonstrating their invariants*. `experience/lab-engine.js` contains two small, auditable, deterministic models with no I/O: a synthetic role-grant contract under a toy table swap, and a tenant-scoped lexical search of exactly six invented documents. The latter applies authorization before token scoring, and an explicit unsafe toggle shows how foreign-tenant results can emerge. Neither model should be mistaken for production PostgreSQL/pg-osc or a deployed Zhixu/Chroma/LLM execution.

`experience/lab-ui.js` owns the bilingual user interaction, two accessible tabs, native inputs, repeatable execution trace, independent check results, JSON scenario export, public source links and `?lab=permission|retrieval#lab` navigation. The lab is designed to teach the underlying security/reliability question without claiming a production benchmark or scientific run.

Acceptance is added in two layers: pure Node tests for model invariants and a real Chromium browser sequence for changing user inputs, unsafe/safe transitions, localization, URL state, mobile layout and axe-core checks. All source remains small (230 KB raw cap), self-hosted and free of third-party frontend JavaScript.

## V9 — Guided Field Notes / human-first orientation

The portfolio is now large enough that new visitors need a way through it. The optional, editorial `experience/journey.js` reader exposes three short bilingual paths: shipping a real product, inspecting why successful processes can still fail, and connecting construction, network and software engineering. Each route consists of verified public project references, clear scope, native dialog navigation, a miniature reading-progress visualization and actionable handoffs to the existing **real** site tools.

This is **navigation**, not invented project metrics, telemetry or a synthetic validation result. Each reading step cites public sources already present in the curated project data; private code remains private. Deep links preserve a `trail` and a numbered `note` in the URL, and no page action requires sign-in, analytics or remote JavaScript. Readers choose this experience; the homepage never interrupts them automatically.

The dialog uses focus containment, accessible names, left/right keyboard step navigation, native buttons and responsive narrow-screen layout. It supports `prefers-reduced-motion`. The visual index and cases remain available for visitors who prefer browsing freely. V9's static raw source cap is 250 KB across 12 first-party files, with independent Chromium mobile and accessibility tests.

## V10 — Evidence search instead of an AI-shaped façade

The highest-value change is a **better retrieval interaction**, not a new section. `experience/search-engine.js` provides deterministic, bilingual signals for shipping, databases, knowledge retrieval, security boundaries, construction costs, verification, research and engineering workflows. It scores **query relevance only** against the ten previously published public records in `experience/data.js`; ranking is not a person-quality or project-maturity metric. The code displays recognized themes, the original `proof`, recorded `note` limitations, and actual public links via the existing searchable native dialog.

Chinese natural-language phrases work through transparent curated concept signals, while English technical names match public project fields. Unrecognized queries produce zero results. No query is sent to an API or stored in the portfolio, and nothing claims access to private repositories. The site should not misrepresent these curated answers as generative AI or real-time GitHub verification.

`tools/search_engine.test.cjs` verifies real bilingual queries, no-hallucination empty states, bounded input and evidence linkage. `tests/test_search.py` enforces semantic, source and script-order contracts. The Chromium acceptance suite checks that the actual interface continues to work in English, Chinese and narrow mobile layouts, alongside the existing system casebook, lab, comparison and story reader.
