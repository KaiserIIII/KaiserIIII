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


def label(x: int | float, y: int | float, value: object, size: int = 16,
          color: str = "#dbeafa", weight: int = 400, extra: str = "") -> str:
    return (f'<text x="{x}" y="{y}" font-family="Segoe UI,Arial,sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>'
            f'{escape(str(value))}</text>')


def panel(x: int, y: int, w: int, h: int, fill: str = "#102239") -> str:
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="17" '
            f'fill="{fill}" stroke="#2a4860" stroke-width="1"/>')


def draw_dashboard(s: dict) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 622" '
        'width="1200" height="622" role="img" '
        'aria-label="GitHub public repository counts, language mix and creation timeline">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop stop-color="#050b19"/><stop offset="1" stop-color="#14263d"/>'
        '</linearGradient><linearGradient id="aqua" x1="0" x2="1">'
        '<stop stop-color="#57f6d6"/><stop offset="1" stop-color="#83b9ff"/>'
        '</linearGradient></defs>',
        '<rect width="1200" height="622" rx="16" fill="url(#bg)"/>',
    ]
    parts += [
        label(42, 52, "PUBLIC / ENGINEERING TELEMETRY", 27, "#f2faff", 760, 'letter-spacing="1.3"'),
        label(43, 79, "Source: GitHub REST API  ·  Public repositories only  ·  No private activity", 15, "#99afc6"),
        label(1155, 54, s["updated"], 14, "#62e5cf", 650, 'text-anchor="end"'),
    ]
    metrics = [
        ("PUBLIC REPOS", s["public"], "Public repositories, including forks"),
        ("ORIGINAL PROJECTS", s["originals"], "Excludes forks and profile repository"),
        ("PYTHON PRIMARY", s["python"], "GitHub primary language: Python"),
        ("UPDATED / 30 DAYS", s["updated_30d"], "Non-fork projects with a recent push"),
    ]
    for i, (title, value, hint) in enumerate(metrics):
        x = 41 + i * 282
        parts.append(panel(x, 100, 270, 111))
        parts.append(label(x + 16, 131, title, 13, "#90acc4", 710, 'letter-spacing=".8"'))
        parts.append(label(x + 17, 181, value, 41, "#f5fcff", 770))
        parts.append(label(x + 81, 184, hint[:29], 11, "#83a0b8"))
        parts.append(f'<rect x="{x+16}" y="198" width="237" height="2" rx="1" fill="#24475b"/>')
    parts += [panel(41, 227, 546, 328), panel(606, 227, 553, 328)]
    parts += [
        label(64, 262, "LANGUAGE COMPOSITION", 20, "#edf7ff", 730),
        label(64, 284, "Primary language / unforked public projects", 13, "#8caac1"),
        label(628, 262, "REPOSITORY LAUNCHES", 20, "#edf7ff", 730),
        label(628, 284, "Creation dates / rolling 12 months", 13, "#8caac1"),
    ]
    langs = list(s["langs"].items())
    total = max(1, sum(v for _, v in langs))
    # Standalone SVG with no scripts, fonts, remote resources or animations.
    cx, cy, radius = 215, 409, 88
    circ = math.tau * radius
    offset = 0.0
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#203c51" stroke-width="25"/>')
    for i, (name, count) in enumerate(langs):
        arc = count / total * circ
        if arc <= 0:
            continue
        fill = COLORS[i % len(COLORS)]
        visible = max(0.5, arc - 4)
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
            f'stroke="{fill}" stroke-width="23" stroke-linecap="butt" '
            f'stroke-dasharray="{visible:.2f} {circ-visible:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 {cx} {cy})"/>'
        )
        offset += arc
    parts += [
        label(cx, 411, s["originals"], 43, "#f6faff", 790, 'text-anchor="middle"'),
        label(cx, 433, "PROJECT REPOS", 12, "#93b2c5", 670, 'text-anchor="middle"'),
    ]
    for i, (name, count) in enumerate(langs[:6]):
        y = 331 + i * 38
        fill = COLORS[i % len(COLORS)]
        parts.append(f'<rect x="345" y="{y-14}" width="13" height="13" rx="3" fill="{fill}"/>')
        parts.append(label(368, y-2, name, 15, "#e5f1fc", 560))
        parts.append(label(548, y-2, count, 17, fill, 750, 'text-anchor="end"'))
    months = s["months"]
    peak = max(1, max(count for _, count in months))
    base_y = 502
    parts.append('<path d="M628 502H1138" stroke="#4a667c" stroke-width="1.1"/>')
    for i, (month, count) in enumerate(months):
        x = 634 + i * 42
        height = max(2, round(count / peak * 164))
        y = base_y - height
        opacity = "1" if count else ".22"
        fill = "#67ead6" if count == peak and count else "#719de4"
        parts.append(
            f'<rect x="{x}" y="{y}" width="27" height="{height}" rx="5" '
            f'fill="{fill}" opacity="{opacity}"/>'
        )
        if count:
            parts.append(label(x+13, y-10, count, 14, "#d9f7fc", 680, 'text-anchor="middle"'))
        parts.append(label(x+13, 523, month[-2:], 11, "#86a8c0", 520, 'text-anchor="middle"'))
    parts.append(label(632, 539, f"{months[0][0][:4]}–{months[-1][0][:4]}  ·  MONTH / UTC", 11, "#8ca5bd"))
    parts += [
        label(43, 585, "METHODOLOGY", 12, "#66e8cf", 750, 'letter-spacing="1.1"'),
        label(166, 585, "Metadata counts, not contributions, LOC, seniority or production quality.", 14, "#bbd0e0"),
        label(43, 607, "Includes public forks only in the first total; excludes private repositories entirely. Updated on scheduled workflow runs.", 12, "#829bb5"),
        '</svg>',
    ]
    svg = "".join(parts)
    ET.fromstring(svg)
    return svg + "\n"


def main() -> int:
    cli = argparse.ArgumentParser()
    cli.add_argument("--output", default="assets/live-dashboard.svg")
    cli.add_argument("--fixture", help="Optional local test fixture: list of public repository metadata")
    args = cli.parse_args()
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
