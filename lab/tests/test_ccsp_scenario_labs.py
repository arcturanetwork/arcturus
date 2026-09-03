import json
from pathlib import Path
import unittest


class CcspScenarioLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.labs = json.loads(Path("studies/ccsp/scenario-labs.json").read_text())

    def test_three_scenarios_cover_every_domain(self):
        expected = {"concepts-architecture-design", "data-security", "platform-infrastructure-security",
                    "application-security", "security-operations", "legal-risk-compliance"}
        domains = {lab["domain"] for lab in self.labs}
        self.assertEqual(domains, expected)
        self.assertTrue(all(sum(x["domain"] == d for x in self.labs) == 3 for d in domains))

    def test_scenarios_have_reasoning_contract(self):
        self.assertEqual(len(self.labs), 18)
        self.assertEqual(len({lab["id"] for lab in self.labs}), 18)
        for lab in self.labs:
            self.assertGreater(lab["minutes"], 0)
            self.assertGreaterEqual(len(lab["must_reason"]), 4)
            self.assertTrue(lab["best_action"]); self.assertTrue(lab["trap"])


if __name__ == "__main__":
    unittest.main()
