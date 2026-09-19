from langgraph.graph import END, START, StateGraph

from app.rag.nodes import (
    check_relevance_node,
    generate_node,
    refuse_node,
    retrieve_node,
)
from app.rag.state import RAGState


def route_after_relevance(state: RAGState):
    if state["is_relevant"]:
        return "generate"

    return "refuse"


def build_graph():
    graph = StateGraph(RAGState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("check_relevance", check_relevance_node)
    graph.add_node("generate", generate_node)
    graph.add_node("refuse", refuse_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "check_relevance")

    graph.add_conditional_edges(
        "check_relevance",
        route_after_relevance,
        {
            "generate": "generate",
            "refuse": "refuse",
        },
    )

    graph.add_edge("generate", END)
    graph.add_edge("refuse", END)

    return graph.compile()