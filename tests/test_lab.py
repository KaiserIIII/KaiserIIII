import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/"experience"/"index.html").read_text(encoding="utf8")
ENGINE=(ROOT/"experience"/"lab-engine.js").read_text(encoding="utf8")
UI=(ROOT/"experience"/"lab-ui.js").read_text(encoding="utf8")
CSS=(ROOT/"experience"/"styles.css").read_text(encoding="utf8")
class ReliabilityLabTests(unittest.TestCase):
 def test_semantic_controls_and_accessible_tabs(self):
  for marker in ('id="lab"','id="lab-workbench"','role="tablist"',
                 'id="lab-tab-permission"','id="lab-tab-retrieval"',
                 'id="lab-form-permission"','id="lab-form-retrieval"',
                 'id="lab-reapply"','id="lab-scoped"','id="lab-query"',
                 'id="lab-verdict"','id="lab-checks"','id="lab-trace"',
                 'id="lab-copy-status"','id="lab-evidence-link"'):
   self.assertIn(marker,HTML)
  self.assertIn('aria-live="polite"',HTML)
  self.assertIn('src="./lab-engine.js"',HTML)
  self.assertIn('src="./lab-ui.js"',HTML)
 def test_model_has_scoped_access_and_independent_checks(self):
  for token in ('tenant==="public"','scoped','unauthorized','expected','actual','missing','trace','pass'):
   self.assertIn(token,ENGINE)
  self.assertIn('docs.filter',ENGINE)
  self.assertIn('expected.map',ENGINE)
  self.assertIn('module.exports',ENGINE)
  self.assertIn('Synthetic',ENGINE+" synthetic")
 def test_safe_and_bilingual_rendering(self):
  for token in ('navLab','labTitle','labBoundary','labEvidence','labTrace',
                'zh:{','en:{','selectMode','popstate','textContent','replaceChildren',
                'role','lab-query','KAISER_LAB'):
   self.assertIn(token,UI)
  for token in ('.innerHTML','window.eval(','globalThis.eval(','new Function(','fetch(','XMLHttpRequest'):
   self.assertNotIn(token,UI+ENGINE)
 def test_visual_system_and_mobile(self):
  self.assertIn('.lab-workbench',CSS)
  self.assertIn('@media(max-width:660px)',CSS)
  self.assertIn('.lab-verdict[data-status=fail]',CSS)
 def test_links_go_to_actual_sources_and_simulation_disclaimed(self):
  self.assertIn('KaiserIIII/migrationwitness/blob/main/PG_OSC_197_RESULTS.md',HTML+UI)
  self.assertIn('KaiserIIII/zhixu/blob/main/docs/verification.md',UI)
  self.assertIn('deliberately simplified teaching models',UI)
  self.assertIn('虚构',UI)
if __name__=="__main__":unittest.main()
