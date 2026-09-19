from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.config import CHAT_MODEL, TOP_K
from app.rag.state import RAGState

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Answer using only the provided context. If the answer is not in it, say you do not know."),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])


def retrieve_node(state: RAGState, retriever) -> RAGState:
    return {"context": retriever.invoke(state["question"])}


def answer_node(state: RAGState) -> RAGState:
    model = ChatOpenAI(model=CHAT_MODEL, temperature=0)
    context = "\n\n".join(document.page_content for document in state.get("context", []))
    answer = (PROMPT | model).invoke({"context": context, "question": state["question"]})
    sources = sorted({document.metadata.get("source", "unknown") for document in state.get("context", [])})
    return {"answer": answer.content, "sources": sources}


def make_retriever(vector_store):
    return vector_store.as_retriever(search_kwargs={"k": TOP_K})
