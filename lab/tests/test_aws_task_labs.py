import unittest
from assessments.task_lab import coverage, load_labs

class AwsTaskLabTests(unittest.TestCase):
    def setUp(self): self.labs = load_labs()
    def test_every_c02_task_has_exactly_one_lab(self):
        expected = {f"1.{i}" for i in range(1,6)} | {f"2.{i}" for i in range(1,7)} | {f"3.{i}" for i in range(1,6)} | {f"4.{i}" for i in range(1,5)}
        actual = [lab["task"] for lab in self.labs]
        self.assertEqual(set(actual),expected); self.assertEqual(len(actual),len(set(actual)))
    def test_each_lab_has_constraints_rubric_points_and_trap(self):
        for lab in self.labs:
            self.assertGreaterEqual(len(lab["must_address"]),5); self.assertTrue(lab["brief"]); self.assertTrue(lab["trap"])
    def test_coverage_is_honest_about_semantic_limit(self):
        report = coverage("Transit Gateway with segmented route tables and Direct Connect", self.labs[0])
        self.assertGreater(report["mentioned"],0); self.assertIn("does not prove",report["warning"])

if __name__ == "__main__": unittest.main()

