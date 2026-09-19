from pathlib import Path

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.config import EMBEDDING_MODEL


def build_index(documents, persist_directory: Path) -> Chroma:
    """Create or replace a local Chroma index for document chunks."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(persist_directory),
    )
