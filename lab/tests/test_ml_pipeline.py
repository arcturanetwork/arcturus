import unittest
from capstone.ml.pipeline import (Example, PipelineError, PREPROCESSING_FINGERPRINT, Registry,
                                 diagnose_change, mean_shift, release_decision,
                                 retraining_decision, serving_recommendation, train)

TRAIN = [Example(-2,0), Example(-1,0), Example(1,1), Example(2,1)]
VALID = [Example(-3,0), Example(-.5,0), Example(.5,1), Example(3,1)]

class MlPipelineTests(unittest.TestCase):
    def test_versioned_lineage_and_metric(self):
        model = train("v1", TRAIN, VALID)
        self.assertEqual(model.metrics["accuracy"], 1.0); self.assertTrue(model.dataset_fingerprint)
        self.assertEqual(model.preprocessing_fingerprint, PREPROCESSING_FINGERPRINT)
    def test_validation_rejects_single_class(self):
        with self.assertRaisesRegex(PipelineError, "both classes"): train("v1", [Example(i,0) for i in range(4)], VALID)
    def test_versions_are_immutable(self):
        registry, model = Registry(), train("v1", TRAIN, VALID); registry.register(model)
        with self.assertRaisesRegex(PipelineError, "immutable"): registry.register(model)
    def test_quality_gate_blocks_bad_model(self):
        registry = Registry(); registry.register(train("bad", TRAIN, [Example(-3,1),Example(-1,1),Example(1,0),Example(3,0)]))
        with self.assertRaisesRegex(PipelineError, "quality gate"): registry.deploy("bad", .8)
    def test_canary_failure_can_roll_back(self):
        registry = Registry()
        for version in ("v1","v2"): registry.register(train(version, TRAIN, VALID))
        registry.deploy("v1",.9); registry.deploy("v2",.9); registry.rollback()
        self.assertEqual(registry.deployed,"v1")
    def test_drift_is_normalized(self):
        self.assertEqual(mean_shift([-1,1],[-1,1]),0); self.assertGreater(mean_shift([-1,0,1],[10,11]),2)
    def test_retraining_does_not_directly_promote(self):
        decision = retraining_decision(3,.9)
        self.assertTrue(decision["trigger_training"]); self.assertTrue(decision["requires_validation_and_approval"])

    def test_monitoring_categories_are_not_conflated(self):
        findings = diagnose_change(training_serving_feature_gap=True,
                                   input_distribution_changed=False,
                                   relationship_quality_changed=True,
                                   attribution_changed=False)
        self.assertEqual(findings, ["training_serving_skew", "concept_drift"])

    def test_serving_choice_preserves_security_and_slo_requirements(self):
        online = serving_recommendation(interactive=True, volume=500, latency_slo_ms=200,
                                        payload_contains_sensitive_data=True)
        self.assertEqual(online["mode"], "online")
        self.assertTrue(online["autoscaling_required"]); self.assertTrue(online["private_endpoint"])
        with self.assertRaisesRegex(PipelineError, "latency SLO"):
            serving_recommendation(interactive=True, volume=5, latency_slo_ms=None,
                                   payload_contains_sensitive_data=False)

    def test_release_gate_blocks_harmed_slice(self):
        baseline, candidate = train("base", TRAIN, VALID), train("candidate", TRAIN, VALID)
        result = release_decision(candidate, baseline, slice_floor=.85,
                                  slice_scores={"en": .98, "es": .60})
        self.assertFalse(result["approved"]); self.assertEqual(result["failed_slices"], ["es"])

if __name__ == "__main__": unittest.main()
