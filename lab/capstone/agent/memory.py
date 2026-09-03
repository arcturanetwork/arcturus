"""Comparable memory policies with explicit retention behavior."""

from dataclasses import dataclass, field

from capstone.agent.knowledge import tokens


@dataclass
class Message:
    turn: int
    text: str


@dataclass
class WindowMemory:
    size: int
    messages: list[Message] = field(default_factory=list)

    def add(self, message: Message) -> None:
        self.messages = (self.messages + [message])[-self.size:]

    def recall(self, query: str) -> list[Message]:
        return list(self.messages)


@dataclass
class RetrievalMemory:
    messages: list[Message] = field(default_factory=list)

    def add(self, message: Message) -> None:
        self.messages.append(message)

    def recall(self, query: str) -> list[Message]:
        terms = tokens(query)
        return [message for message in self.messages
                if terms & tokens(message.text)]


def compare_memory() -> dict[str, object]:
    conversation = [
        Message(1, "project codename is aurora"), Message(2, "use private networking"),
        Message(3, "prefer weekly reports"), Message(4, "budget is constrained"),
    ]
    window, retrieval = WindowMemory(2), RetrievalMemory()
    for message in conversation:
        window.add(message)
        retrieval.add(message)
    query = "what is the project codename"
    window_hits, retrieval_hits = window.recall(query), retrieval.recall(query)
    return {
        "query": query,
        "window_turns": [item.turn for item in window_hits],
        "retrieval_turns": [item.turn for item in retrieval_hits],
        "window_found_fact": any("aurora" in item.text for item in window_hits),
        "retrieval_found_fact": any("aurora" in item.text for item in retrieval_hits),
        "tradeoff": "window is bounded and recent; retrieval preserves older relevant facts but needs retention/access controls",
    }
