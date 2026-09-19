from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec

from app.config import (
    EMBEDDING_DIMENSION,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE,
)


def create_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_pinecone_index():
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is not set")

    pc = Pinecone(api_key=PINECONE_API_KEY)

    if not pc.has_index(PINECONE_INDEX_NAME):
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            ),
        )

    return pc.Index(PINECONE_INDEX_NAME)


def index_documents(documents):
    embedding_model = create_embedding_model()
    index = create_pinecone_index()

    vectors = []

    for i, document in enumerate(documents):
        vector = embedding_model.embed_query(document.page_content)

        vectors.append(
            {
                "id": f"chunk-{i:04d}",
                "values": vector,
                "metadata": {
                    "text": document.page_content,
                    "source": document.metadata.get("source"),
                    "page": document.metadata.get("page"),
                },
            }
        )

    index.upsert(
        vectors=vectors,
        namespace=PINECONE_NAMESPACE,
    )

    return len(vectors)


def retrieve(query: str, top_k: int = 4):
    embedding_model = create_embedding_model()
    index = create_pinecone_index()

    query_vector = embedding_model.embed_query(query)

    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        namespace=PINECONE_NAMESPACE,
    )

    return results