from typing import TypedDict


class RAGState(TypedDict, total=False):
    question: str
    context: list[str]
    scores: list[float]
    answer: str
    is_relevant: bool