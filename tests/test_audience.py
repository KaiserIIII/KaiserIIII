import unittest
from pathlib import Path
PAGE=(Path(__file__).resolve().parents[1]/"experience"/"index.html").read_text(encoding="utf8")
class BilingualAudienceTests(unittest.TestCase):
    def test_bilingual_and_two_lenses(self):
        for marker in ('data-lang="zh"','data-lang="en"','data-audience="industry"','data-audience="research"','function changeAudience','function refreshLocale','zhProjects='):
            self.assertIn(marker,PAGE)
    def test_verifiable_first_view(self):
        for proof in ("Northeast Forestry University","Engineering Management undergraduate","Steam demo","120 backend + 33 frontend","PostgreSQL 16 / 17"):
            self.assertIn(proof,PAGE)
    def test_real_clipboard_and_no_html_injection(self):
        self.assertIn("navigator.clipboard.writeText(message)",PAGE)
        self.assertIn("textContent=value",PAGE)
        self.assertNotIn(".innerHTML=",PAGE)
        self.assertIn("requestAnimationFrame(tick)",PAGE)
if __name__=="__main__":unittest.main()
