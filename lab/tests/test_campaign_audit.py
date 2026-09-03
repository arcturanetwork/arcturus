from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from assessments.campaign_audit import audit, platform_gate


class CampaignAuditTests(unittest.TestCase):
    def test_platform_gate_fails_pending_or_missing_proof(self):
        requirements = [{"id":"a", "status":"pending", "proof":[]},
                        {"id":"b", "status":"verified", "proof":["missing.json"]}]
        result = platform_gate(requirements)
        self.assertFalse(result["ready"]); self.assertEqual(result["pending"], ["a", "b"])

    def test_platform_gate_accepts_only_existing_verified_proof(self):
        with TemporaryDirectory() as directory:
            proof = Path(directory) / "run.json"; proof.write_text("{}")
            result = platform_gate([{"id":"lab", "status":"verified", "proof":["run.json"]}],
                                   Path(directory))
            self.assertTrue(result["ready"])

    def test_campaign_is_fail_closed_without_real_attempts_and_platform_runs(self):
        report = audit(date(2026, 9, 3))
        self.assertFalse(report["all_certifications_ready"])
        self.assertTrue(all(not x["ready"] for x in report["tracks"]))
        self.assertTrue(all(x["gates"]["objective_coverage"] for x in report["tracks"]))
        self.assertTrue(all(not x["gates"]["scenario"] for x in report["tracks"]))
        self.assertTrue(all(not x["gates"]["platform"] for x in report["tracks"]))


if __name__ == "__main__": unittest.main()
