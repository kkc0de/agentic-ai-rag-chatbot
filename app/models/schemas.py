from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


class RetrievedContext(BaseModel):
    text: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    retrieved_context: list[RetrievedContext]
    retrieval_score: float