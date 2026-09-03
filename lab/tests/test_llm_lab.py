import unittest

from capstone.llm.lab import (
    clean_dataset, cosine_similarity, dequantize, filtered_distribution, kv_cache_bytes,
    perplexity, quantization_error, rouge_l, sample_token, scaled_dot_product_attention,
    sinusoidal_position, softmax, symmetric_int8,
)


class LlmLabTests(unittest.TestCase):
    def test_softmax_is_stable_and_normalized(self):
        result = softmax([1000, 1001, 1002])
        self.assertAlmostEqual(sum(result), 1.0)
        self.assertGreater(result[2], result[1])

    def test_lower_temperature_sharpens_distribution(self):
        cold = softmax([1, 2, 3], 0.5)
        warm = softmax([1, 2, 3], 2.0)
        self.assertGreater(cold[-1], warm[-1])

    def test_top_k_and_nucleus_filter_and_renormalize(self):
        topk = filtered_distribution([4, 3, 2, 1], top_k=2)
        nucleus = filtered_distribution([4, 3, 2, 1], top_p=0.8)
        self.assertEqual(sum(value > 0 for value in topk), 2)
        self.assertAlmostEqual(sum(nucleus), 1.0)

    def test_sampling_is_reproducible_with_seed(self):
        self.assertEqual(sample_token([1, 2, 3], 7), sample_token([1, 2, 3], 7))

    def test_perplexity_rewards_more_likely_sequence(self):
        self.assertLess(perplexity([0.8, 0.7]), perplexity([0.2, 0.1]))

    def test_rouge_l_uses_sequence_not_bag_of_words(self):
        exact = rouge_l("a b c", "a b c")
        reversed_order = rouge_l("a b c", "c b a")
        self.assertEqual(exact["f1"], 1.0)
        self.assertLess(reversed_order["f1"], exact["f1"])

    def test_int8_quantization_reports_accuracy_tradeoff(self):
        original = [-2.0, -0.3, 0.0, 0.7, 2.0]
        quantized, scale = symmetric_int8(original)
        error = quantization_error(original, dequantize(quantized, scale))
        self.assertLessEqual(max(map(abs, quantized)), 127)
        self.assertGreaterEqual(error, 0)
        self.assertLess(error, 0.001)

    def test_kv_cache_scales_linearly_with_context_and_batch(self):
        base = kv_cache_bytes(32, 2048, 4096, 2)
        self.assertEqual(kv_cache_bytes(32, 4096, 4096, 2), base * 2)
        self.assertEqual(kv_cache_bytes(32, 2048, 4096, 2, 4), base * 4)

    def test_dataset_cleaning_tracks_rejection_reasons(self):
        rows = [
            {"prompt": " Q ", "answer": " A ", "source": "urn:test:1"},
            {"prompt": "q", "answer": "a", "source": "urn:test:2"},
            {"prompt": "", "answer": "a", "source": "urn:test:3"},
            {"prompt": "x", "answer": "y", "source": "local-file"},
        ]
        accepted, rejected = clean_dataset(rows)
        self.assertEqual(len(accepted), 1)
        self.assertEqual(rejected, {"duplicate": 1, "missing_text": 1, "missing_provenance": 1})

    def test_embedding_cosine_tracks_direction_not_magnitude(self):
        self.assertAlmostEqual(cosine_similarity([1, 2], [2, 4]), 1.0)
        self.assertAlmostEqual(cosine_similarity([1, 0], [0, 1]), 0.0)
        with self.assertRaisesRegex(ValueError, "zero vector"):
            cosine_similarity([0, 0], [1, 0])

    def test_sinusoidal_positions_are_deterministic_and_position_dependent(self):
        origin = sinusoidal_position(0, 4)
        self.assertEqual(origin, [0.0, 1.0, 0.0, 1.0])
        self.assertEqual(sinusoidal_position(3, 4), sinusoidal_position(3, 4))
        self.assertNotEqual(origin, sinusoidal_position(1, 4))

    def test_attention_weights_normalize_and_mix_values(self):
        output, weights = scaled_dot_product_attention([[1, 0]], [[1, 0], [0, 1]],
                                                       [[10, 0], [0, 20]])
        self.assertAlmostEqual(sum(weights[0]), 1.0)
        self.assertGreater(weights[0][0], weights[0][1])
        self.assertGreater(output[0][0], 5); self.assertGreater(output[0][1], 0)

    def test_causal_mask_blocks_future_information(self):
        queries = [[1, 0], [1, 0]]; keys = [[1, 0], [1, 0]]
        first, weights = scaled_dot_product_attention(queries, keys, [[3], [999]], causal=True)
        changed, _ = scaled_dot_product_attention(queries, keys, [[3], [-999]], causal=True)
        self.assertEqual(weights[0], [1.0, 0.0])
        self.assertEqual(first[0], changed[0]); self.assertNotEqual(first[1], changed[1])


if __name__ == "__main__":
    unittest.main()
