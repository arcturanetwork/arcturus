import unittest
from capstone.llm.training import BytePairTokenizer, EarlyStopping, fairness_report, lora_parameter_count, lora_update

class LlmTrainingTests(unittest.TestCase):
    def test_bpe_learns_repeatable_merges_and_shortens_frequent_word(self):
        tokenizer = BytePairTokenizer(); before = len(tokenizer.encode_word("lower"))
        tokenizer.train(["lower lower lowest", "newer wider"], 6)
        self.assertLess(len(tokenizer.encode_word("lower")), before)
        second = BytePairTokenizer(); second.train(["lower lower lowest", "newer wider"], 6)
        self.assertEqual(tokenizer.merges, second.merges)
    def test_lora_uses_fewer_parameters_at_small_rank(self):
        counts = lora_parameter_count(4096, 4096, 8)
        self.assertLess(counts["lora"], counts["full"])
    def test_lora_update_has_expected_shape_and_scaling(self):
        update = lora_update([[1,2],[3,4]], [[1,0],[0,1],[1,1]], alpha=2)
        self.assertEqual(len(update), 3); self.assertEqual(len(update[0]), 2)
        self.assertEqual(update[0], [1,2])
    def test_early_stopping_resets_only_on_material_improvement(self):
        stop = EarlyStopping(2, .01)
        self.assertFalse(stop.update(1)); self.assertFalse(stop.update(.995)); self.assertTrue(stop.update(.994))
        stop = EarlyStopping(2, .01); stop.update(1); stop.update(1.01)
        self.assertFalse(stop.update(.8)); self.assertEqual(stop.bad_epochs, 0)
    def test_fairness_report_exposes_group_gap_and_limitations(self):
        rows = [{"group":"a","label":1,"prediction":1},{"group":"a","label":0,"prediction":1},
                {"group":"b","label":1,"prediction":0},{"group":"b","label":0,"prediction":0}]
        report = fairness_report(rows)
        self.assertEqual(report["selection_rate_gap"], 1); self.assertTrue(report["limitations"])

if __name__ == "__main__": unittest.main()

