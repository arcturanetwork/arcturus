from datetime import date
import json
from pathlib import Path
import unittest

from assessments.blueprint_audit import audit


class BlueprintAuditTests(unittest.TestCase):
    def test_registry_has_six_unique_primary_sources_and_structures(self):
        tracks = json.loads(Path("resources/certification-registry.json").read_text())["tracks"]
        self.assertEqual(len(tracks), 6)
        self.assertEqual(len({x["id"] for x in tracks}), 6)
        self.assertTrue(all(x["blueprint_url"].startswith("https://") for x in tracks))
        self.assertTrue(all(x["objective_structure"] for x in tracks))

    def test_current_published_tracks_pass_source_checks(self):
        report = audit(date(2026, 9, 3))
        by_id = {x["id"]: x for x in report["tracks"]}
        for track in ("cka", "ccsp", "google-pmle"):
            self.assertTrue(by_id[track]["booking_ready"])

    def test_prelaunch_and_provisional_targets_block_booking(self):
        report = audit(date(2026, 9, 3))
        by_id = {x["id"]: x for x in report["tracks"]}
        for track in ("ncp-aai", "ncp-genl", "aws-sap"):
            self.assertFalse(by_id[track]["booking_ready"])
            self.assertIn("target blueprint is provisional or prelaunch", by_id[track]["blockers"])

    def test_sources_become_stale_after_three_days(self):
        report = audit(date(2026, 9, 7))
        self.assertTrue(all(not x["source_current"] for x in report["tracks"]))
        self.assertFalse(report["all_booking_ready"])


if __name__ == "__main__": unittest.main()
