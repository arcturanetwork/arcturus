import json
from pathlib import Path
import unittest


class AwsArchitectureEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(Path("capstone/aws/architecture-manifest.json").read_text())
        cls.dossier = Path("capstone/aws/trustgraph-architecture.md").read_text().lower()

    def test_manifest_covers_all_c02_domains(self):
        for key in ("accounts", "controls", "reliability", "operations", "cost", "migration"):
            self.assertTrue(self.manifest[key], key)

    def test_recovery_has_numeric_objectives_and_restore_test(self):
        requirements = self.manifest["requirements"]
        self.assertGreater(requirements["ingestion_rpo_minutes"], 0)
        self.assertGreater(requirements["query_rto_minutes"], 0)
        self.assertIn("backup-restore-test", self.manifest["reliability"])

    def test_cost_model_includes_transfer_not_just_compute(self):
        self.assertIn("transfer-model", self.manifest["cost"])
        self.assertIn("nat", self.dossier)
        self.assertIn("cross-region", self.dossier)

    def test_scp_is_not_misrepresented_as_permission_grant(self):
        self.assertIn("scps are guardrails, not grants", self.dossier)

    def test_design_does_not_claim_cloud_deployment(self):
        self.assertEqual(self.manifest["evidence_status"], "design-only")
        self.assertIn("not evidence of deployment", self.dossier)


if __name__ == "__main__":
    unittest.main()

