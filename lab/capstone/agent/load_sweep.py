"""Repeated concurrency sweep for the local TrustGraph HTTP lab."""
from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import statistics

from capstone.agent.load_profile import run_profile


def aggregate(workers: int, trials: list[dict[str, object]]) -> dict[str, object]:
    if workers < 1 or not trials:
        raise ValueError("positive workers and trials required")
    for trial in trials:
        if trial["configuration"]["workers"] != workers:
            raise ValueError("trial worker count does not match group")
    metric = lambda key: [float(trial["latency_ms"][key]) for trial in trials]
    return {"workers": workers, "trials": len(trials),
            "median_throughput_rps": statistics.median(float(x["throughput_rps"]) for x in trials),
            "median_latency_ms": {key: statistics.median(metric(key)) for key in ("p50", "p95", "p99")},
            "worst_p99_ms": max(metric("p99")),
            "unexpected_outcomes": sum(int(x["unexpected_outcomes"]) for x in trials),
            "all_correlation_intact": all(bool(x["correlation_integrity"]) for x in trials)}


def saturation_findings(groups: list[dict[str, object]]) -> dict[str, object]:
    if len(groups) < 2:
        raise ValueError("at least two concurrency groups required")
    ordered = sorted(groups, key=lambda x: int(x["workers"]))
    peak = max(ordered, key=lambda x: float(x["median_throughput_rps"]))
    regressions = []
    for prior, current in zip(ordered, ordered[1:]):
        throughput_gain = (float(current["median_throughput_rps"]) /
                           float(prior["median_throughput_rps"]) - 1)
        p95_growth = (float(current["median_latency_ms"]["p95"]) /
                      max(float(prior["median_latency_ms"]["p95"]), .000001) - 1)
        if throughput_gain < .10 and p95_growth > .50:
            regressions.append({"from_workers":prior["workers"], "to_workers":current["workers"],
                                "throughput_gain":throughput_gain, "p95_growth":p95_growth})
    return {"peak_median_throughput_workers":peak["workers"],
            "peak_median_throughput_rps":peak["median_throughput_rps"],
            "saturation_candidates":regressions,
            "rule":"candidate when throughput gains <10% while p95 grows >50%"}


def run_sweep(worker_counts: tuple[int, ...] = (1, 5, 10, 20, 40),
              trials_per_group: int = 3, requests_per_trial: int = 100) -> dict[str, object]:
    if len(set(worker_counts)) != len(worker_counts) or trials_per_group < 2:
        raise ValueError("unique worker counts and at least two trials required")
    groups = []
    for workers in worker_counts:
        trials = [run_profile(requests_per_trial, workers) for _ in range(trials_per_group)]
        groups.append(aggregate(workers, trials))
    return {"recorded_at":datetime.now(timezone.utc).isoformat(),
            "requests_per_trial":requests_per_trial, "groups":groups,
            "findings":saturation_findings(groups),
            "limitations":["short loopback trials with no model or external dependency",
                           "medians reduce run noise but do not replace sustained soak/resource telemetry"]}


if __name__ == "__main__":
    report = run_sweep()
    output = Path("evidence/ncp-aai/http-concurrency-sweep.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {output}; groups={len(report['groups'])}")
