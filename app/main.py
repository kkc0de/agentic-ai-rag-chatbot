from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS

from app.models.schemas import ChatRequest, ChatResponse
from app.rag.graph import build_graph


app = FastAPI(
    title="Agentic AI RAG Chatbot",
    description="RAG-based chatbot grounded in the Agentic AI eBook.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


rag_graph = build_graph()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "agentic-ai-rag-chatbot",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = rag_graph.invoke(
            {
                "question": request.question,
            }
        )

        if result["is_relevant"]:
            context = [
                {
                    "text": text,
                    "score": score,
                }
                for text, score in zip(
                    result["context"],
                    result["scores"],
                )
            ]
        else:
            context = []

        return ChatResponse(
            answer=result["answer"],
            retrieved_context=context,
            retrieval_score=max(result["scores"]),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG pipeline failed: {str(e)}",
        )