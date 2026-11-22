#!/usr/bin/env python3
"""Validate that a self-contained browser prototype has executable JS syntax."""
import re
from pathlib import Path
import subprocess
import tempfile
import sys
src=Path("experience/index.html").read_text(encoding="utf-8")
scripts=re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>",src,re.DOTALL)
if len(scripts)!=1:
    raise SystemExit("Expected exactly one inline application script")
with tempfile.TemporaryDirectory() as folder:
    js=Path(folder)/"app.js"
    js.write_text(scripts[0],encoding="utf-8")
    subprocess.run(["node","--check",str(js)],check=True)
if 'prefers-reduced-motion' not in src:
    raise SystemExit("Missing reduced-motion mode")
if "https://github.com/KaiserIIII" not in src:
    raise SystemExit("Missing public project evidence")
print("Browser JavaScript syntax and static invariants passed")
