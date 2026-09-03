# HTTP tail-latency investigation

## Baseline — 2026-09-03

The dependency-free loopback gateway received 200 requests with 20 workers; every tenth request was an intentionally unauthorized write. It processed 180 reads and rejected all 20 writes with zero unexpected outcomes and intact correlation IDs. Throughput was 97.76 requests/s. Latency was p50 8.95 ms, p95 1,011.36 ms, p99 1,470.34 ms, and max 1,511.20 ms.

The median and correctness result were acceptable for a local functional test, but the tail was not. The first controlled hypothesis was connection admission: Python's base TCP server commonly uses a listen backlog of five, smaller than the 20-worker burst. The candidate raises the lab server backlog to 128 and enables daemon request threads. The workload, worker count, request mix, and profiler remain unchanged.

This experiment can show whether queue admission dominated the observed tail. It does not establish a production SLO: loopback removes real network and dependency latency, the handler performs no model inference, the run is short, and the gateway still uses in-memory state. Subsequent work must test realistic service time, saturation, cancellation, external dependencies, persistence, containers, and multiple replicas.

## Candidate result

The identical rerun with backlog 128 completed 200 requests in 1.142 seconds at 175.17 requests/s. It again produced 180 successful reads, 20 expected policy rejections, zero unexpected outcomes, and intact correlation. Latency was p50 24.62 ms, p95 433.26 ms, p99 476.42 ms, and max 490.24 ms.

Compared with the baseline, throughput increased about 79%, p95 decreased about 57%, and p99 decreased about 68%. Median latency increased from 8.95 to 24.62 ms, so the change did not dominate on every metric. The result supports—without proving—the connection-admission hypothesis. OS scheduling and a single short sample can materially affect these numbers. Next validation should use repeated warm runs, several concurrency levels, a realistic service-time distribution, and resource saturation telemetry before setting any SLO or capacity limit.

## Replicated concurrency sweep

`python3 -m capstone.agent.load_sweep` runs three 100-request trials at 1, 5, 10, 20, and 40 workers. It reports median throughput and p50/p95/p99 per group, the worst p99, correctness/correlation failures, and candidate saturation transitions. The saturation heuristic flags a transition only when median throughput gains less than 10% while median p95 grows more than 50%. This is a diagnostic rule, not a universal capacity definition.

The measured median throughput by worker count was 174.50, 170.27, 168.42, 163.93, and 162.84 requests/s for 1, 5, 10, 20, and 40 workers respectively. Median p95 was 0.83, 5.30, 10.09, 22.04, and 42.14 ms. All 1,500 requests across 15 trials had expected outcomes and intact correlation. Every concurrency transition met the diagnostic saturation rule because throughput did not rise while tail latency grew sharply.

This does not mean a real agent service should use one worker. The synthetic handler has almost no model, retrieval, network, or storage wait, so concurrency provides no latency-hiding benefit and mostly adds scheduling/queueing overhead. The key production lesson is to profile with a representative service-time and dependency distribution; worker count from a no-op loopback benchmark is not portable capacity guidance.
