# KAISER / Atelier — an interactive portfolio

The published site is available at **https://kaiseriiii.github.io/KaiserIIII/**.

A self-contained, bilingual personal engineering portfolio with original editorial artwork and a source-backed project explorer. It uses no framework, remote font, analytics beacon or third-party profile badge.

## Explore

Open `index.html` directly in a modern browser, or use a local server:

```bash
python3 -m http.server 8765 --directory experience
```

The site supports an animated orbit illustration, bilingual content, keyboard-search command palette (Cmd/Ctrl+K or /), project archive search, category filters, draggable SVG relationship graph, project evidence inspector, **project-to-project comparison**, and shareable, interactive system blueprints (for example `?case=zhixu` and `?case=migrationwitness`). Controls are keyboard accessible and honor reduced-motion preferences.

## Files

- `index.html` — semantic structure and metadata
- `styles.css` — responsive editorial design and reduced-motion styles
- `data.js` — ten projects with Chinese/English copy and known public source links
- `app.js` — rendering, graph motion, drag interactions and accessible palette
- `blueprints.js` — six bilingual conceptual architecture journeys with explicit scope limits
- `casebook.js` — keyboard-accessible stage diagrams, direct links, and modal interactions
- `compare.js` — side-by-side curated comparisons, SVG connection art and shareable URL state
- `lab-engine.js` — pure, deterministic toy models for PostgreSQL-like grant contracts and tenant-scoped lexical retrieval
- `lab-ui.js` — bilingual lab forms, status outputs, trace viewer and JSON scenario export
- `cover.svg` and `favicon.svg` — vector branding

## Verification

The source suite checks local scripts, semantic structure, public links, data boundaries and a 230 KB raw-file budget. The Chromium smoke suite checks mobile and desktop layouts, both languages, filtering, SVG drag/reset, search, stage-by-stage project exploration, reduced motion and axe-core A/AA severe accessibility findings.

```bash
python3 tools/check_experience.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Browser test: `node tools/browser_smoke.cjs` with a local server and Playwright installed. See `../docs/ATELIER.md` for design constraints and evidence caveats.

The profile README itself is static by GitHub design, with an animated image linking to this real, interactive Pages application.

## V7 acceptance snapshot

The 2026-11-23 V7 branch passed 26 Python source tests, the Chromium interaction suite
(desktop and 390px touch viewport), Chinese/English switching, SVG drag/reset,
project comparison, mobile filtering, deep links, reduced-motion checks,
and automated axe-core WCAG A/AA checks with zero reported violations.
These are scoped automated checks, not a blanket accessibility certification.
The source budget measures raw on-disk bytes rather than an unreliable
cache-dependent transfer estimate.

Use the [GitHub Actions logs](https://github.com/KaiserIIII/KaiserIIII/actions)
and downloadable visual-review screenshots to inspect acceptance evidence.

## V8 — Hands-on reliability lab

At `/?lab=permission#lab` and `/?lab=retrieval#lab`, visitors can change input parameters and execute **real JavaScript models** in their own browser. The toy grant model compares expected SQL privileges with actual privileges after a simplified native alter or replacement swap and optional grant replay. The toy retrieval model filters six invented documents by tenant before ranking exact query-token overlaps; disabling the scope creates a reproducible foreign-tenant leak.

The lab neither starts PostgreSQL nor issues pg-osc commands, and it does not run Zhixu, Chroma, embeddings or a language model. Its explanation and evidence links clearly distinguish the model from [real MigrationWitness experiments](https://github.com/KaiserIIII/migrationwitness/blob/main/PG_OSC_197_RESULTS.md) and [Zhixu verification](https://github.com/KaiserIIII/zhixu/blob/main/docs/verification.md).

The engine is a pure CommonJS/browser-compatible script, independently tested with `node --test tools/lab_engine.test.cjs`. The Chromium suite exercises both safe and unsafe transitions, bilingual output, touch-sized controls and no horizontal overflow. The **230 KB** raw-source budget includes the new engine and UI. There is no external analytics or runtime network call.
