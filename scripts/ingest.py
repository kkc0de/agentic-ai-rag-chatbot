import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.ingestion.loader import load_pdf
from app.ingestion.chunker import split_documents
from app.ingestion.indexer import index_documents


PDF_PATH = PROJECT_ROOT / "data" / "Ebook-Agentic-AI.pdf"


def main():
    documents = load_pdf(PDF_PATH)
    chunks = split_documents(documents)

    print(f"Loaded documents: {len(documents)}")
    print(f"Created chunks: {len(chunks)}")

    count = index_documents(chunks)

    print(f"Indexed vectors: {count}")


if __name__ == "__main__":
    main()