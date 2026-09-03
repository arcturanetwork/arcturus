import unittest

from capstone.agent.load_profile import percentile, summarize


class AgentLoadProfileTests(unittest.TestCase):
    def test_percentiles_use_observed_values_and_validate_input(self):
        values = [1, 2, 3, 4, 100]
        self.assertEqual(percentile(values, .5), 3)
        self.assertEqual(percentile(values, .95), 100)
        with self.assertRaises(ValueError): percentile([], .5)

    def test_summary_exposes_tail_latency_errors_and_correlation(self):
        rows = [{"request_id":"a", "status":200, "latency_ms":1, "expected":True},
                {"request_id":"b", "status":403, "latency_ms":9, "expected":True}]
        report = summarize(rows, 1)
        self.assertEqual(report["throughput_rps"], 2)
        self.assertEqual(report["status_counts"], {"200":1, "403":1})
        self.assertEqual(report["unexpected_outcomes"], 0)
        self.assertTrue(report["correlation_integrity"])

    def test_duplicate_correlation_is_detected(self):
        rows = [{"request_id":"same", "status":200, "latency_ms":1, "expected":True},
                {"request_id":"same", "status":200, "latency_ms":2, "expected":True}]
        self.assertFalse(summarize(rows, 1)["correlation_integrity"])


if __name__ == "__main__": unittest.main()
