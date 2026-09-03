import unittest

from capstone.agent.memory import compare_memory


class MemoryTests(unittest.TestCase):
    def test_retrieval_recovers_old_fact_window_drops(self):
        result = compare_memory()
        self.assertFalse(result["window_found_fact"])
        self.assertTrue(result["retrieval_found_fact"])
        self.assertEqual(result["window_turns"], [3, 4])
        self.assertEqual(result["retrieval_turns"], [1])


if __name__ == "__main__":
    unittest.main()

