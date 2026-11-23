# KAISER / Atelier — an interactive portfolio

The published site is available at **https://kaiseriiii.github.io/KaiserIIII/**.

A self-contained, bilingual personal engineering portfolio with original editorial artwork and a source-backed project explorer. It uses no framework, remote font, analytics beacon or third-party profile badge.

## Explore

Open `index.html` directly in a modern browser, or use a local server:

```bash
python3 -m http.server 8765 --directory experience
```

The site supports an animated orbit illustration, bilingual content, keyboard-search command palette (Cmd/Ctrl+K or /), project archive search, category filters, draggable SVG relationship graph and project evidence inspector. Controls are keyboard accessible and honor reduced-motion preferences.

## Files

- `index.html` — semantic structure and metadata
- `styles.css` — responsive editorial design and reduced-motion styles
- `data.js` — ten projects with Chinese/English copy and known public source links
- `app.js` — rendering, graph motion, drag interactions and accessible palette
- `cover.svg` and `favicon.svg` — vector branding

## Verification

The source suite checks local scripts, semantic structure, public links and data boundaries. The Chromium smoke suite checks mobile and desktop layouts, both languages, filtering, SVG drag/reset, search and reduced motion.

```bash
python3 tools/check_experience.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Browser test: `node tools/browser_smoke.cjs` with a local server and Playwright installed. See `../docs/ATELIER.md` for design constraints and evidence caveats.

The profile README itself is static by GitHub design, with an animated image linking to this real, interactive Pages application.
