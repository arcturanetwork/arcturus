# NCP-GENL objective mastery map

Source: NVIDIA's 13-page Gen AI LLMs Exam Study Guide, retrieved 2026-09-03. The downloadable guide corrects the obvious OpenUSD copy error on the live webpage. Status distinguishes `studied`, `tested-concept`, and `gpu/model-lab-required`.

| Guide objectives | Skills | Evidence | Status |
|---|---|---|---|
| 1.1–1.6 | Encoder/decoder structures, attention, embeddings, advanced/output sampling | Reference scaled dot-product attention with causal masking, sinusoidal positions, cosine similarity, temperature, top-k and nucleus tests | tested-concept; trained architecture/embedding model lab required |
| 2.1–2.4 | Prompt templates, zero/one/few-shot, causal LM, validation/constrained decoding | Deterministic output controls only | studied; model lab required |
| 3.1–3.3 | Cleaning/curation, formats/distributions, BPE/WordPiece and vocabulary | Provenance/duplicate tests plus deterministic BPE merge training | tested-concept; production tokenizer comparison required |
| 4.1–4.7 | Pruning/sparsity/quantization, distillation, tuning, ablations, TensorRT/KV cache, MLM | Symmetric INT8 error measurement and KV-cache scaling model | tested-concept; model/GPU experiments required |
| 5.1–5.4 | SFT/RLHF/DPO/GRPO, contrastive/PEFT, early stopping, hallucination assessment | LoRA update/parameter math, early-stopping tests and method selection notes | tested-concept; model training required |
| 6.1–6.4 | Human/LLM judge, BLEU/ROUGE/perplexity, error analysis, platform comparison, eval framework | Perplexity and ROUGE-L implementations; existing policy/retrieval suite | tested-concept; human/model judge and platform benchmark required |
| 7.1–7.4 | DDP/FSDP and model/pipeline/tensor/data/sequence/expert parallelism, mixed precision, GEMM/accumulation, CUDA profiling | Memory/parallelism notes only | gpu/model-lab-required |
| 8.1–8.3 | Model-type tradeoffs, container/dynamic batching/Dynamo-Triton, Kubernetes/monitoring | CKA manifests; no serving runtime | gpu/model-lab-required |
| 9.1–9.5 | Dashboards, logs/anomalies/RCA, version benchmarks, automated lifecycle, uptime/trust | Agent trace and versioned eval artifacts | partial tested-concept |
| 10.1–10.5 | Responsible deployment, bias/fairness audit, monitoring, mitigation, guardrails | Agent controls plus group selection/TPR fairness report with limitations | partial tested-concept; model guardrails required |

## Core distinctions studied

- Temperature reshapes probabilities; top-k and top-p truncate candidate support. They solve different control problems.
- Perplexity evaluates probability assigned to a sequence and is not a direct truth/helpfulness score.
- ROUGE/BLEU overlap can miss semantic equivalence and reward reference mimicry; use task and human evidence too.
- PTQ is cheaper and data-light; QAT can recover accuracy but adds training cost. Always measure quality and hardware-realized speed.
- Quantization, pruning and distillation are separate mechanisms; a smaller artifact is not automatically faster on the target runtime.
- Data, tensor, pipeline, sequence and expert parallelism partition different dimensions and incur different communication/bubble costs.
- Gradient accumulation raises effective batch size without storing all microbatches concurrently, but it changes optimizer-step frequency and does not remove all memory costs.
- KV-cache memory grows with layers, context length, hidden representation, precision and batch/concurrency.

## Timed scenario practice

Use the [20 original blueprint scenarios](scenario-labs.json) with the [evidence-first rubric](scenario-rubric.md). They cover every published domain twice and exercise selection, diagnosis, and experimental design. They do not replace model, GPU, distributed-training, or serving-runtime evidence.

## Source-quality note

The PDF metadata/title says “AI Infrastructure” while its actual cover/content says Gen AI LLMs. The live page's Fine-Tuning row contains unrelated OpenUSD text and its Model Optimization row contains deployment language. Use the numbered PDF objectives while still rechecking the launch edition.
