from datetime import date
import json
from pathlib import Path
import unittest

from capstone.security.governance import (
    Classification, DataAsset, DataPolicy, GovernanceError, accountable_party,
    cryptographic_erase, eligible_for_deletion, validate_placement,
)


class CcspGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.policy = DataPolicy(Classification.RESTRICTED, 30, frozenset({"us-west"}))

    def test_residency_violation_is_rejected(self):
        asset = DataAsset("a", self.policy, date(2026, 1, 1), "eu-central")
        with self.assertRaisesRegex(GovernanceError, "residency"):
            validate_placement(asset)

    def test_retention_expiry_allows_deletion(self):
        asset = DataAsset("a", self.policy, date(2026, 1, 1), "us-west")
        self.assertFalse(eligible_for_deletion(asset, date(2026, 1, 30)))
        self.assertTrue(eligible_for_deletion(asset, date(2026, 1, 31)))

    def test_legal_hold_overrides_expired_retention(self):
        asset = DataAsset("a", self.policy, date(2026, 1, 1), "us-west", legal_hold=True)
        with self.assertRaisesRegex(GovernanceError, "legal hold"):
            cryptographic_erase(asset, date(2027, 1, 1))

    def test_crypto_erase_records_key_and_asset_state(self):
        asset = DataAsset("a", self.policy, date(2026, 1, 1), "us-west")
        cryptographic_erase(asset, date(2026, 2, 1))
        self.assertTrue(asset.deleted)
        self.assertTrue(asset.key_destroyed)

    def test_shared_responsibility_keeps_customer_duties(self):
        self.assertEqual(accountable_party("hypervisor"), "provider")
        self.assertEqual(accountable_party("data_classification"), "customer")
        self.assertEqual(accountable_party("incident_coordination"), "shared")

    def test_control_matrix_has_owner_operator_and_evidence(self):
        controls = json.loads(Path("capstone/security/control-matrix.json").read_text())["controls"]
        self.assertGreaterEqual(len(controls), 10)
        for control in controls:
            self.assertTrue({"id", "objective", "owner", "operator", "evidence"} <= control.keys())


if __name__ == "__main__":
    unittest.main()

