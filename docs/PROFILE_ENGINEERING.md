# Profile engineering / 主页实现说明

This repository's README is an executable design system, not a collection of externally hosted badges.

## The challenge

GitHub READMEs cannot safely execute JavaScript, so conventional interactive dashboards are not available in the profile itself. Instead, the profile uses **self-hosted, generated SVG**: diagrams, graphic encoding and data summaries render inside GitHub's supported Markdown image pipeline. The real interaction is through linked inspectable code and expandable evidence panels.

## Data contract

1. Fetch public repository metadata from the official GitHub REST `/users/KaiserIIII/repos` endpoint with pagination, a timeout and an optional token. No private repository endpoint is queried.
2. Explicitly filter `private == false`, require matching account owner, and exclude forks and the profile repository for project-level statistics.
3. Aggregate primary-language counts, creation months (rolling 12 calendar months, UTC), and repos with a push within 30 days.
4. The diagram **must not** imply that repository counts equal commits, hours, code volume, seniority, or impact. Creation months are **not contribution activity**.
5. Input labels are HTML/XML escaped and each generated SVG is parsed as XML; no remote image, imported fonts, scripts or tracking endpoints.
6. Assets are committed, so a failed API request leaves the last successful page available. Metadata provenance and assumptions are visible in the README.

## Visual system

Design tokens: `#F8F5EF` warm paper, `#FFFCF7` warm white, `#342F2B` charcoal ink, `#C67858` terracotta, `#667D70` sage, `#697F98` muted blue. Type uses Georgia for editorial display headings and platform sans-serif for technical annotation; no webfont request. Variable-length data labels are XML-escaped.

The source-controlled renderer builds these views:

| Asset | Construction |
|:--|:--|
| `profile-hero.svg` | Parametric circles, Bezier curves, typography, and a purpose-built mark |
| `project-atlas.svg` | Capability → repository bipartite evidence graph; curated edges |
| `live-dashboard.svg` | Public REST metadata → language bars, monthly histogram and metric summaries |
| `engineering-loop.svg` | Six stages of the page's own implementation and publishing pipeline |
| `evidence-board.svg` | Curated matrix tied to individual repository validation notes |

Graphics use viewBox scaling and real alt text. GIF animation and SVG JavaScript are intentionally avoided for predictable GitHub rendering and reduced motion.

## Reproduce

```bash
python3 -m unittest discover -s tests -v
python3 tools/render_live_metrics.py --art-only
python3 tools/render_live_metrics.py --output assets/live-dashboard.svg
```

The last command requires API access. The first two are offline and deterministic. The GitHub Action tests before rendering and publishes only changed generated SVG files. Static diagrams regenerate from code rather than being maintained separately.

## Honest limitations

The private CardCraft source and other private repositories are not included in public analytics. A hosted CI pass is not a production proof. The repository evidence mapping is curated, not an algorithmic proficiency score. SVG files are static inside README: a genuinely interactive application would require a separately deployed website, not a misleading script embedded in Markdown.
