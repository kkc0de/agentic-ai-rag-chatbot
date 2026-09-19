from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, MIN_RETRIEVAL_SCORE
from app.ingestion.indexer import retrieve
from app.rag.state import RAGState


def create_llm():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set")

    return ChatGroq(
        model="openai/gpt-oss-safeguard-20b",
        temperature=0,
    )


def retrieve_node(state: RAGState) -> RAGState:
    question = state["question"]

    results = retrieve(question, top_k=4)

    context = []
    scores = []

    for match in results["matches"]:
        metadata = match["metadata"]

        context.append(metadata["text"])
        scores.append(match["score"])

    return {
        **state,
        "context": context,
        "scores": scores,
    }


def check_relevance_node(state: RAGState) -> RAGState:
    scores = state["scores"]

    if not scores:
        return {
            **state,
            "is_relevant": False,
        }

    highest_score = max(scores)

    return {
        **state,
        "is_relevant": highest_score >= MIN_RETRIEVAL_SCORE,
    }


def generate_node(state: RAGState) -> RAGState:
    question = state["question"]
    context = state["context"]

    context_text = "\n\n---\n\n".join(context)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a question-answering assistant.

Answer the user's question ONLY using the provided context
from the Agentic AI eBook.

Rules:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the answer cannot be found in the context, say:
"I could not find this information in the provided Agentic AI eBook."
4. Keep the answer clear and concise.

Context:
{context}
""",
            ),
            ("human", "{question}"),
        ]
    )

    llm = create_llm()
    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context_text,
            "question": question,
        }
    )

    return {
        **state,
        "answer": response.content,
    }


def refuse_node(state: RAGState) -> RAGState:
    return {
        **state,
        "answer": (
            "I could not find this information in the provided "
            "Agentic AI eBook."
        ),
    }