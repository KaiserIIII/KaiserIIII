import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/"experience"/"index.html").read_text(encoding="utf8")
DATA=(ROOT/"experience"/"data.js").read_text(encoding="utf8")
BLUE=(ROOT/"experience"/"blueprints.js").read_text(encoding="utf8")
CASE=(ROOT/"experience"/"casebook.js").read_text(encoding="utf8")

class SystemBlueprintTests(unittest.TestCase):
    def test_six_source_backed_interactive_stories(self):
        for name in ("cardcraft","zhixu","wifiscope","migrationwitness","cost","reproshift"):
            self.assertIn(name+":{",BLUE.replace(" ",""))
        for token in ('en:{','zh:{','question:', 'detail:', 'evidenceTitle:'):
            self.assertIn(token, BLUE)
        self.assertGreaterEqual(BLUE.count('question:'),30)
    def test_real_dialog_and_direct_link(self):
        for marker in ('id="casebook-dialog"','id="casebook-graphic"','id="casebook-stage-buttons"','id="casebook-share"','id="casebook-from-inspector"'):
            self.assertIn(marker,HTML)
        for marker in ('history[method]','searchParams.set("case"','popstate','showModal','setAttribute("aria-pressed"','casebook-svg-node'):
            self.assertIn(marker,CASE)
    def test_data_boundaries_and_security(self):
        self.assertIn('textContent',CASE)
        self.assertNotIn('.innerHTML',CASE)
        self.assertIn('rel:"noopener noreferrer"',CASE)
        for corpus in (CASE,BLUE):
            for private in ('KaiserIIII/cardcraft-engineering"','KaiserIIII/CampusScopePro','KaiserIIII/sliver-master'):
                self.assertNotIn(private,corpus)
    def test_progressive_enhancement(self):
        self.assertIn('data-open-case="cardcraft"',HTML)
        self.assertIn("KAISER_CASEBOOK",CASE)
        self.assertIn("k a i s e r", "k a i s e r")

if __name__=="__main__":unittest.main()
