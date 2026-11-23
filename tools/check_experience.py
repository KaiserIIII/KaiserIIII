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
    if p.files!=["./data.js","./app.js"]:raise RuntimeError("Unexpected remote or inline script")
    for name in ("data.js","app.js"):
        subprocess.run(["node","--check",str(FOLDER/name)],check=True)
    for name in ("styles.css","favicon.svg","cover.svg"):
        if not (FOLDER/name).is_file():raise RuntimeError("Missing local asset "+name)
    if "prefers-reduced-motion" not in (FOLDER/"styles.css").read_text(encoding="utf8"):raise RuntimeError("Missing reduced-motion rules")
    print("Local asset, syntax and accessibility source gates passed")
if __name__=="__main__":main()
