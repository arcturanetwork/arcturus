import json
from pathlib import Path
import unittest


class NcpAaiScenarioLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.labs = json.loads(Path("studies/ncp-aai/scenario-labs.json").read_text())

    def test_two_scenarios_cover_each_blueprint_domain(self):
        domains = {lab["domain"] for lab in self.labs}
        self.assertEqual(domains, {"architecture-design", "development", "evaluation-tuning",
                                  "deployment-scaling", "planning-memory", "knowledge-data",
                                  "nvidia-platform", "operations", "safety-compliance",
                                  "human-oversight"})
        self.assertTrue(all(sum(x["domain"] == d for x in self.labs) == 2 for d in domains))

    def test_ids_and_evidence_contract(self):
        self.assertEqual(len({lab["id"] for lab in self.labs}), 20)
        for lab in self.labs:
            self.assertGreater(lab["minutes"], 0)
            self.assertGreaterEqual(len(lab["must_evidence"]), 4)
            self.assertTrue(lab["trap"])


if __name__ == "__main__":
    unittest.main()
