import json
from pathlib import Path
import unittest


class NcpGenlScenarioLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.labs = json.loads(Path("studies/ncp-genl/scenario-labs.json").read_text())

    def test_two_scenarios_cover_every_blueprint_domain(self):
        expected = {"model-optimization", "gpu-acceleration", "prompt-engineering", "fine-tuning",
                    "data-preparation", "model-deployment", "evaluation", "monitoring-reliability",
                    "llm-architecture", "safety-ethics-compliance"}
        domains = {lab["domain"] for lab in self.labs}
        self.assertEqual(domains, expected)
        self.assertTrue(all(sum(x["domain"] == d for x in self.labs) == 2 for d in domains))

    def test_scenarios_have_unique_ids_and_evidence(self):
        self.assertEqual(len(self.labs), 20)
        self.assertEqual(len({lab["id"] for lab in self.labs}), 20)
        for lab in self.labs:
            self.assertGreater(lab["minutes"], 0)
            self.assertGreaterEqual(len(lab["must_evidence"]), 4)
            self.assertTrue(lab["trap"])


if __name__ == "__main__":
    unittest.main()
