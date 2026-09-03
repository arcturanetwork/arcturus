import json
from pathlib import Path
import unittest
from capstone.security.evidence import EvidenceItem

class SecurityEvidenceTests(unittest.TestCase):
    def test_chain_of_custody_detects_content_change(self):
        item = EvidenceItem("evt-1", b"original"); original = item.digest
        item.record("collector", "acquired", original); self.assertTrue(item.verify())
        item.content = b"changed"; self.assertFalse(item.verify())
        with self.assertRaisesRegex(ValueError, "integrity"): item.record("analyst", "received", original)
    def test_custody_requires_actor_and_action(self):
        with self.assertRaises(ValueError): EvidenceItem("evt-2", b"x").record("", "acquired")
    def test_risk_register_is_complete_and_math_is_consistent(self):
        risks = json.loads(Path("capstone/security/risk-register.json").read_text())["risks"]
        treatments = set()
        for risk in risks:
            self.assertEqual(risk["inherent"], risk["likelihood"] * risk["impact"])
            self.assertLess(risk["residual"], risk["inherent"])
            self.assertTrue(risk["controls"]); self.assertTrue(risk["owner"]); treatments.add(risk["treatment"])
        self.assertTrue(any("accept" in value for value in treatments)); self.assertIn("avoid", treatments)
    def test_stride_and_contract_cover_all_required_categories(self):
        threat = Path("studies/ccsp/threat-model.md").read_text()
        for category in ("Spoofing","Tampering","Repudiation","Information disclosure","Denial of service","Elevation of privilege"):
            self.assertIn(category, threat)
        contract = Path("studies/ccsp/provider-and-contract-review.md").read_text().lower()
        for term in ("right to audit","incident","rto/rpo","data ownership","termination","deletion","exit test"):
            self.assertIn(term, contract)

if __name__ == "__main__": unittest.main()

