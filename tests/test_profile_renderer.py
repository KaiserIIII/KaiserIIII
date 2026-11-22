import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from tools.render_live_metrics import get_snapshot, public_originals, month_history, draw_dashboard

NOW = datetime(2026, 11, 23, tzinfo=timezone.utc)

def repo(name, language, created, *, fork=False, private=False, pushed="2026-11-22T00:00:00Z", owner="KaiserIIII"):
    return {
        "name": name, "language": language, "created_at": created,
        "pushed_at": pushed, "fork": fork, "private": private,
        "owner": {"login": owner},
    }

class PublicMetadataTests(unittest.TestCase):
    def setUp(self):
        self.repos = [
            repo("project-a", "Python", "2026-10-01T00:00:00Z"),
            repo("project-b", "GDScript", "2026-11-01T00:00:00Z"),
            repo("fork-one", None, "2026-11-01T00:00:00Z", fork=True),
            repo("KaiserIIII", None, "2026-10-01T00:00:00Z"),
            repo("secret", "Go", "2026-11-01T00:00:00Z", private=True),
            repo("someone-else", "JavaScript", "2026-11-01T00:00:00Z", owner="other"),
        ]
    def test_private_and_foreign_excluded(self):
        result = get_snapshot(self.repos, NOW)
        self.assertEqual((result["public"], result["originals"], result["python"]), (4, 2, 1))
        self.assertEqual(result["updated_30d"], 2)
        self.assertNotIn("Go", result["langs"])
        self.assertNotIn("JavaScript", result["langs"])
    def test_time_buckets(self):
        result = month_history(public_originals(self.repos), NOW)
        self.assertEqual(result[-2:], [("2026-10", 1), ("2026-11", 1)])
        self.assertEqual(len(result), 12)
    def test_standalone_svg(self):
        svg = draw_dashboard(get_snapshot(self.repos, NOW))
        ET.fromstring(svg)
        self.assertIn("PUBLIC REPOS", svg)
        self.assertNotIn("<script", svg)
        self.assertNotIn("secret", svg)
    def test_missing_timestamps_fail_closed(self):
        items = [repo("x", "Python", "not a timestamp", pushed="invalid")]
        self.assertEqual(get_snapshot(items, NOW)["updated_30d"], 0)
        self.assertEqual(month_history(items, NOW)[-1], ("2026-11", 0))
    def test_generated_chart_escapes_untrusted_language_labels(self):
        items = [repo("x", "<script>alert(1)</script>", "2026-10-01T00:00:00Z")]
        svg = draw_dashboard(get_snapshot(items, NOW))
        ET.fromstring(svg)
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)

if __name__ == "__main__":
    unittest.main()
