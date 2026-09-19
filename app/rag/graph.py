from langgraph.graph import END, START, StateGraph

from app.rag.nodes import answer_node, retrieve_node
from app.rag.state import RAGState


def build_graph(retriever):
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", lambda state: retrieve_node(state, retriever))
    graph.add_node("answer", answer_node)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)
    return graph.compile()
