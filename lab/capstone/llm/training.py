"""Dependency-free tokenizer, PEFT, early-stopping, and fairness exercises."""
from collections import Counter
from dataclasses import dataclass

class BytePairTokenizer:
    def __init__(self): self.merges: list[tuple[str, str]] = []
    def train(self, texts: list[str], merge_count: int) -> None:
        corpus = [list(word) + ["</w>"] for text in texts for word in text.lower().split()]
        self.merges = []
        for _ in range(merge_count):
            pairs = Counter((tokens[i], tokens[i+1]) for tokens in corpus for i in range(len(tokens)-1))
            if not pairs: break
            pair = min((key for key, count in pairs.items() if count == max(pairs.values())), default=None)
            if pair is None: break
            self.merges.append(pair); merged = "".join(pair)
            updated = []
            for tokens in corpus:
                output, i = [], 0
                while i < len(tokens):
                    if i + 1 < len(tokens) and (tokens[i], tokens[i+1]) == pair:
                        output.append(merged); i += 2
                    else: output.append(tokens[i]); i += 1
                updated.append(output)
            corpus = updated
    def encode_word(self, word: str) -> list[str]:
        tokens = list(word.lower()) + ["</w>"]
        for pair in self.merges:
            output, i = [], 0
            while i < len(tokens):
                if i + 1 < len(tokens) and (tokens[i], tokens[i+1]) == pair:
                    output.append("".join(pair)); i += 2
                else: output.append(tokens[i]); i += 1
            tokens = output
        return tokens

def matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    if not left or not right or len(left[0]) != len(right): raise ValueError("incompatible matrices")
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))] for i in range(len(left))]

def lora_update(a: list[list[float]], b: list[list[float]], alpha: float = 1.0) -> list[list[float]]:
    rank = len(a)
    if rank == 0 or len(b[0]) != rank: raise ValueError("invalid LoRA factors")
    product = matmul(b, a)
    return [[value * alpha / rank for value in row] for row in product]

def lora_parameter_count(input_size: int, output_size: int, rank: int) -> dict[str, int]:
    if not 0 < rank <= min(input_size, output_size): raise ValueError("rank must fit dimensions")
    return {"full": input_size * output_size, "lora": rank * (input_size + output_size)}

@dataclass
class EarlyStopping:
    patience: int
    minimum_improvement: float = 0.0
    best: float = float("inf")
    bad_epochs: int = 0
    def update(self, validation_loss: float) -> bool:
        if validation_loss < self.best - self.minimum_improvement:
            self.best, self.bad_epochs = validation_loss, 0
        else: self.bad_epochs += 1
        return self.bad_epochs >= self.patience

def fairness_report(rows: list[dict[str, object]]) -> dict[str, object]:
    """Selection rate and true-positive rate by group; context determines appropriateness."""
    groups = sorted({str(row["group"]) for row in rows}); report = {}
    for group in groups:
        subset = [row for row in rows if str(row["group"]) == group]
        positives = [row for row in subset if int(row["label"]) == 1]
        report[group] = {
            "count": len(subset),
            "selection_rate": sum(int(row["prediction"]) == 1 for row in subset) / len(subset),
            "true_positive_rate": (sum(int(row["prediction"]) == 1 for row in positives) / len(positives)) if positives else None,
        }
    rates = [value["selection_rate"] for value in report.values()]
    return {"groups": report, "selection_rate_gap": max(rates) - min(rates),
            "limitations": "Group metrics require justified labels, representative samples, uncertainty, intersectional review, and impact analysis."}

