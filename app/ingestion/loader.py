from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


def load_documents(data_dir: Path) -> list[Document]:
    """Load supported documents from the data directory."""
    documents: list[Document] = []
    for path in sorted(data_dir.iterdir()):
        if path.suffix.lower() == ".pdf":
            documents.extend(PyPDFLoader(str(path)).load())
        elif path.suffix.lower() in {".txt", ".md"}:
            documents.extend(TextLoader(str(path), encoding="utf-8").load())
    return documents
