import unittest

from capstone.agent.knowledge import Document, KnowledgeStore, QualityError, retrieval_metrics


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.store = KnowledgeStore()
        self.store.ingest(Document("public", "public#1", "human approval for writes",
                                   frozenset({"alice", "bob"}), "https://example.test/public"))
        self.store.ingest(Document("private", "private#1", "secret merger approval",
                                   frozenset({"alice"}), "urn:internal:private"))

    def test_search_returns_rank_and_provenance(self):
        result = self.store.search("approval writes", "bob")
        self.assertEqual(result[0]["passage_id"], "public#1")
        self.assertIn("source_uri", result[0])
        self.assertGreater(result[0]["score"], 0)

    def test_acl_filters_before_results(self):
        result = self.store.search("secret merger", "bob")
        self.assertEqual(result, [])

    def test_authorized_principal_can_retrieve_private_passage(self):
        result = self.store.search("secret merger", "alice")
        self.assertEqual(result[0]["document_id"], "private")

    def test_duplicate_content_is_rejected(self):
        with self.assertRaisesRegex(QualityError, "duplicate"):
            self.store.ingest(Document("copy", "copy#1", "human approval for writes",
                                       frozenset({"alice"}), "urn:copy"))

    def test_missing_provenance_and_acl_are_rejected(self):
        with self.assertRaises(QualityError):
            self.store.ingest(Document("bad", "bad#1", "content", frozenset(), "file.txt"))

    def test_graph_path_obeys_hop_limit(self):
        self.store.add_edge("agent", "uses", "tool")
        self.store.add_edge("tool", "requires", "approval")
        self.assertEqual(self.store.path("agent", "approval", 2), ["agent", "tool", "approval"])
        self.assertEqual(self.store.path("agent", "approval", 1), [])

    def test_hybrid_search_combines_signals_without_acl_leak(self):
        result = self.store.hybrid_search("approval writes", "bob", {"private#1": 1.0, "public#1": .4})
        self.assertEqual([item["passage_id"] for item in result], ["public#1"])
        self.assertIn("lexical_score", result[0]); self.assertIn("semantic_score", result[0])

    def test_retrieval_metrics_measure_ranking_and_coverage(self):
        metrics = retrieval_metrics({"q1":{"a"},"q2":{"b","c"}}, {"q1":["x","a"],"q2":["b","x"]}, 2)
        self.assertEqual(metrics["recall@2"], .75); self.assertEqual(metrics["mrr@2"], .75)


if __name__ == "__main__":
    unittest.main()
