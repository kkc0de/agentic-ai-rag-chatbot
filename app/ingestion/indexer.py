from pinecone import Pinecone, ServerlessSpec

from app.config import (
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    PINECONE_NAMESPACE,
)


def create_pinecone_client():
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is not set")

    return Pinecone(api_key=PINECONE_API_KEY)


def create_pinecone_index():
    pc = create_pinecone_client()

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


def embed_texts(texts: list[str], input_type: str):
    pc = create_pinecone_client()

    response = pc.inference.embed(
        model=EMBEDDING_MODEL,
        inputs=[{"text": text} for text in texts],
        parameters={
            "input_type": input_type,
            "truncate": "END",
        },
    )

    return [item["values"] for item in response.data]


def index_documents(documents):
    index = create_pinecone_index()

    batch_size = 32
    total_indexed = 0

    for start in range(0, len(documents), batch_size):
        batch = documents[start:start + batch_size]

        texts = [
            document.page_content
            for document in batch
        ]

        embeddings = embed_texts(
            texts,
            input_type="passage",
        )

        vectors = []

        for i, (document, vector) in enumerate(
            zip(batch, embeddings),
            start=start,
        ):
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

        total_indexed += len(vectors)

    return total_indexed


def retrieve(query: str, top_k: int = 4):
    index = create_pinecone_index()

    query_embedding = embed_texts(
        [query],
        input_type="query",
    )[0]

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=PINECONE_NAMESPACE,
    )

    return results