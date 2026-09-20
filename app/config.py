import os

from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "agentic-ai-rag-v2",
)
PINECONE_NAMESPACE = os.getenv(
    "PINECONE_NAMESPACE",
    "agentic-ai",
)

EMBEDDING_MODEL = "llama-text-embed-v2"
EMBEDDING_DIMENSION = 1024

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MIN_RETRIEVAL_SCORE = 0.5

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://127.0.0.1:5500,http://localhost:5500"
    ).split(",")
    if origin.strip()
]