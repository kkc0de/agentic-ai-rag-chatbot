# Agentic AI RAG Chatbot

A small LangGraph-based RAG chatbot scaffold for loading local PDFs/text files, indexing them with Chroma, and answering questions with an OpenAI model.

## Setup

```powershell
cd agentic-ai-rag-chatbot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add `OPENAI_API_KEY` to `.env`, then put `.pdf`, `.txt`, or `.md` files in `data/`.

## Run

```powershell
python scripts/ingest.py
python run.py
```

The first command creates the local Chroma index. The second starts a simple terminal chat prompt.
