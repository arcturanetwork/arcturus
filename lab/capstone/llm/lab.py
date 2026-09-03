"""Numerical LLM concepts lab using only the Python standard library."""

from collections import Counter
import math
import random
import re


def dot(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or not left:
        raise ValueError("vectors must have equal positive dimensions")
    return sum(a * b for a, b in zip(left, right))


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = dot(left, right)
    left_norm = math.sqrt(dot(left, left)); right_norm = math.sqrt(dot(right, right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("cosine similarity is undefined for a zero vector")
    return numerator / (left_norm * right_norm)


def sinusoidal_position(position: int, dimensions: int) -> list[float]:
    if position < 0 or dimensions < 1:
        raise ValueError("position must be nonnegative and dimensions positive")
    result = []
    for index in range(dimensions):
        frequency = 1 / (10_000 ** (2 * (index // 2) / dimensions))
        angle = position * frequency
        result.append(math.sin(angle) if index % 2 == 0 else math.cos(angle))
    return result


def scaled_dot_product_attention(queries: list[list[float]], keys: list[list[float]],
                                 values: list[list[float]], causal: bool = False
                                 ) -> tuple[list[list[float]], list[list[float]]]:
    """Reference attention for reasoning tests, not a performance implementation."""
    if not queries or not keys or len(keys) != len(values):
        raise ValueError("queries, keys, and matching values are required")
    key_width = len(keys[0]); value_width = len(values[0])
    if key_width < 1 or value_width < 1 or any(len(row) != key_width for row in queries + keys):
        raise ValueError("query and key dimensions must match")
    if any(len(row) != value_width for row in values):
        raise ValueError("value dimensions must be consistent")
    outputs, all_weights = [], []
    scale = math.sqrt(key_width)
    for query_index, query in enumerate(queries):
        logits = [dot(query, key) / scale for key in keys]
        allowed = [index for index in range(len(keys)) if not causal or index <= query_index]
        if not allowed:
            raise ValueError("causal attention has no visible key")
        visible = softmax([logits[index] for index in allowed])
        weights = [0.0] * len(keys)
        for index, weight in zip(allowed, visible): weights[index] = weight
        outputs.append([sum(weights[row] * values[row][column] for row in range(len(values)))
                        for column in range(value_width)])
        all_weights.append(weights)
    return outputs, all_weights


def softmax(logits: list[float], temperature: float = 1.0) -> list[float]:
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    scaled = [value / temperature for value in logits]
    peak = max(scaled)
    exps = [math.exp(value - peak) for value in scaled]
    total = sum(exps)
    return [value / total for value in exps]


def filtered_distribution(logits: list[float], top_k: int | None = None,
                          top_p: float | None = None,
                          temperature: float = 1.0) -> list[float]:
    probabilities = softmax(logits, temperature)
    order = sorted(range(len(probabilities)), key=probabilities.__getitem__, reverse=True)
    keep = set(order)
    if top_k is not None:
        if top_k < 1:
            raise ValueError("top_k must be positive")
        keep &= set(order[:top_k])
    if top_p is not None:
        if not 0 < top_p <= 1:
            raise ValueError("top_p must be in (0, 1]")
        cumulative, nucleus = 0.0, set()
        for index in order:
            nucleus.add(index)
            cumulative += probabilities[index]
            if cumulative >= top_p:
                break
        keep &= nucleus
    masked = [probability if index in keep else 0.0
              for index, probability in enumerate(probabilities)]
    total = sum(masked)
    return [value / total for value in masked]


def sample_token(logits: list[float], seed: int, **options: object) -> int:
    probabilities = filtered_distribution(logits, **options)
    return random.Random(seed).choices(range(len(logits)), weights=probabilities, k=1)[0]


def perplexity(token_probabilities: list[float]) -> float:
    if not token_probabilities or any(p <= 0 or p > 1 for p in token_probabilities):
        raise ValueError("probabilities must be non-empty and in (0, 1]")
    return math.exp(-sum(math.log(p) for p in token_probabilities) / len(token_probabilities))


def rouge_l(reference: str, candidate: str) -> dict[str, float]:
    left, right = reference.split(), candidate.split()
    table = [[0] * (len(right) + 1) for _ in range(len(left) + 1)]
    for i, a in enumerate(left, 1):
        for j, b in enumerate(right, 1):
            table[i][j] = table[i - 1][j - 1] + 1 if a == b else max(table[i - 1][j], table[i][j - 1])
    overlap = table[-1][-1]
    precision = overlap / len(right) if right else 0.0
    recall = overlap / len(left) if left else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def symmetric_int8(values: list[float]) -> tuple[list[int], float]:
    peak = max((abs(value) for value in values), default=0.0)
    if peak == 0:
        return [0 for _ in values], 1.0
    scale = peak / 127
    return [max(-127, min(127, round(value / scale))) for value in values], scale


def dequantize(values: list[int], scale: float) -> list[float]:
    return [value * scale for value in values]


def quantization_error(original: list[float], restored: list[float]) -> float:
    if len(original) != len(restored):
        raise ValueError("vectors must have equal length")
    return sum((a - b) ** 2 for a, b in zip(original, restored)) / max(1, len(original))


def kv_cache_bytes(layers: int, tokens: int, hidden_size: int,
                   bytes_per_element: int, batch_size: int = 1) -> int:
    """Approximation: key + value for each layer/token/hidden element."""
    if min(layers, tokens, hidden_size, bytes_per_element, batch_size) < 1:
        raise ValueError("dimensions must be positive")
    return 2 * layers * tokens * hidden_size * bytes_per_element * batch_size


def clean_dataset(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, int]]:
    accepted, seen = [], set()
    rejected = Counter()
    for row in rows:
        prompt = re.sub(r"\s+", " ", row.get("prompt", "")).strip()
        answer = re.sub(r"\s+", " ", row.get("answer", "")).strip()
        source = row.get("source", "").strip()
        if not prompt or not answer:
            rejected["missing_text"] += 1
            continue
        if not source.startswith(("https://", "urn:")):
            rejected["missing_provenance"] += 1
            continue
        key = (prompt.lower(), answer.lower())
        if key in seen:
            rejected["duplicate"] += 1
            continue
        seen.add(key)
        accepted.append({"prompt": prompt, "answer": answer, "source": source})
    return accepted, dict(rejected)
