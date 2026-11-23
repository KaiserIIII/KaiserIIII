import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=(ROOT/"experience"/"data.js").read_text(encoding="utf8")
APP=(ROOT/"experience"/"app.js").read_text(encoding="utf8")
HTML=(ROOT/"experience"/"index.html").read_text(encoding="utf8")
class PortfolioContentTests(unittest.TestCase):
    def test_language_and_public_projects(self):
        self.assertIn("en: {",DATA);self.assertIn("zh: {",DATA)
        self.assertIn("东北林业大学",DATA)
        self.assertIn("Northeast Forestry University",DATA)
        self.assertEqual(DATA.count('field:"'),10)
        self.assertIn("data-i18n",HTML)
    def test_source_backed_claims(self):
        for claim in ("store.steampowered.com/app/4338300","zhixu/blob/main/docs/verification.md","migrationwitness/blob/main/CROSS_VERSION_RESULTS.md","WiFiScope/releases/latest"):
            self.assertIn(claim,HTML+DATA)
        self.assertIn("120 backend + 33 frontend tests",HTML+DATA)
        self.assertIn("source is private",DATA.lower())
    def test_personal_not_recruiter_only(self):
        self.assertNotIn("For recruiters / HR",HTML+DATA)
        self.assertNotIn("Graduate admissions",HTML+DATA)
        self.assertIn("And understanding them.",HTML)
    def test_safe_text_rendering(self):
        self.assertNotIn(".innerHTML =",APP)
        self.assertNotIn("eval(",APP)
        self.assertIn("textContent",APP)
if __name__=="__main__":unittest.main()
