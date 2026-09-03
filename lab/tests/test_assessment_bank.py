import unittest
from assessments.quiz import load_bank, score

class AssessmentBankTests(unittest.TestCase):
    def setUp(self): self.bank = load_bank()
    def test_unique_ids_and_valid_answers(self):
        self.assertEqual(len({q["id"] for q in self.bank}), len(self.bank))
        for q in self.bank:
            self.assertGreaterEqual(len(q["choices"]), 4)
            self.assertIn(q["answer"], range(len(q["choices"])))
            self.assertTrue(q["rationale"])
    def test_each_track_has_four_questions_and_multiple_domains(self):
        tracks = {q["track"] for q in self.bank}
        self.assertEqual(tracks, {"ncp-aai","aws-sap","cka","ncp-genl","ccsp","google-pmle"})
        for track in tracks:
            selected = [q for q in self.bank if q["track"] == track]
            self.assertEqual(len(selected), 4)
            self.assertGreaterEqual(len({q["domain"] for q in selected}), 4)
    def test_perfect_and_empty_scores(self):
        perfect = {q["id"]: q["answer"] for q in self.bank}
        self.assertEqual(score(perfect)["rate"], 1)
        empty = score({})
        self.assertEqual(empty["correct"], 0); self.assertEqual(len(empty["missed"]), 24)

if __name__ == "__main__": unittest.main()

