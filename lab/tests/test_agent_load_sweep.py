import unittest

from capstone.agent.load_sweep import aggregate, saturation_findings


def trial(workers, throughput, p50, p95, p99, unexpected=0):
    return {"configuration":{"workers":workers}, "throughput_rps":throughput,
            "latency_ms":{"p50":p50, "p95":p95, "p99":p99},
            "unexpected_outcomes":unexpected, "correlation_integrity":True}


class AgentLoadSweepTests(unittest.TestCase):
    def test_aggregate_uses_medians_and_worst_tail(self):
        result = aggregate(5, [trial(5, 10, 1, 5, 8), trial(5, 30, 3, 9, 20),
                               trial(5, 20, 2, 7, 10)])
        self.assertEqual(result["median_throughput_rps"], 20)
        self.assertEqual(result["median_latency_ms"]["p95"], 7)
        self.assertEqual(result["worst_p99_ms"], 20)

    def test_mismatched_worker_group_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "does not match"):
            aggregate(5, [trial(10, 1, 1, 1, 1)])

    def test_saturation_requires_small_gain_and_large_tail_growth(self):
        groups = [aggregate(5, [trial(5, 100, 1, 10, 15)]),
                  aggregate(10, [trial(10, 105, 2, 20, 25)])]
        finding = saturation_findings(groups)
        self.assertEqual(len(finding["saturation_candidates"]), 1)
        self.assertEqual(finding["peak_median_throughput_workers"], 10)


if __name__ == "__main__": unittest.main()
