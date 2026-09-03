import json
from pathlib import Path
import unittest


class GooglePmleScenarioLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.labs = json.loads(Path("studies/google-pmle/scenario-labs.json").read_text())

    def test_three_scenarios_cover_every_guide_section(self):
        expected = {"low-code-ai", "collaboration-data-models", "scaling-models",
                    "serving-scaling", "pipelines-retraining", "risk-monitoring"}
        sections = {lab["section"] for lab in self.labs}
        self.assertEqual(sections, expected)
        self.assertTrue(all(sum(x["section"] == s for x in self.labs) == 3 for s in sections))

    def test_scenarios_have_evidence_contract(self):
        self.assertEqual(len(self.labs), 18)
        self.assertEqual(len({lab["id"] for lab in self.labs}), 18)
        for lab in self.labs:
            self.assertGreater(lab["minutes"], 0)
            self.assertGreaterEqual(len(lab["must_evidence"]), 4)
            self.assertTrue(lab["decision"]); self.assertTrue(lab["trap"])


if __name__ == "__main__":
    unittest.main()
