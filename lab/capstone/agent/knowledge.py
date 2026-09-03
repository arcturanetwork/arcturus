"""Small, auditable retrieval/ETL/graph lab; no external service required."""

from dataclasses import dataclass
from collections import defaultdict, deque
import hashlib
import re


STOPWORDS = {"a", "an", "and", "are", "for", "in", "is", "of", "on", "the", "to", "what"}


def tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower())
            if token not in STOPWORDS}


@dataclass(frozen=True)
class Document:
    document_id: str
    passage_id: str
    text: str
    principals: frozenset[str]
    source_uri: str

    @property
    def checksum(self) -> str:
        return hashlib.sha256(self.text.encode()).hexdigest()


class QualityError(ValueError):
    pass


class KnowledgeStore:
    def __init__(self) -> None:
        self.documents: dict[str, Document] = {}
        self.checksums: set[str] = set()
        self.edges: dict[str, set[tuple[str, str]]] = defaultdict(set)

    def ingest(self, document: Document) -> None:
        if not document.document_id or not document.passage_id:
            raise QualityError("stable document and passage identifiers are required")
        if not document.text.strip():
            raise QualityError("empty passage")
        if not document.source_uri.startswith(("https://", "urn:")):
            raise QualityError("source provenance is required")
        if not document.principals:
            raise QualityError("an explicit access policy is required")
        if document.checksum in self.checksums:
            raise QualityError("duplicate content")
        self.documents[document.passage_id] = document
        self.checksums.add(document.checksum)

    def search(self, query: str, principal: str, limit: int = 5) -> list[dict[str, object]]:
        """Lexical baseline with authorization before scoring and return."""
        query_tokens = tokens(query)
        scored = []
        for document in self.documents.values():
            if principal not in document.principals:
                continue
            overlap = len(query_tokens & tokens(document.text))
            if overlap:
                score = overlap / max(1, len(query_tokens))
                scored.append((score, document))
        scored.sort(key=lambda item: (-item[0], item[1].passage_id))
        return [{"document_id": doc.document_id, "passage_id": doc.passage_id,
                 "source_uri": doc.source_uri, "score": score, "text": doc.text}
                for score, doc in scored[:limit]]

    def hybrid_search(self, query: str, principal: str,
                      semantic: dict[str, float], lexical_weight: float = 0.5,
                      limit: int = 5) -> list[dict[str, object]]:
        """Fuse normalized lexical overlap with externally supplied semantic scores."""
        if not 0 <= lexical_weight <= 1: raise ValueError("weight must be in [0, 1]")
        query_tokens, ranked = tokens(query), []
        for document in self.documents.values():
            if principal not in document.principals: continue
            lexical = len(query_tokens & tokens(document.text)) / max(1, len(query_tokens))
            vector = max(0.0, min(1.0, semantic.get(document.passage_id, 0.0)))
            score = lexical_weight * lexical + (1 - lexical_weight) * vector
            if score: ranked.append((score, lexical, vector, document))
        ranked.sort(key=lambda item: (-item[0], item[3].passage_id))
        return [{"document_id": doc.document_id, "passage_id": doc.passage_id,
                 "source_uri": doc.source_uri, "score": score,
                 "lexical_score": lexical, "semantic_score": vector, "text": doc.text}
                for score, lexical, vector, doc in ranked[:limit]]

    def add_edge(self, source: str, relation: str, target: str) -> None:
        if not all((source, relation, target)):
            raise QualityError("complete graph triple required")
        self.edges[source].add((relation, target))

    def path(self, source: str, target: str, max_hops: int = 4) -> list[str]:
        queue = deque([(source, [source])])
        visited = {source}
        while queue:
            node, path = queue.popleft()
            if node == target:
                return path
            if len(path) - 1 >= max_hops:
                continue
            for _relation, neighbor in sorted(self.edges[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []

def retrieval_metrics(expected: dict[str, set[str]], results: dict[str, list[str]], k: int) -> dict[str, float]:
    if k < 1 or not expected: raise ValueError("queries and positive k required")
    recalls, reciprocal = [], []
    for query, relevant in expected.items():
        ranked = results.get(query, [])[:k]
        recalls.append(len(set(ranked) & relevant) / max(1, len(relevant)))
        first = next((index for index, item in enumerate(ranked, 1) if item in relevant), None)
        reciprocal.append(1 / first if first else 0.0)
    return {f"recall@{k}": sum(recalls)/len(recalls), f"mrr@{k}": sum(reciprocal)/len(reciprocal)}
