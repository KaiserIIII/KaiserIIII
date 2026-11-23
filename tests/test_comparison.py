import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/"experience"/"index.html").read_text(encoding="utf8")
APP=(ROOT/"experience"/"app.js").read_text(encoding="utf8")
COMP=(ROOT/"experience"/"compare.js").read_text(encoding="utf8")
DATA=(ROOT/"experience"/"data.js").read_text(encoding="utf8")
CSS=(ROOT/"experience"/"styles.css").read_text(encoding="utf8")

class ComparisonStudioTests(unittest.TestCase):
    def test_complete_comparison_interface(self):
        for key in ('id="compare"','id="compare-title"','id="compare-studio"',
                    'id="compare-left"','id="compare-right"','id="compare-swap"',
                    'id="compare-share"','id="compare-overlap"',
                    'id="compare-left-proof"','id="compare-right-limit"',
                    'id="compare-visual"'):
            if key == 'id="compare-overlap"':
                self.assertIn('class="compare-overlap"',HTML)
            else:
                self.assertIn(key,HTML)
        self.assertIn('src="./compare.js"',HTML)
        self.assertIn('data-compare-preset="zhixu,migrationwitness"',HTML)
    def test_bilingual_and_truthful_shared_subjects(self):
        for key in ("compareTitle","compareProof","compareBoundary",
                    "compareExplanationSome","compareExplanationNone",
                    "compareLinkCopied","comparePresetThree"):
            self.assertIn(key+":",COMP)
        self.assertIn("No score",COMP)
        self.assertIn("四类主题",COMP)
        self.assertIn("data.domains.filter",COMP)
        self.assertIn("project(left).domains.includes",COMP)
    def test_safe_deep_links_and_render(self):
        for code in ('new Set(data.projects.map','searchParams.set("compare"',
                     'parsePair(', 'popstate','history[method]','textContent',
                     'replaceChildren','rel:"noopener noreferrer"'):
            self.assertIn(code,COMP)
        for dangerous in ('.innerHTML','eval(','new Function(',
                          'KaiserIIII/CampusScopePro','KaiserIIII/sliver-master'):
            self.assertNotIn(dangerous,COMP)
    def test_mobile_index_replaces_overwide_canvas_only_if_js_works(self):
        self.assertIn('id="mobile-project-index"',HTML)
        self.assertIn('function buildMobileIndex()',APP)
        self.assertIn('function updateMobileIndex()',APP)
        self.assertIn('selectProject(project.id',APP)
        self.assertIn('body.js #graph-frame{display:none}',CSS)
        self.assertIn('body.js .mobile-graph-index{display:grid',CSS)
        self.assertIn('aria-pressed',APP)
        self.assertIn('graphGroups.get(next.id).group.focus()',APP)
    def test_project_data_not_modified_for_comparison(self):
        self.assertEqual(DATA.count('field:"'),10)
        for project in ('cardcraft','zhixu','wifiscope','migrationwitness',
                        'cost','reproshift','qldevice','importproof','tta','paperskill'):
            self.assertIn('id:"'+project+'"',DATA)

if __name__=="__main__":
    unittest.main()
