import unittest
from html.parser import HTMLParser
from pathlib import Path
CONTENT=(Path(__file__).resolve().parents[1]/"experience"/"index.html").read_text(encoding="utf8")
class Tags(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.buttons=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if "id" in d:
            assert d["id"] not in self.ids
            self.ids.add(d["id"])
        if tag=="button":self.buttons+=1
class ExperienceTest(unittest.TestCase):
    def test_structure(self):
        p=Tags();p.feed(CONTENT)
        self.assertGreaterEqual(p.buttons,9)
        self.assertTrue({"graph","focus-title","focus-desc","help","focus-evidence"}.issubset(p.ids))
    def test_real_interactions(self):
        for f in ("requestAnimationFrame(tick)","pointermove","pointerdown","keydown","bezier","aria-pressed","prefers-reduced-motion"):
            self.assertIn(f,CONTENT)
    def test_no_private_code_or_external_scripts(self):
        self.assertNotIn("KaiserIIII/CampusScopePro",CONTENT)
        self.assertNotIn("<script src=",CONTENT)
if __name__=="__main__":unittest.main()
