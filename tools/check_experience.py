#!/usr/bin/env python3
"""Check the source contract for the standalone GitHub Pages app."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/"experience"
class Scripts(HTMLParser):
    def __init__(self):super().__init__();self.files=[]
    def handle_starttag(self,tag,attrs):
        if tag=="script":self.files.append(dict(attrs).get("src"))
def main():
    page=(FOLDER/"index.html").read_text(encoding="utf8")
    p=Scripts();p.feed(page)
    if p.files!=["./data.js","./blueprints.js","./app.js","./casebook.js","./compare.js","./lab-engine.js","./lab-ui.js"]:raise RuntimeError("Unexpected remote or inline script")
    for name in ("data.js","blueprints.js","app.js","casebook.js","compare.js","lab-engine.js","lab-ui.js"):
        subprocess.run(["node","--check",str(FOLDER/name)],check=True)
    for name in ("styles.css","favicon.svg","cover.svg"):
        if not (FOLDER/name).is_file():raise RuntimeError("Missing local asset "+name)
    if "prefers-reduced-motion" not in (FOLDER/"styles.css").read_text(encoding="utf8"):raise RuntimeError("Missing reduced-motion rules")
    assets=("index.html","styles.css","data.js","blueprints.js","app.js","casebook.js","compare.js","lab-engine.js","lab-ui.js","favicon.svg","cover.svg")
    raw_bytes=sum((FOLDER/name).stat().st_size for name in assets)
    if raw_bytes >= 230_000:
        raise RuntimeError(f"Static source exceeds 200 KB raw budget: {raw_bytes:,} bytes")
    print(f"Static source: {raw_bytes:,} bytes across {len(assets)} files, budget 230,000 bytes")
    print("Local asset, syntax and accessibility source gates passed")
if __name__=="__main__":main()
