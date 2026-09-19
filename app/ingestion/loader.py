from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document

def load_pdf(pdf_path: str) -> list[Document]:
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_file}")

    reader = PdfReader(str(pdf_file))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            documents.append(
    Document(
        page_content=text,
        metadata={
            "source": pdf_file.name,
            "page": page_number,
        },
    )
)

    return documents