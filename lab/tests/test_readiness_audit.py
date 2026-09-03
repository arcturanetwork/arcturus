import unittest
from assessments.evidence_audit import MAPS, audit

class ReadinessAuditTests(unittest.TestCase):
    def test_all_six_tracks_have_maps(self): self.assertEqual(len(MAPS),6); self.assertTrue(all(path.exists() for path in MAPS.values()))
    def test_campaign_is_not_falsely_ready(self):
        report = audit(); self.assertFalse(report["all_ready"])
        self.assertTrue(all(not item["ready"] for item in report["tracks"].values()))

if __name__ == "__main__": unittest.main()

