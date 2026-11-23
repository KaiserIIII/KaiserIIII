import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/"experience"/"index.html").read_text(encoding="utf8")
ENGINE=(ROOT/"experience"/"search-engine.js").read_text(encoding="utf8")
APP=(ROOT/"experience"/"app.js").read_text(encoding="utf8")
CSS=(ROOT/"experience"/"styles.css").read_text(encoding="utf8")
DATA=(ROOT/"experience"/"data.js").read_text(encoding="utf8")
class EvidenceSearchTests(unittest.TestCase):
 def test_native_palette_is_upgraded_not_duplicated(self):
  self.assertEqual(HTML.count('id="command-dialog"'),1)
  for name in ("command-prompts","command-query-status","command-preview",
               "command-preview-proof","command-preview-boundary",
               "command-evidence-link","command-explore"):
   self.assertIn('id="'+name+'"',HTML)
  self.assertIn('src="./search-engine.js"',HTML)
  self.assertLess(HTML.index('src="./search-engine.js"'),HTML.index('src="./app.js"'))
 def test_search_uses_actual_public_evidence_and_limits(self):
  self.assertIn("searchEngine.inspect(query,data.projects,locale",APP)
  self.assertIn("match.evidence",APP)
  self.assertIn("match.limitation",APP)
  self.assertIn("project.links",APP)
  self.assertIn("projectText(project).proof",APP)
  self.assertIn("projectText(project).note",APP)
  self.assertIn("KAISER_CASEBOOK.open",APP)
  self.assertIn('role:"option"',APP)
 def test_local_only_and_rejects_unknown_text(self):
  for source in (ENGINE,APP):
   for danger in ("new Function(","XMLHttpRequest(","window.eval(","fetch(",".innerHTML"):
    self.assertNotIn(danger,source)
  self.assertIn("results:corpus.slice",ENGINE)
  self.assertIn("results.filter(r=>r.score>0",ENGINE)
  self.assertIn("No public project evidence matched",APP)
  self.assertIn("没有找到匹配",APP)
 def test_bilingual_semantics_no_skill_scoring(self):
  for phrase in ("数据库正确性","Published & usable work","reasons","evidence","limitation"):
   self.assertIn(phrase,ENGINE)
  self.assertIn("项目资料",ENGINE)
  self.assertIn("Search the work & evidence",DATA)
  self.assertIn("探索项目与公开证据",DATA)
  self.assertIn("not AI-generated",APP)
  self.assertNotIn("competence: ",ENGINE)
 def test_accessibility_and_responsive_style(self):
  self.assertIn('aria-live="polite"',HTML)
  self.assertIn('role="listbox"',HTML)
  self.assertIn("role:\"option\"",APP)
  self.assertIn(".command-preview[hidden]{display:none!important}",CSS)
  self.assertIn("@media(max-width:660px)",CSS)
if __name__=="__main__":unittest.main()
