from pathlib import Path

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.config import DATA_DIR, EMBEDDING_MODEL
from app.rag.graph import build_graph


if __name__ == "__main__":
    index_dir = DATA_DIR / "chroma"
    if not index_dir.exists():
        raise SystemExit("No index found. Add documents to data/ and run: python scripts/ingest.py")

    store = Chroma(
        persist_directory=str(index_dir),
        embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
    )
    graph = build_graph(store.as_retriever())
    question = input("Question: ").strip()
    result = graph.invoke({"question": question})
    print(f"\n{result['answer']}\n")
    if result.get("sources"):
        print("Sources:")
        print("\n".join(f"- {Path(source).name}" for source in result["sources"]))
