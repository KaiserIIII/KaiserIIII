#!/usr/bin/env python3
"""Build a source-backed public GitHub snapshot as a standalone SVG.

No private repository API is queried. Counts are based on repository metadata,
not lines of code, skill, contribution activity or production readiness.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
from html import escape
import json
import math
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

OWNER = "KaiserIIII"
API = "https://api.github.com"
COLORS = ["#62efcf", "#8cbcff", "#bc9bff", "#f9bb7c", "#8ea8be", "#5d8999"]


def public_originals(repositories: list[dict]) -> list[dict]:
    """Include only the account's public, unforked, non-profile repos."""
    return [
        r for r in repositories
        if isinstance(r, dict)
        and not r.get("private", True)
        and not r.get("fork", True)
        and r.get("name") != OWNER
        and str((r.get("owner") or {}).get("login", "")).lower() == OWNER.lower()
    ]


def _when(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result.astimezone(timezone.utc) if result.tzinfo else result.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def month_history(repos: list[dict], now: datetime) -> list[tuple[str, int]]:
    current = now.year * 12 + now.month - 1
    periods = []
    for index in range(current - 11, current + 1):
        year, month0 = divmod(index, 12)
        periods.append((year, month0 + 1))
    counts = Counter()
    for repo in repos:
        created = _when(repo.get("created_at"))
        if created is not None:
            counts[(created.year, created.month)] += 1
    return [(f"{y:04d}-{m:02d}", counts[(y, m)]) for y, m in periods]


def get_snapshot(repositories: list[dict], now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    public = [
        r for r in repositories
        if isinstance(r, dict)
        and r.get("private") is False
        and str((r.get("owner") or {}).get("login", "")).lower() == OWNER.lower()
    ]
    projects = public_originals(public)
    langs = Counter((str(r.get("language")).strip() if r.get("language") else "Undeclared") for r in projects)
    updated = 0
    for repo in projects:
        stamp = _when(repo.get("pushed_at"))
        if stamp is not None and now - timedelta(days=30) <= stamp <= now:
            updated += 1
    return {
        "updated": now.strftime("%Y-%m-%d %H:%M UTC"),
        "public": len(public),
        "originals": len(projects),
        "python": langs["Python"],
        "updated_30d": updated,
        "langs": dict(sorted(langs.items(), key=lambda item: (-item[1], item[0]))),
        "months": month_history(projects, now),
    }


def fetch_public_repositories(owner: str = OWNER) -> list[dict]:
    """Public /users endpoint; GITHUB_TOKEN is optional and never logged."""
    result: list[dict] = []
    token = os.environ.get("GH_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "KaiserIIII-profile-telemetry",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    for page in range(1, 6):
        query = urllib.parse.urlencode({
            "type": "owner", "sort": "full_name",
            "direction": "asc", "per_page": 100, "page": page,
        })
        url = f"{API}/users/{urllib.parse.quote(owner)}/repos?{query}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.load(response)
        if not isinstance(data, list):
            raise ValueError("GitHub returned no repository list")
        result.extend(data)
        if len(data) < 100:
            break
    else:
        raise RuntimeError("Repository pagination exceeded five pages")
    if not result:
        raise RuntimeError("GitHub returned zero public repositories; refuse to publish")
    return result


# Warm editorial design system: deterministic SVG, no remote assets and no JS.
PAPER = "#F8F5EF"
CARD = "#FFFCF7"
INK = "#342F2B"
MUTED = "#736B63"
FAINT = "#E5DBCD"
ACCENT = "#C67858"
SAGE = "#667D70"
BLUE = "#697F98"
PLUM = "#8A748A"
PALETTE = [ACCENT, SAGE, BLUE, PLUM, "#B4996F", "#8D938D"]


def rect(x, y, w, h, fill=CARD, radius=0, stroke="none", sw=0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def line(x, y, end_x, end_y, color=FAINT, width=1):
    return (f'<path d="M{x} {y}L{end_x} {end_y}" fill="none" '
            f'stroke="{color}" stroke-width="{width}"/>')


def label(x, y, value, size=16, color=INK, weight=400, anchor=None, serif=False):
    attrs = (f'x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
             f'fill="{color}" font-family="{"Georgia,Times New Roman,serif" if serif else "Segoe UI,Arial,sans-serif"}"')
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    return f'<text {attrs}>{escape(str(value))}</text>'


def svg_open(width, height, accessible_name):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(accessible_name, quote=True)}">'
            + rect(0, 0, width, height, PAPER, 20))


def valid_svg(parts):
    svg = "".join(parts) + "</svg>\n"
    ET.fromstring(svg)
    return svg


def draw_hero():
    p = [svg_open(1200, 344, "Yue Yu. Engineering management and computer science.")]
    p += [
        rect(44, 43, 5, 257, ACCENT, 2),
        label(71, 65, "K A I S E R    /    PERSONAL ENGINEERING NOTEBOOK", 15, ACCENT, 650),
        label(68, 153, "Yue Yu.", 84, INK, 500, serif=True),
        label(71, 199, "于越  ·  Engineering Management × Computer Science", 19, MUTED, 500),
        line(71, 219, 680, 219),
        label(71, 260, "I build systems that can be used, inspected and explained.", 23, INK, 500),
        label(72, 299, "Products     /     Verification     /     Research artifacts", 16, MUTED),
    ]
    # A technical monogram drawn from an actual parametric vector construction,
    # rather than a logo image or a generic third-party GitHub badge.
    p.append('<g fill="none" stroke-width="1.5">')
    for radius in (61, 89, 118, 149):
        p.append(f'<circle cx="1020" cy="171" r="{radius}" stroke="{FAINT}"/>')
    p.append(f'<path d="M871 171C944 92 1091 250 1169 171" stroke="{ACCENT}" stroke-width="2.5"/>')
    p.append(f'<path d="M1020 22C1105 115 938 236 1020 320" stroke="{BLUE}" stroke-width="1.5"/>')
    p.append("</g>")
    for x, y, color in ((871,171,ACCENT),(1020,22,BLUE),(1169,171,ACCENT),(1020,320,BLUE)):
        p.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{color}"/>')
    p += [
        rect(975, 128, 90, 88, CARD, 18, FAINT, 1.3),
        label(1020, 184, "K", 59, INK, 500, "middle", True),
        label(1020, 336, "DESIGNED IN CODE", 12, MUTED, 600, "middle"),
    ]
    return valid_svg(p)


def draw_capability_map():
    p = [svg_open(1200, 652, "Diagram connecting technical capabilities to representative repositories.")]
    p += [label(50, 65, "A capability map, backed by code.", 38, INK, 500, serif=True),
          label(51, 94, "Connections describe relevant implementation evidence—not ability scores.", 16, MUTED),
          label(52, 139, "CAPABILITY", 13, ACCENT, 700),
          label(823, 139, "EVIDENCE / PUBLIC CODE", 13, ACCENT, 700)]
    left = [
        ("Systems architecture", "service boundaries, state & interfaces"),
        ("Data & protocols", "storage, parsing and external I/O"),
        ("Verification", "reproductions, tests and CI"),
        ("Research engineering", "repeatability and explicit limits"),
    ]
    right = [
        ("CardCraft", "Godot / Steam / multiplayer"),
        ("Zhixu", "FastAPI / RAG / workflows"),
        ("WiFiScope", "network evidence / PCAP"),
        ("MigrationWitness", "PostgreSQL / contract tests"),
        ("Cost Analyzer", "BOQ / Decimal calculations"),
        ("ReproShift", "reproducible experiments"),
    ]
    left_y = [197 + i * 104 for i in range(4)]
    right_y = [175 + i * 72 for i in range(6)]
    # Source -> proof edges (capability index, public project index).
    edges = [(0,0),(0,1),(0,4),(1,1),(1,2),(1,3),(1,4),(2,0),(2,2),(2,3),(3,3),(3,5)]
    for a, b in edges:
        y1, y2 = left_y[a], right_y[b]
        color = PALETTE[a]
        p.append(f'<path d="M399 {y1} C535 {y1}, 656 {y2}, 797 {y2}" '
                 f'fill="none" stroke="{color}" stroke-width="1.7" opacity=".65"/>')
    for i, ((name, detail), cy) in enumerate(zip(left, left_y)):
        y = cy - 34
        p += [rect(50, y, 346, 72, CARD, 11, FAINT, 1),
              rect(50, y, 4, 72, PALETTE[i], 2),
              label(68, y+29, name, 21, INK, 650),
              label(68, y+54, detail, 14, MUTED),
              f'<circle cx="399" cy="{cy}" r="4" fill="{PALETTE[i]}"/>']
    for j, ((name, detail), cy) in enumerate(zip(right, right_y)):
        y = cy - 29
        p += [rect(802, y, 351, 61, CARD, 11, FAINT, 1),
              f'<circle cx="797" cy="{cy}" r="4" fill="{ACCENT}"/>',
              label(822, y+25, name, 19, INK, 650),
              label(822, y+48, detail, 13, MUTED)]
    p += [line(51, 619, 1152, 619),
          label(51, 640, "LINKED PROJECTS ARE EXAMPLES, NOT A BENCHMARK OF PERSONAL SKILL.", 12, MUTED)]
    return valid_svg(p)


def draw_engineering_loop():
    p = [svg_open(1200, 342, "Automated build pipeline behind this GitHub profile.")]
    p += [label(52, 63, "The engineering behind this page.", 36, INK, 500, serif=True),
          label(53, 91, "A real stdlib-only rendering pipeline: versioned design, validated data, CI, and self-hosted SVG.", 15, MUTED)]
    steps = [
        ("SOURCE", "GitHub public API", "public metadata"),
        ("BOUNDARY", "private → excluded", "type & owner filters"),
        ("MODEL", "UTC + aggregation", "reproducible data"),
        ("DESIGN", "parametric SVG", "no third-party cards"),
        ("VERIFY", "tests + XML parse", "escaping & fixtures"),
        ("PUBLISH", "GitHub Actions", "committed assets"),
    ]
    for i, (kicker, title, detail) in enumerate(steps):
        x = 51 + i * 191
        p += [rect(x, 125, 174, 153, CARD, 12, FAINT, 1),
              rect(x, 125, 174, 3, ACCENT if i in (0,3,5) else BLUE, 1),
              label(x+14, 156, kicker, 12, ACCENT, 700),
              label(x+14, 198, title, 16, INK, 650),
              label(x+14, 229, detail, 13, MUTED)]
        if i < 5:
            p += [line(x+174, 202, x+190, 202, ACCENT, 1.5)]
    p += [label(52, 314, "BUILD CONTRACT", 12, ACCENT, 700),
          label(199, 314, "Never publish private metadata · Never equate counts with skill · Never require external image APIs", 14, MUTED)]
    return valid_svg(p)


def draw_evidence_board():
    p = [svg_open(1200, 565, "Matrix of documented engineering evidence by project.")]
    p += [label(52, 66, "Proof, not badges.", 38, INK, 500, serif=True),
          label(53, 94, "Public artifacts and documented checks; an empty cell is not a failed product.", 16, MUTED)]
    headings = [(65,"PROJECT"),(346,"INSPECTABLE OUTPUT"),(866,"HOSTED CI"),(1002,"REAL CHECK")]
    for x, name in headings:
        p.append(label(x, 143, name, 13, MUTED, 700, "middle" if x > 800 else None))
    data = [
        ("CardCraft", "Steam demo + engineering case notes", False, True),
        ("Zhixu", "Source, test & browser review", True, True),
        ("WiFiScope", "Windows release + CI", True, True),
        ("MigrationWitness", "pg-osc reproduction, PG16/17", True, True),
        ("Construction Cost", "BOQ engine + method notes", True, False),
        ("ReproShift", "Reproducible research artifact", False, False),
    ]
    for i, (name, artifact, ci, real) in enumerate(data):
        y = 158 + i * 58
        p += [rect(50, y, 1099, 49, CARD if i % 2 == 0 else PAPER, 8, FAINT, 0.8),
              label(65, y+30, name, 17, INK, 600),
              label(346, y+30, artifact, 16, MUTED)]
        for x, present in ((866, ci), (1002, real)):
            p.append(f'<circle cx="{x}" cy="{y+25}" r="12" fill="{PALETTE[1] if present else FAINT}"/>')
            p.append(label(x, y+30, "✓" if present else "–", 14,
                           CARD if present else MUTED, 700, "middle"))
    p += [label(53, 538, "Real check: scoped UI, desktop, database or other documented execution. Read project limitations.", 14, MUTED)]
    return valid_svg(p)


def draw_dashboard(s: dict):
    p = [svg_open(1200, 630, "Public GitHub repository metadata and monthly activity, rendered from code.")]
    p += [label(52, 63, "A living data portrait.", 38, INK, 500, serif=True),
          label(53, 92, "Only public original repositories are used for the charts. Creation date ≠ coding activity.", 15, MUTED),
          label(1149, 56, s["updated"], 14, MUTED, 500, "end")]
    metrics = [
        ("PUBLIC REPOSITORIES", s["public"], "includes public forks"),
        ("ORIGINAL PROJECTS", s["originals"], "excludes profile / forks"),
        ("PYTHON PRIMARY", s["python"], "GitHub primary language"),
        ("UPDATED / 30 DAYS", s["updated_30d"], "at least one recent push"),
    ]
    for i, (name, number, hint) in enumerate(metrics):
        x = 51 + i * 283
        p += [rect(x, 116, 267, 112, CARD, 12, FAINT, 1),
              label(x+17, 146, name, 13, MUTED, 700),
              label(x+17, 200, number, 44, INK, 600, serif=True),
              label(x+83, 198, hint, 12, MUTED)]
    p += [rect(51, 248, 520, 322, CARD, 12, FAINT, 1),
          rect(590, 248, 559, 322, CARD, 12, FAINT, 1),
          label(74, 290, "Language landscape", 26, INK, 500, serif=True),
          label(74, 314, "Primary language, original repositories", 14, MUTED),
          label(613, 290, "Repository beginnings", 26, INK, 500, serif=True),
          label(613, 314, "Created each month · rolling 12 months", 14, MUTED)]
    langs = list(s["langs"].items())
    largest = max([1] + [n for _, n in langs])
    for i, (name, count) in enumerate(langs[:5]):
        y = 348 + i*42
        color = PALETTE[i % len(PALETTE)]
        # Escape user-controlled language names: no executable SVG fragments.
        p += [label(75, y+4, name, 15, INK, 500),
              rect(227, y-9, 275, 13, FAINT, 6),
              rect(227, y-9, round(275 * count/largest,2), 13, color, 6),
              label(547, y+4, count, 15, color, 650, "end")]
    months = s["months"]
    maximum = max([1] + [n for _, n in months])
    base_y = 516
    p += [line(619, base_y, 1123, base_y)]
    for i, (date, count) in enumerate(months):
        x = 623 + i * 41
        height = max(2, round(count/maximum * 144))
        y = base_y - height
        color = ACCENT if count == maximum and count else BLUE
        p += [rect(x, y, 23, height, color if count else FAINT, 4),
              label(x+11.5, 541, date[-2:], 12, MUTED, 500, "middle")]
        if count:
            p.append(label(x+11.5, y-8, count, 13, INK, 600, "middle"))
    p += [line(52, 590, 1148, 590),
          label(52, 613, "METHODOLOGY", 12, ACCENT, 700),
          label(195, 613, "GitHub metadata only · not lines of code, contribution counts, skill ratings, or private activity", 13, MUTED)]
    return valid_svg(p)


def create_static_assets(output_dir: Path):
    images = {
        "profile-hero.svg": draw_hero(),
        "project-atlas.svg": draw_capability_map(),
        "engineering-loop.svg": draw_engineering_loop(),
        "evidence-board.svg": draw_evidence_board(),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for file_name, content in images.items():
        path = output_dir / file_name
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
    return images


def main() -> int:
    cli = argparse.ArgumentParser()
    cli.add_argument("--output", default="assets/live-dashboard.svg")
    cli.add_argument("--art-dir", default="assets")
    cli.add_argument("--art-only", action="store_true")
    cli.add_argument("--fixture", help="Optional local test fixture: list of public repository metadata")
    args = cli.parse_args()
    create_static_assets(Path(args.art_dir))
    if args.art_only:
        return 0
    if args.fixture:
        repos = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    else:
        repos = fetch_public_repositories()
    snapshot = get_snapshot(repos)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    new_content = draw_dashboard(snapshot)
    if not out.is_file() or out.read_text(encoding="utf-8") != new_content:
        out.write_text(new_content, encoding="utf-8")
    print(json.dumps({key: value for key, value in snapshot.items() if key not in ("langs", "months")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
