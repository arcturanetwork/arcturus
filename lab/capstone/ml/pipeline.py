"""Provider-neutral MLOps pipeline lab mapped to Google PMLE decisions."""
from dataclasses import dataclass, field
import hashlib, json, statistics

class PipelineError(RuntimeError): pass

@dataclass(frozen=True)
class Example:
    value: float
    label: int

@dataclass(frozen=True)
class Model:
    version: str
    threshold: float
    preprocessing_fingerprint: str
    metrics: dict[str, float]
    dataset_fingerprint: str
    def predict(self, value: float) -> int: return int(value >= self.threshold)

@dataclass
class Registry:
    models: dict[str, Model] = field(default_factory=dict)
    deployed: str | None = None
    prior_deployed: str | None = None
    def register(self, model: Model) -> None:
        if model.version in self.models: raise PipelineError("immutable version already exists")
        self.models[model.version] = model
    def deploy(self, version: str, minimum_accuracy: float) -> None:
        if self.models[version].metrics["accuracy"] < minimum_accuracy:
            raise PipelineError("model failed deployment quality gate")
        self.prior_deployed, self.deployed = self.deployed, version
    def rollback(self) -> None:
        if self.prior_deployed is None: raise PipelineError("no prior deployment")
        self.deployed, self.prior_deployed = self.prior_deployed, self.deployed

def fingerprint(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:16]

def validate(examples: list[Example]) -> None:
    if len(examples) < 4: raise PipelineError("insufficient examples")
    labels = {item.label for item in examples}
    if not labels <= {0, 1} or labels != {0, 1}: raise PipelineError("binary labels must include both classes")
    if any(not -1_000_000 < item.value < 1_000_000 for item in examples):
        raise PipelineError("feature outside accepted range")

def preprocess(value: float) -> float: return round(value, 6)
PREPROCESSING_FINGERPRINT = fingerprint("round(value, 6):v1")

def accuracy(model: Model, examples: list[Example]) -> float:
    return sum(model.predict(preprocess(item.value)) == item.label for item in examples) / len(examples)

def train(version: str, training: list[Example], validation: list[Example]) -> Model:
    validate(training); validate(validation)
    negatives = [preprocess(x.value) for x in training if x.label == 0]
    positives = [preprocess(x.value) for x in training if x.label == 1]
    threshold = (max(negatives) + min(positives)) / 2
    lineage = fingerprint([(x.value, x.label) for x in training])
    draft = Model(version, threshold, PREPROCESSING_FINGERPRINT, {"accuracy": 0}, lineage)
    return Model(version, threshold, PREPROCESSING_FINGERPRINT,
                 {"accuracy": accuracy(draft, validation)}, lineage)

def mean_shift(training_values: list[float], serving_values: list[float]) -> float:
    if not training_values or not serving_values: raise PipelineError("monitoring windows cannot be empty")
    spread = statistics.pstdev(training_values)
    difference = abs(statistics.mean(serving_values) - statistics.mean(training_values))
    return difference / spread if spread else (float("inf") if difference else 0.0)

def retraining_decision(shift: float, quality: float | None,
                        shift_threshold: float = 2.0, quality_floor: float = 0.85) -> dict[str, object]:
    reasons = []
    if shift >= shift_threshold: reasons.append("data_drift")
    if quality is not None and quality < quality_floor: reasons.append("quality_regression")
    return {"trigger_training": bool(reasons), "reasons": reasons,
            "requires_validation_and_approval": bool(reasons)}

def diagnose_change(*, training_serving_feature_gap: bool, input_distribution_changed: bool,
                    relationship_quality_changed: bool, attribution_changed: bool) -> list[str]:
    """Classify independent monitoring signals; categories may coexist."""
    findings = []
    if training_serving_feature_gap: findings.append("training_serving_skew")
    if input_distribution_changed: findings.append("data_drift")
    if relationship_quality_changed: findings.append("concept_drift")
    if attribution_changed: findings.append("attribution_drift")
    return findings

def serving_recommendation(*, interactive: bool, volume: int, latency_slo_ms: int | None,
                           payload_contains_sensitive_data: bool) -> dict[str, object]:
    """Make the batch/online and exposure decision explicit and testable."""
    if volume <= 0: raise PipelineError("volume must be positive")
    if interactive and latency_slo_ms is None:
        raise PipelineError("interactive serving needs a latency SLO")
    mode = "online" if interactive else "batch"
    return {"mode": mode,
            "autoscaling_required": interactive and volume > 100,
            "private_endpoint": payload_contains_sensitive_data,
            "latency_slo_ms": latency_slo_ms if interactive else None,
            "note": "IAM and data controls remain required even with private exposure"}

def release_decision(candidate: Model, baseline: Model, *, slice_floor: float,
                     slice_scores: dict[str, float], max_accuracy_regression: float = 0.0) -> dict[str, object]:
    """Gate promotion on aggregate and worst-slice quality, never metrics alone."""
    if not slice_scores: raise PipelineError("slice scores required")
    aggregate_ok = candidate.metrics["accuracy"] >= baseline.metrics["accuracy"] - max_accuracy_regression
    failed_slices = sorted(name for name, score in slice_scores.items() if score < slice_floor)
    approved = aggregate_ok and not failed_slices
    return {"approved": approved, "aggregate_ok": aggregate_ok,
            "failed_slices": failed_slices, "requires_human_approval": approved}
