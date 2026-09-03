# NCP-AAI objective mastery map

Source: NVIDIA's 13-page Agentic AI Exam Study Guide, retrieved 2026-09-03. Status is evidence-based: `studied`, `implemented`, `tested`, or `needs-platform-lab`.

| Guide section and numbered objectives | Current evidence | Status |
|---|---|---|
| 1.1–1.8 UI, ReAct, agent protocols, memory, multi-agent orchestration, logic/prompt/state chains, knowledge graphs, scale | Typed correlated agent messages, role/message allowlists, decreasing hop budgets, approval/trace model, bounded state | tested locally; UI/model ReAct remain |
| 2.1–2.6 prompts, multimodal models, tools/APIs, failure recovery, streaming/feedback, decision refinement | Allowlisted typed tools; bounded transient retries; circuit breaker; failure events | tested (2.3–2.4); remaining studied |
| 3.1–3.5 benchmarks, comparisons, feedback, parameter tradeoffs, result-driven tuning | 50-case suite, workflow/planner comparison, structured categorized human feedback, retrieval Recall/MRR | tested locally; model tuning remains |
| 4.1–4.5 production orchestration, MLOps, load profiling, containers/Kubernetes, cost/HA | Threaded HTTP gateway plus reproducible loopback load/failure profiler measure throughput, p50/p95/p99/max, correlation and policy rejection; container/Kubernetes/external-dependency evidence pending | partial tested |
| 5.1–5.5 memory, decomposition, planning, stateful orchestration, feedback adaptation | Step budget, explicit state, workflow/planner comparison, window-vs-retrieval memory experiment | tested (5.1–5.4); feedback adaptation studied |
| 6.1–6.5 RAG/hybrid retrieval, vector DBs, ETL, quality, real-time structured/unstructured knowledge | Lexical+semantic score fusion, authorization-before-ranking, provenance, Recall/MRR, duplicate/metadata validation, graph traversal | tested locally; real vector DB/ETL streaming remain |
| 7.1–7.5 NeMo Guardrails, NIM, Agent Toolkit, TensorRT-LLM/Triton, multimodal NVIDIA pipelines | Requires NVIDIA environment | needs-platform-lab |
| 8.1–8.5 dashboards/SLOs, logs/anomalies, version benchmarks, automated lifecycle, uptime/trust | HTTP health boundary plus structured trace/retry/circuit events and versioned evaluation report | partial tested; telemetry/load/automated lifecycle remain |
| 9.1–9.5 audit/security, privacy/policy, bias/toxicity, layered safety, licensing/regulation | Approval, audit and injection tests | tested (partial) |
| 10.1–10.4 UI, feedback, decision traceability, intervention | Approval and trace primitives | implemented |

## Next evidence increments

1. Replace repeated template cases with a richer model-backed representative/adversarial dataset while retaining deterministic policy tests.
2. Replace supplied semantic scores with real embeddings/vector DB and add streaming updates.
3. Add summary memory and explicit retention/deletion policy tests.
4. Run NeMo Guardrails/NIM/Triton labs in an appropriate NVIDIA environment.
5. Deploy through the CKA track and load-test through the AWS architecture track.

Use the [20-domain scenario lab bank](scenario-labs.json) and [scoring rubric](scenario-rubric.md) for timed design practice. Passing these scenarios demonstrates blueprint reasoning, not NVIDIA runtime competence.

## Verified local evidence

- `python3 -m unittest discover -s tests -v`: run the current repository-wide test count; do not preserve a stale numeric claim here.
- `python3 -m capstone.agent.evaluate`: 50/50 policy cases pass; workflow and flexible-planner results are stored in `evaluation-results.json`.
- The retrieval tests exposed and then verified remediation of a false positive caused by stopword overlap; query/document normalization now removes a small explicit stopword set.
- Limitation: these results prove deterministic control behavior, not semantic model quality or NVIDIA platform mastery.

## Source discrepancy to resolve before booking

The PDF lists Deployment and Scaling at 5% and Run/Monitor/Maintain at 7%. The live certification table showed 13% and 5% on 2026-09-03, causing its visible weights to total 98%. Study every objective and confirm the governing weights with NVIDIA when registration opens.
