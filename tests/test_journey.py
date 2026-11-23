import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/"experience"/"index.html").read_text(encoding="utf8")
JS=(ROOT/"experience"/"journey.js").read_text(encoding="utf8")
CSS=(ROOT/"experience"/"styles.css").read_text(encoding="utf8")
DATA=(ROOT/"experience"/"data.js").read_text(encoding="utf8")

class GuidedFieldNotesTests(unittest.TestCase):
    def test_semantic_opt_in_navigation(self):
        for anchor in ('id="journey-launch"','id="journey-dialog"',
                       'id="journey-chooser"','id="journey-reader"',
                       'id="journey-choices"','id="journey-title"',
                       'id="journey-action"','id="journey-rail"',
                       'id="journey-share-status"','id="journey-evidence-links"'):
            self.assertIn(anchor,HTML)
        self.assertIn('aria-haspopup="dialog"',HTML)
        self.assertIn('src="./journey.js"',HTML)
        self.assertIn('id="journey-chooser-label"',HTML)
        self.assertIn('id="journey-dialog-label"',HTML)
    def test_three_different_paths_and_public_evidence(self):
        self.assertIn('id:"ship"',JS)
        self.assertIn('id:"verify"',JS)
        self.assertIn('id:"bridge"',JS)
        self.assertEqual(JS.count('action:"case"'),7)
        self.assertEqual(JS.count('action:"lab"'),2)
        self.assertEqual(JS.count('action:"compare"'),1)
        for project in ('cardcraft','zhixu','migrationwitness','reproshift','cost','wifiscope'):
            self.assertIn('project:"'+project+'"',JS)
            self.assertIn('id:"'+project+'"',DATA)
        self.assertIn('p?.links',JS)
        self.assertIn('evidence',JS.lower())
    def test_bilingual_and_interaction_actions(self):
        for marker in ('Take a guided look','跟着故事逛一圈','Make it real','为什么', 'selectMode','setPair',
                       'KAISER_CASEBOOK','history.replaceState',
                       'searchParams.set("trail"','showModal','popstate',
                       'kaiser:language','aria-pressed'):
            self.assertIn(marker,JS)
        self.assertIn('noopener noreferrer',JS)
        self.assertIn('textContent',JS)
        self.assertIn('replaceChildren',JS)
        self.assertIn('disabled=index===0',JS)
    def test_no_private_scoring_or_remote_scripts(self):
        for content in (HTML,JS):
            for unwanted in ('KaiserIIII/CampusScopePro','KaiserIIII/sliver-master',
                             'google-analytics','googletagmanager',
                             'eval(','new Function(','.innerHTML'):
                self.assertNotIn(unwanted,content)
    def test_reduced_motion_mobile_and_failure_fallback(self):
        self.assertIn('body:not(.js) .journey-launch{display:none}',CSS)
        self.assertIn('.journey-reader[hidden]{display:none!important}',CSS)
        self.assertIn('@media(max-width:660px)',CSS)
        self.assertIn('prefers-reduced-motion:reduce',CSS)

if __name__=="__main__":
    unittest.main()
