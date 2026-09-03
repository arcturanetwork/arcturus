from json import loads
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]


class NvidiaPlatformRunbookTests(unittest.TestCase):
    def test_runbook_is_safe_current_and_evidence_gated(self):
        text = (ROOT / "studies/ncp-aai/free-nvidia-platform-runbook.md").read_text()
        for required in (
            "nvidia-nat[eval]", "nvidia-nat[profiler]", "nvidia-nat[security]",
            "nemoguardrails", "integrate.api.nvidia.com/v1/chat/completions",
            "Never run `echo $NVIDIA_API_KEY`", "failure", "secret scanning",
            "no credentialed request was made",
        ):
            self.assertIn(required, text)
        self.assertNotIn("nvidia-nat[profiling]", text)

    def test_community_repo_audit_is_pinned_and_reconciled(self):
        report = loads((ROOT / "resources/audits/akshan-ncp-aai.json").read_text())
        self.assertEqual(len(report["audited_commit"]), 40)
        counts = report["declared_and_observed_counts"]
        self.assertEqual((counts["modules"], counts["labs"], counts["capstones"]), (13, 12, 2))
        self.assertEqual(sum(counts["question_breakdown"].values()), counts["practice_questions"])
        self.assertEqual(report["adoption_decision"], "reference_and_reimplement")


if __name__ == "__main__":
    unittest.main()
