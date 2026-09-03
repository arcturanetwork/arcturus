from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from assessments.scenario_exam import (DIMENSIONS, Attempt, append_attempt, bank_digest,
                                       draw, load_bank, readiness_gate, score_attempt)


class ScenarioExamTests(unittest.TestCase):
    def test_all_six_banks_load_with_unique_ids(self):
        for track in ("ncp-aai", "aws-sap", "cka", "ncp-genl", "ccsp", "google-pmle"):
            bank = load_bank(track)
            ids = [str(x.get("id") or f"AWS-{x['task']}") for x in bank]
            self.assertTrue(bank); self.assertEqual(len(ids), len(set(ids))); self.assertTrue(bank_digest(track))

    def test_draw_is_repeatable_and_spans_groups(self):
        first, second = draw("google-pmle", 6, 42), draw("google-pmle", 6, 42)
        self.assertEqual(first, second)
        self.assertEqual(len({x["section"] for x in first}), 6)

    def test_score_requires_complete_bounded_rubric(self):
        scenarios = draw("ncp-aai", 2, 1)
        ratings = {x["id"]: {dimension: 2 for dimension in DIMENSIONS} for x in scenarios}
        result = score_attempt("ncp-aai", scenarios, ratings, "2026-09-03", 10,
                               ["evidence/run-1.json"], [])
        self.assertEqual(result.rate, 1); self.assertTrue(result.within_time)
        ratings[scenarios[0]["id"]]["safety"] = 3
        with self.assertRaisesRegex(ValueError, "0 to 2"):
            score_attempt("ncp-aai", scenarios, ratings, "2026-09-03", 10, [], [])

    def test_gate_requires_two_timed_evidenced_attempts_seven_days_apart(self):
        def attempt(day, errors=()):
            return Attempt("ccsp", day, ("CCSP-01",), 9, 10, 7, 8,
                           (f"evidence/{day}.md",), errors, "digest")
        self.assertFalse(readiness_gate([attempt("2026-09-01"), attempt("2026-09-05")])["ready"])
        self.assertTrue(readiness_gate([attempt("2026-09-01"), attempt("2026-09-08")])["ready"])
        self.assertFalse(readiness_gate([attempt("2026-09-01", ("scope",)),
                                         attempt("2026-09-08", ("scope",))])["ready"])

    def test_history_is_append_only_at_api_level(self):
        record = Attempt("cka", "2026-09-03", ("CKA-S01",), 9, 10, 6, 7,
                         ("evidence/cka.md",), (), "digest")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "attempts.json"
            append_attempt(path, record); append_attempt(path, record)
            self.assertEqual(len(json.loads(path.read_text())), 2)


if __name__ == "__main__": unittest.main()
