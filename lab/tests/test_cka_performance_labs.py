import json
from pathlib import Path
import unittest

class CkaPerformanceLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.labs = json.loads(Path("studies/cka/performance-labs.json").read_text())
    def test_ids_unique_and_all_domains_present(self):
        self.assertEqual(len({lab["id"] for lab in self.labs}),len(self.labs))
        self.assertEqual({lab["domain"] for lab in self.labs},{"storage","troubleshooting","workloads-scheduling","architecture-install-config","services-networking"})
    def test_published_competency_counts_are_represented(self):
        counts = {domain:sum(lab["domain"]==domain for lab in self.labs) for domain in {lab["domain"] for lab in self.labs}}
        self.assertEqual(counts,{"storage":3,"troubleshooting":5,"workloads-scheduling":5,"architecture-install-config":6,"services-networking":5})
    def test_every_task_has_time_verification_and_risk(self):
        for lab in self.labs:
            self.assertGreater(lab["minutes"],0); self.assertGreaterEqual(len(lab["verify"]),3); self.assertTrue(lab["risk"])

if __name__ == "__main__": unittest.main()

