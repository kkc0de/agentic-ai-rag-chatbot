# 🤖 Agentic AI RAG Chatbot

> A grounded Retrieval-Augmented Generation (RAG) chatbot that answers questions strictly from the **Agentic AI eBook** using semantic retrieval, LangGraph, Pinecone, and an LLM.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-purple)
![Groq](https://img.shields.io/badge/Groq-LLM-black)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

</p>

---

## 🌐 Project Links

| Resource | Link |
|---|---|
| 🔴 Live Demo | **Coming Soon** |
| 💼 LinkedIn | **[Add LinkedIn Profile](#)** |
| 📦 GitHub | **This Repository** |

> The live deployment and LinkedIn link will be updated after deployment.

---

## 📌 Overview

This project implements a **Retrieval-Augmented Generation (RAG) chatbot** that answers user questions using information retrieved from an **Agentic AI eBook PDF**.

Instead of allowing the language model to answer using its general knowledge, the system retrieves relevant sections from the eBook and provides them as context to the LLM.

The system also includes a **relevance guard** that prevents the LLM from generating an answer when the retrieved content is not sufficiently relevant to the user's question.

The chatbot is exposed through a **FastAPI REST API** with interactive Swagger documentation.

---

## ✨ Features

- 📄 PDF document ingestion
- ✂️ Recursive text chunking
- 🧠 Local text embeddings using Sentence Transformers
- 🔎 Semantic similarity search using Pinecone
- 🔗 LangGraph-based RAG workflow
- 🤖 Groq-hosted LLM generation
- 🛡️ Context-grounded responses
- 🚫 Relevance guard for unrelated questions
- 📊 Pinecone similarity scores
- ⚡ FastAPI REST API
- 📚 Retrieved context included in API response
- 🧪 Swagger/OpenAPI documentation
- 🔐 Environment-variable based API key management
## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Agentic AI PDF   │
                    └──────────┬──────────┘
                               │
                    │   PDF Text Loader   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Text Chunking      │
                    │ Recursive Splitter  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Embeddings       │
                    │ MiniLM-L6-v2        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Pinecone       │
                    │    Vector Store     │
                    └──────────┬──────────┘
                               │
                         User Question
                               │
                               ▼
                    ┌─────────────────────┐
                               │
                               ▼
                    ┌─────────────────────┐
                    │     LangGraph       │
                    │   RAG Workflow      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Retrieval       │
                    │      Top-K = 4      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Relevance Guard     │
                    └──────┬───────┬──────┘
                           │       │
                     Relevant    Not Relevant
                           │       │
                           ▼       ▼
                    ┌──────────┐  ┌──────────────┐
                    │   LLM    │  │    Refuse    │
                    │ Generate │  │   Response   │
                    └────┬─────┘  └──────┬───────┘
                         │               │
                         └───────┬───────┘
                                 ▼
                         Final API Response
```

## 🔄 How It Works

### 1. PDF Ingestion

The Agentic AI eBook is loaded page-by-page using pypdf.

Each page is converted into a LangChain Document containing:

- Page content
- Source filename
- Page number

### 2. Text Chunking

The extracted documents are split into smaller chunks using RecursiveCharacterTextSplitter.

Current configuration:

- Chunk Size: 1000
- Chunk Overlap: 150

This allows the retrieval system to work with smaller, semantically meaningful pieces of the document.

### 3. Embeddings

Each chunk is converted into a numerical vector using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embedding dimension is:

```text
384
```

The same embedding model is used for both document chunks and user queries.

### 4. Vector Storage

The generated vectors are stored in Pinecone using cosine similarity.

Each stored vector also contains metadata such as:

- text
- source
- page
### 5. Retrieval

When a user submits a question:

```text
Question
   ↓
Embedding
   ↓
Pinecone similarity search
   ↓
Top 4 relevant chunks
```

The retrieved chunks and their similarity scores are passed to the LangGraph workflow.

### 6. Relevance Guard

The system checks the highest retrieved similarity score before calling the LLM.

If the score is below the configured relevance threshold, the system does not ask the LLM to generate an answer.

Instead, it returns:

```text
I could not find this information in the provided Agentic AI eBook.
```

This helps prevent unrelated questions from being answered using the LLM's general knowledge.

### 7. Grounded Generation

For relevant questions, the retrieved chunks are passed to the LLM as context.

The prompt explicitly instructs the model to:

- Use only the provided context
- Avoid outside knowledge
- Avoid inventing information
- Refuse when the answer is not present in the context

## 🧩 LangGraph Workflow

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
Relevant      Not Relevant
  │               │
  ▼               ▼
Generate         Refuse
  │               │
  └───────┬───────┘
          ▼
         END
  ```

  ## 🛠️ Tech Stack

  | Technology | Purpose |
  |---|---|
  | Python | Core implementation |
  | FastAPI | REST API |
  | LangGraph | RAG workflow orchestration |
  | LangChain | Prompting and document utilities |
  | Pinecone | Vector database |
  | Hugging Face / Sentence Transformers | Text embeddings |
  | Groq | LLM inference |
  | pypdf | PDF extraction |
  | Uvicorn | ASGI server |
  | Pydantic | API request/response validation |

  ## 📁 Project Structure
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
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd agentic-ai-rag-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

#### Windows

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a .env file in the project root.

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=agentic-ai-rag
PINECONE_NAMESPACE=agentic-ai

GROQ_API_KEY=your_groq_api_key
```

Never commit the .env file to GitHub.

## 📥 Index the eBook

Run the ingestion pipeline:

```bash
python scripts/ingest.py
```

The pipeline:

```text
PDF
 ↓
Load pages
 ↓
Create chunks
 ↓
Generate embeddings
 ↓
Upload vectors to Pinecone
```

## 🚀 Run the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 📚 API Documentation

FastAPI provides interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "agentic-ai-rag-chatbot"
}
```

## 💬 Chat API

### Endpoint

```text
POST /chat
```

### Request

```json
{
  "question": "What is Agentic AI?"
}
```

### Response

```json
{
  "answer": "Generated answer based on the retrieved eBook context.",
  "retrieved_context": [
    {
      "text": "Retrieved chunk from the Agentic AI eBook...",
      "score": 0.81
    }
  ],
  "retrieval_score": 0.81
}
```

retrieval_score represents the highest Pinecone similarity score for the retrieved results. It is not a probability or guaranteed confidence percentage.

## 🧪 Sample Queries

The following queries can be used to test the chatbot:

### In-domain queries
1. What is Agentic AI?

2. What are AI agents?

3. How do AI agents differ from traditional AI systems?

4. What are the key characteristics of Agentic AI?

### Out-of-domain query
5. What is the capital of France?

Expected behavior:

```text
I could not find this information in the provided Agentic AI eBook.
```

### Grounding test
6. Ask a question whose answer is not contained in the eBook.

The chatbot should refuse instead of relying on the LLM's general knowledge.

## 🛡️ Grounding & Safety

The chatbot is designed to keep responses grounded in the provided eBook.

Two layers are used:

### Retrieval Relevance Guard

A similarity threshold is applied to the retrieved results.

```text
High relevance
     ↓
LLM generation allowed

Low relevance
     ↓
Generation skipped
     ↓
Refusal response
```

### Prompt-Level Grounding

The LLM is explicitly instructed to answer only from the retrieved context and avoid outside knowledge.

These mechanisms reduce the risk of unsupported answers.

## 📊 Tested Behavior

The system has been tested with both relevant and unrelated questions.

### Relevant Query
Question:
What is Agentic AI?

The system retrieves relevant eBook chunks and generates an answer using the retrieved context.

### Unrelated Query
Question:
What is the capital of France?

The retrieval scores are significantly lower than those observed for relevant eBook questions, triggering the relevance guard.

The system returns the grounded refusal response instead of answering from general knowledge.

## 🔮 Future Improvements

Possible future improvements include:

- 💬 Web-based chat interface
- 📡 Streaming responses
- 🧠 Conversation memory
- 🔍 Hybrid search
- 🎯 Reranking retrieved chunks
- 🐳 Docker deployment
- ☁️ Cloud deployment
- 📈 RAG evaluation and tracing
- 🔐 API authentication

## 👨‍💻 Author

Krishna Kant Sharma

AI / ML Engineer | Generative AI | RAG | LangGraph | Python

### Connect
💼 LinkedIn: Add LinkedIn URL
🌐 Live Demo: Coming Soon
📦 GitHub: Add Repository URL

## 📄 License

This project is licensed under the MIT License.

## 🖥️ Demo

[UI Screenshot / GIF]

Live Demo → ...