import unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/"experience"/"index.html").read_text(encoding="utf8")
JS=(ROOT/"experience"/"app.js").read_text(encoding="utf8")
DATA=(ROOT/"experience"/"data.js").read_text(encoding="utf8")
CSS=(ROOT/"experience"/"styles.css").read_text(encoding="utf8")
class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.duplicates=[];self.links=[];self.scripts=[];self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:self.duplicates.append(a["id"])
            self.ids.add(a["id"])
        if tag=="a":self.links.append(a)
        if tag=="script":self.scripts.append(a)
        if tag=="h1":self.h1+=1
class ExperienceTests(unittest.TestCase):
    def setUp(self):
        self.parser=Parser();self.parser.feed(HTML)
    def test_semantics(self):
        self.assertFalse(self.parser.duplicates)
        self.assertEqual(self.parser.h1,1)
        self.assertTrue({"main","hero-title","work","connections","archive","about","contact","relationship-graph","inspector-title","archive-list","command-dialog","casebook-dialog","casebook-stage-buttons","casebook-graphic"}.issubset(self.parser.ids))
    def test_local_resources(self):
        self.assertEqual([s.get("src") for s in self.parser.scripts],["./data.js","./blueprints.js","./app.js","./casebook.js","./compare.js"])
        for f in ("styles.css","data.js","blueprints.js","app.js","casebook.js","compare.js","favicon.svg","cover.svg"):
            self.assertTrue((ROOT/"experience"/f).is_file())
        for a in self.parser.links:
            if a.get("href","").startswith("#"):self.assertIn(a["href"][1:],self.parser.ids)
            if a.get("target")=="_blank":self.assertIn("noopener",a.get("rel",""))
    def test_actual_interactions(self):
        for name in ("setPointerCapture","getScreenCTM","requestAnimationFrame","showModal","setLanguage","renderArchive","renderCommandResults","setMapFilter","IntersectionObserver"):
            self.assertIn(name,JS)
        self.assertIn("prefers-reduced-motion",CSS)
        self.assertIn('class="skip-link"',HTML)
    def test_no_private_source_or_trackers(self):
        for content in (HTML,DATA,JS):
            for forbidden in ("KaiserIIII/CampusScopePro","KaiserIIII/sliver-master","google-analytics","googletagmanager"):
                self.assertNotIn(forbidden,content)
if __name__=="__main__":unittest.main()
