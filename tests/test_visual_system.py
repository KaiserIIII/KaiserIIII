import unittest
import xml.etree.ElementTree as ET
from tools.render_live_metrics import (
    draw_hero, draw_capability_map, draw_engineering_loop,
    draw_evidence_board, draw_dashboard, get_snapshot,
)

class EditorialVisualTests(unittest.TestCase):
    def test_all_standalone_svgs_parse(self):
        fixture = get_snapshot([], now=__import__("datetime").datetime(2026, 11, 23, tzinfo=__import__("datetime").timezone.utc))
        for maker in (draw_hero, draw_capability_map, draw_engineering_loop, draw_evidence_board):
            with self.subTest(maker=maker.__name__):
                image = maker()
                ET.fromstring(image)
                self.assertTrue(image.startswith("<svg "))
                self.assertIn('viewBox=', image)
                self.assertNotIn("<script", image)
                self.assertNotIn("http://", image)
                self.assertNotIn("#050b19", image)
        ET.fromstring(draw_dashboard(fixture))

    def test_capability_map_contains_real_project_edges(self):
        image = draw_capability_map()
        self.assertIn("C535 ", image)
        for name in ("CardCraft", "Zhixu", "WiFiScope", "MigrationWitness", "Cost Analyzer", "ReproShift"):
            self.assertIn(name, image)

    def test_escaping_of_untrusted_language(self):
        fixture = get_snapshot([
            {"private": False, "fork": False, "name": "x",
             "owner": {"login": "KaiserIIII"},
             "language": '<img src="x" onerror="bad">',
             "created_at": "2026-11-01T00:00:00Z",
             "pushed_at": "2026-11-01T00:00:00Z"}
        ], now=__import__("datetime").datetime(2026, 11, 23, tzinfo=__import__("datetime").timezone.utc))
        svg = draw_dashboard(fixture)
        ET.fromstring(svg)
        self.assertIn("&lt;img", svg)
        self.assertNotIn("<img ", svg)

    def test_profile_is_source_generated(self):
        for image in (draw_hero(), draw_capability_map(), draw_engineering_loop()):
            self.assertIn("#F8F5EF", image)
            self.assertIn("#C67858", image)

if __name__ == "__main__":
    unittest.main()
