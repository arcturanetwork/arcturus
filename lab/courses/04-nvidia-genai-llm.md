# Track 4 — NVIDIA Certified Professional: Generative AI LLMs

**Target:** NCP-GENL; official page checked 2026-09-03; exam marked coming soon. NVIDIA describes 60–70 questions in 120 minutes and recommends 2–3 years of LLM experience.

Track evidence: [numbered objective map](../studies/ncp-genl/objective-map.md), [standard-library numerical lab](../capstone/llm/lab.py), and [timed scenario bank](../studies/ncp-genl/scenario-labs.json). These exercises prove concept implementation and reasoning only; they do not substitute for model training, GPU profiling, distributed execution, or NVIDIA serving evidence.

## Blueprint map

| Domain | Weight | Course outcome |
|---|---:|---|
| Model optimization | 17% | Optimize latency, throughput, memory and serving tradeoffs |
| GPU acceleration and optimization | 14% | Explain parallelism, precision, memory, batching and profiling |
| Prompt engineering | 13% | Design controlled prompts and measure changes rather than vibe-checking |
| Fine-tuning | 13% | Select PEFT/full tuning, build datasets, train and evaluate safely |
| Data preparation | 9% | Curate, clean, tokenize, split, govern and document data |
| Model deployment | 9% | Containerized scalable inference and orchestration |
| Evaluation | 7% | Task, safety, retrieval and human evaluation systems |
| Production monitoring/reliability | 7% | SLOs, drift, quality regressions, rollback and lifecycle controls |
| LLM architecture | 6% | Transformers, attention, tokenization, decoding and context limits |
| Safety, ethics and compliance | 5% | Bias, privacy, misuse, provenance, guardrails and governance |

Note: the live NVIDIA page currently appears to place deployment text under “Model Optimization” and unrelated OpenUSD text under “Fine-Tuning.” Treat the domain names/weights and downloadable study guide as authoritative, and re-check when the exam launches.

## Eight-week sprint

1. Transformer and inference mechanics; calculate rough KV-cache and throughput tradeoffs.
2. Prompt/context engineering; establish task datasets and baselines first.
3. Data curation, deduplication, contamination, splits, lineage and model/data cards.
4. RAG: chunking, embeddings, reranking, citation faithfulness and access control.
5. Fine-tuning: SFT, LoRA/PEFT, preference methods, catastrophic forgetting and checkpoints.
6. GPU/distributed systems: tensor/pipeline/data parallelism, precision, quantization and profiling.
7. Serving: batching, caching, Triton/NIM concepts, autoscaling and Kubernetes.
8. Evaluation, safety, monitoring, rollback and incident response.

## Exit gate

Compare baseline, RAG and adapted-model approaches on a held-out suite. Report quality, groundedness, safety, p50/p95 latency, throughput and estimated cost. Make a defensible ship/no-ship decision.

Primary links: [certification and blueprint](https://www.nvidia.com/en-us/learn/certification/generative-ai-llm-professional/), [NVIDIA DLI](https://www.nvidia.com/en-us/training/), [NeMo documentation](https://docs.nvidia.com/nemo-framework/), [NVIDIA Developer videos](https://www.youtube.com/@NVIDIADeveloper).
