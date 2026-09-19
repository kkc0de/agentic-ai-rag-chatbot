from app.config import DATA_DIR
from app.ingestion.chunker import split_documents
from app.ingestion.indexer import build_index
from app.ingestion.loader import load_documents


if __name__ == "__main__":
    documents = load_documents(DATA_DIR)
    chunks = split_documents(documents)
    build_index(chunks, DATA_DIR / "chroma")
    print(f"Indexed {len(chunks)} chunks from {len(documents)} documents.")
