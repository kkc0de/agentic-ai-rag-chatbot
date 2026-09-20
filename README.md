# 🤖 Agentic AI RAG Chatbot

> A production-ready Retrieval-Augmented Generation (RAG) chatbot that answers questions strictly from the **Agentic AI eBook** using semantic retrieval, Pinecone, LangGraph, FastAPI, and Groq.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green?logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-purple)
![Groq](https://img.shields.io/badge/Groq-LLM-black)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

</p>

---

## 🌐 Project Links

| Resource | Link |
|---|---|
| 🚀 Live Demo | https://agentic-ai-rag-frontend.vercel.app/ |
| ⚡ Backend API | https://agentic-ai-rag-chatbot.vercel.app |
| 📚 API Docs | https://agentic-ai-rag-chatbot.vercel.app/docs |
| 💼 LinkedIn | https://www.linkedin.com/in/krishna-sharma-veltr0/ |
| 📦 GitHub | https://github.com/kkc0de/agentic-ai-rag-chatbot |

---

## 📌 Overview

This project implements a **Retrieval-Augmented Generation (RAG) chatbot** that answers questions using information retrieved from an **Agentic AI eBook PDF**.

The system is designed to keep responses grounded in the provided document instead of allowing the language model to freely answer from general knowledge.

When a user asks a question, the system:

1. Converts the query into an embedding.
2. Searches Pinecone for semantically relevant document chunks.
3. Checks whether the retrieved content is sufficiently relevant.
4. Uses LangGraph to control the RAG workflow.
5. Generates an answer using the retrieved context.
6. Returns the final answer along with retrieved context and similarity scores.

For unrelated questions, the system refuses to answer rather than relying on outside knowledge.

---

## ✨ Features

- 📄 PDF document ingestion
- ✂️ Recursive text chunking
- 🧠 Pinecone-hosted text embeddings
- 🔎 Semantic similarity search with Pinecone
- 🔗 LangGraph-based RAG workflow
- 🤖 Groq-hosted LLM inference
- 🛡️ Context-grounded generation
- 🚫 Relevance guard for unrelated questions
- 📊 Pinecone similarity scores
- 📚 Retrieved context returned through the API
- ⚡ FastAPI REST API
- 📖 Swagger/OpenAPI documentation
- 🌐 Responsive web chat interface
- ☁️ Vercel deployment
- 🔐 Environment-variable based API key management
- 🔄 Separate frontend and backend deployment

---

# 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │   Agentic AI eBook   │
                    │         PDF          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      PDF Loader      │
                    │        pypdf         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Text Chunking     │
                    │ Recursive Splitter   │
                    │ 1000 / 150 overlap   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Embeddings      │
                    │ llama-text-embed-v2  │
                    │      1024-dim        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Pinecone        │
                    │     Vector Store     │
                    └──────────┬───────────┘
                               │
                               │
                         User Question
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │       /chat          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      LangGraph       │
                    │    RAG Workflow      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Retrieval       │
                    │       Top-K = 4      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Relevance Guard    │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                 Relevant             Not Relevant
                    │                     │
                    ▼                     ▼
             ┌─────────────┐      ┌─────────────┐
             │   Groq LLM   │      │    Refuse    │
             │   Generate   │      │   Response   │
             └──────┬──────┘      └──────┬──────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌──────────────────────┐
                    │  Answer + Context +  │
                    │   Retrieval Score    │
                    └──────────────────────┘
```

---

# 🔄 RAG Workflow

## 1. PDF Ingestion

The Agentic AI eBook is loaded page-by-page using `pypdf`.

Each page is converted into a LangChain `Document` containing:

- Page content
- Source filename
- Page number

The current eBook produces **59 text-bearing pages** during ingestion.

---

## 2. Text Chunking

The extracted documents are split using LangChain's `RecursiveCharacterTextSplitter`.

### Configuration

```text
Chunk Size:    1000
Chunk Overlap: 150
```

The ingestion pipeline currently produces **114 chunks** from the eBook.

Chunk metadata is preserved so retrieved results can be traced back to their source page.

---

## 3. Embeddings

Document chunks and user queries are converted into vector representations using Pinecone's hosted embedding model:

```text
llama-text-embed-v2
```

Embedding dimension:

```text
1024
```

Using hosted inference avoids loading a local transformer model into the application process, keeping the deployed API lightweight.

---

## 4. Vector Storage

The generated embeddings are stored in **Pinecone** using cosine similarity.

The current vector index is:

```text
agentic-ai-rag-v2
```

Each vector stores metadata including:

- Text
- Source
- Page number

---

## 5. Retrieval

When a user submits a question:

```text
User Question
      ↓
Query Embedding
      ↓
Pinecone Similarity Search
      ↓
Top 4 Retrieved Chunks
      ↓
LangGraph Workflow
```

The retrieved chunks and their similarity scores are passed into the RAG workflow.

---

## 6. Relevance Guard

The system checks the highest retrieved similarity score before allowing LLM generation.

If the highest score does not meet the configured relevance threshold, the generation step is skipped.

The chatbot returns:

```text
I could not find this information in the provided Agentic AI eBook.
```

This prevents unrelated questions from being answered using the LLM's general knowledge.

---

## 7. Grounded Generation

For relevant questions, the retrieved chunks are passed to the Groq-hosted LLM as context.

The prompt instructs the model to:

- Use only the provided context
- Avoid outside knowledge
- Avoid inventing information
- Refuse when the answer cannot be found in the provided context
- Keep responses clear and concise

---

# 🧩 LangGraph Workflow

The RAG pipeline is orchestrated using LangGraph.

```text
START
  │
  ▼
Retrieve
  │
  ▼
Check Relevance
  │
  ├───────────────┐
  │               │
  ▼               ▼
Relevant      Not Relevant
  │               │
  ▼               ▼
Generate        Refuse
  │               │
  └───────┬───────┘
          │
          ▼
         END
```

This separates retrieval, relevance checking, generation, and refusal into explicit workflow nodes.

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core implementation |
| FastAPI | REST API |
| LangGraph | RAG workflow orchestration |
| LangChain | Document and prompt utilities |
| Pinecone | Vector database and hosted embeddings |
| llama-text-embed-v2 | Text embeddings |
| Groq | LLM inference |
| pypdf | PDF extraction |
| Uvicorn | ASGI server |
| Pydantic | Request/response validation |
| HTML/CSS/JavaScript | Frontend chat interface |
| Vercel | Deployment |

---

# 📁 Project Structure

```text
agentic-ai-rag-chatbot/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   └── indexer.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── graph.py
│   │
│   └── models/
│       ├── __init__.py
│       └── schemas.py
│
├── data/
│   ├── .gitkeep
│   └── Ebook-Agentic-AI.pdf
│
├── scripts/
│   ├── __init__.py
│   └── ingest.py
│
├── tests/
│   ├── __init__.py
│   └── test_imports.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── config.js
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

---

# ⚙️ Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/kkc0de/agentic-ai-rag-chatbot.git
cd agentic-ai-rag-chatbot
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the environment

### Windows

```powershell
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-ai-rag-v2
PINECONE_NAMESPACE=agentic-ai
GROQ_API_KEY=your_groq_api_key
```

Never commit the `.env` file to GitHub.

The repository includes `.env.example` as a template.

---

# 📥 Index the eBook

Run the ingestion pipeline:

```bash
python scripts/ingest.py
```

The pipeline performs:

```text
PDF
 ↓
Load Pages
 ↓
Create Chunks
 ↓
Generate Embeddings
 ↓
Upload Vectors to Pinecone
```

The current eBook ingestion creates 114 vectorized chunks.

---

# 🚀 Run the Backend Locally

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The local API will run on:

```text
http://127.0.0.1:8000
```

The local frontend can be served separately from the `frontend/` directory.

---

# 📚 API Documentation

The deployed API provides interactive Swagger documentation:

**[https://agentic-ai-rag-chatbot.vercel.app/docs](https://agentic-ai-rag-chatbot.vercel.app/docs)**

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "agentic-ai-rag-chatbot"
}
```

---

# 💬 Chat API

## Endpoint

```http
POST /chat
```

## Request

```json
{
  "question": "What is Agentic AI?"
}
```

## Response

```json
{
  "answer": "Generated answer based on the retrieved eBook context.",
  "retrieved_context": [
    {
      "text": "Retrieved chunk from the Agentic AI eBook...",
      "score": 0.58
    }
  ],
  "retrieval_score": 0.58
}
```

### Response Fields

| Field | Description |
|---|---|
| `answer` | Final grounded response generated by the LLM |
| `retrieved_context` | Retrieved eBook chunks used by the RAG pipeline |
| `score` | Pinecone similarity score for an individual chunk |
| `retrieval_score` | Highest retrieved similarity score |

> `retrieval_score` is a similarity score, not a probability or guaranteed confidence percentage.

---

# 🧪 Sample Queries

The chatbot can be tested with questions such as:

### In-domain queries

```text
What is Agentic AI?
```

```text
What are the key characteristics of Agentic AI?
```

```text
What are AI agents?
```

```text
How do AI agents differ from traditional AI systems?
```

```text
What are some use cases of Agentic AI?
```

### Out-of-domain query

```text
What is the capital of France?
```

Expected behavior:

```text
I could not find this information in the provided Agentic AI eBook.
```

The system should refuse rather than answer using the LLM's general knowledge.

---

# 🛡️ Grounding Strategy

The chatbot uses two complementary grounding mechanisms.

## 1. Retrieval Relevance Guard

```text
Query
  ↓
Pinecone Retrieval
  ↓
Similarity Check
  ↓
 ┌───────────────┐
 │               │
High Relevance  Low Relevance
 │               │
 ▼               ▼
Generate       Refuse
```

Low-relevance queries do not proceed to LLM generation.

---

## 2. Prompt-Level Grounding

The LLM receives explicit instructions to:

- Use only retrieved context
- Avoid external knowledge
- Avoid assumptions
- Avoid fabricated information
- Refuse when the required information is unavailable

Together, these mechanisms help keep responses grounded in the source document.

---

# 🌐 Deployment

The application is deployed as two components.

### Frontend

Hosted on Vercel:

[https://agentic-ai-rag-frontend.vercel.app/](https://agentic-ai-rag-frontend.vercel.app/)

### Backend

FastAPI backend hosted on Vercel:

[https://agentic-ai-rag-chatbot.vercel.app/](https://agentic-ai-rag-chatbot.vercel.app/)

### API Documentation

[https://agentic-ai-rag-chatbot.vercel.app/docs](https://agentic-ai-rag-chatbot.vercel.app/docs)

The frontend automatically uses the local backend during local development and the deployed backend when running from the production frontend.

---

# ✅ Tested Behavior

The deployed application has been tested with both relevant and unrelated questions.

### Relevant Query

```text
What is Agentic AI?
```

The system retrieves relevant chunks from the Agentic AI eBook and generates an answer using the retrieved context.

### Unrelated Query

```text
What is the capital of France?
```

The relevance guard identifies the query as unrelated to the indexed eBook content and returns the grounded refusal response.

### Additional verified queries

The deployed UI was also tested with questions covering:

- Agentic AI concepts
- AI agents
- Characteristics of Agentic AI
- Differences between agentic and traditional AI systems
- Agentic AI use cases

---

# 🔮 Future Improvements

Potential improvements include:

- 📡 Streaming responses
- 🧠 Conversation memory
- 🔍 Hybrid search
- 🎯 Retrieval reranking
- 📈 Automated RAG evaluation
- 🔎 LangSmith tracing
- 🔐 API authentication
- 🐳 Docker support
- 📊 Advanced retrieval analytics
- ⚡ Response caching

---

# 👨‍💻 Author

## Krishna Kant Sharma

**AI / ML Engineer | Generative AI | RAG | LangGraph | Python**

### Connect

💼 **LinkedIn:**
[https://www.linkedin.com/in/krishna-sharma-veltr0/](https://www.linkedin.com/in/krishna-sharma-veltr0/)

🚀 **Live Project:**
[https://agentic-ai-rag-frontend.vercel.app/](https://agentic-ai-rag-frontend.vercel.app/)

📦 **GitHub:**
[https://github.com/kkc0de/agentic-ai-rag-chatbot](https://github.com/kkc0de/agentic-ai-rag-chatbot)

---

# 📄 License

This project's source code is licensed under the MIT License.

The Agentic AI eBook used as the knowledge base remains the property
of its respective copyright holders.