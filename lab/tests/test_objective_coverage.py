import unittest

from assessments.objective_coverage import audit, expand_range


class ObjectiveCoverageTests(unittest.TestCase):
    def test_range_expansion_is_inclusive(self):
        self.assertEqual(expand_range("3.1-3.3"), ["3.1", "3.2", "3.3"])

    def test_cross_domain_and_descending_ranges_are_rejected(self):
        for value in ("1.4-2.1", "2.5-2.1", "bad"):
            with self.assertRaises(ValueError): expand_range(value)

    def test_all_numbered_counts_match_maps(self):
        report = audit()
        self.assertTrue(report["all_numbered_coverage_consistent"])
        by_id = {x["id"]: x for x in report["tracks"]}
        self.assertEqual(by_id["ncp-aai"]["expanded"], 53)
        self.assertEqual(by_id["aws-sap"]["expanded"], 20)
        self.assertEqual(by_id["ncp-genl"]["expanded"], 45)
        self.assertEqual(by_id["ccsp"]["expanded"], 38)
        self.assertEqual(by_id["google-pmle"]["expanded"], 14)

    def test_audit_accepts_range_or_individual_map_notation(self):
        report = audit()
        by_id = {x["id"]: x for x in report["tracks"]}
        self.assertEqual(by_id["ncp-aai"]["missing_ranges_in_map"], [])
        self.assertEqual(by_id["aws-sap"]["missing_ranges_in_map"], [])


if __name__ == "__main__": unittest.main()
