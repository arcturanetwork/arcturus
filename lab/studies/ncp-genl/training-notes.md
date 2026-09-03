# Tokenization, PEFT, alignment, and evaluation notes

## Transformer and embedding mechanics

Scaled dot-product attention computes query/key similarity divided by the square root of key width, applies masking before softmax, and forms a weighted sum of values. The scale limits softmax saturation as dimensionality grows. A decoder causal mask removes future positions; it is an information-flow constraint, not a request to the model. Multi-head attention learns different projections and concatenates head outputs, while positional information prevents a token sequence from becoming order-blind. Cosine similarity compares vector direction and ignores magnitude; retrieval quality still depends on the embedding model, corpus, negatives, filters, and evaluation set.

The local standard-library implementation is deliberately transparent and numerically tested. It does not claim fused-kernel performance, learned embeddings, a trained transformer, or GPU mastery.

## Tokenization

BPE repeatedly merges frequent adjacent symbols; WordPiece commonly selects merges according to a likelihood-style score rather than raw pair frequency. Vocabulary size trades sequence length against embedding/output-matrix size and rare-token generalization. Train only on the training partition, preserve normalization/version metadata, inspect multilingual and domain fragmentation, and never assume fewer tokens means better semantics.

## Fine-tuning selection

- Prompt/context/RAG first when knowledge changes frequently or provenance matters.
- SFT teaches examples of desired behavior; it requires representative, licensed, quality-controlled data.
- LoRA freezes base weights and learns low-rank updates, reducing trainable parameters and enabling adapter management; low parameter count does not eliminate activation/optimizer/runtime constraints.
- Contrastive learning brings related embeddings closer and separates negatives; negative sampling quality is decisive.
- DPO optimizes preferences against a reference without an online reward-model RL loop. RLHF typically involves preference/reward modeling and policy optimization. GRPO uses group-relative rewards and has distinct stability/data tradeoffs.

Use held-out task and safety slices, early stopping, checkpoint/version lineage, contamination checks, baseline comparison, and ablations. A training-loss improvement is not a production-quality claim.

## Fairness

Measure performance and outcome metrics by relevant groups and intersections, with sample counts and uncertainty. Demographic parity and equal opportunity answer different normative questions and may be mutually inappropriate for a particular context. Investigate data, labels, thresholds, product workflow and downstream harm; do not “fix” a dashboard metric without governance and impact review.
