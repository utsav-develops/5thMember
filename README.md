# 5th Member — Local RAG AI Chat Engine

**5th Member** is a self-hosted conversational AI stack that remembers over time using **Ollama**, **Qdrant**, and **FastAPI**.  
It acts as your team’s quiet 5th member — listening, learning, and responding with context-aware intelligence.

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/e274c6e6-deed-4fec-94e2-5a9f113d4fe0" style="border-radius:12px;" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/9bd5fdf9-167c-422c-b477-ff5922952737" style="border-radius:12px;" />


---

## Features

-  **Conversational Memory:** Stores and recalls chat history through Qdrant vector search  
-  **RAG Integration:** Retrieves past context to enrich current prompts automatically  
-  **FastAPI Backend:** Lightweight async API server ready for local or containerized deployment  
-  **Ollama Integration:** Uses locally-running Ollama models for offline or private inference  
-  **Docker Support:** Works seamlessly with local Dockerized Qdrant setup  
-  **Progressive Summarization:** Keeps your long-term memory concise and relevant  

---

## Tech Stack

| Component | Purpose |
|------------|----------|
| **FastAPI** | API framework for async chat & RAG endpoints |
| **Ollama** | Local LLM runner (e.g., llama3, mistral, codellama) |
| **Qdrant** | Vector database to store and retrieve conversation embeddings |
| **httpx** | Async HTTP client for streaming LLM responses |
| **Python 3.11+** | Core runtime |

---

## Setup Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/utsav-develops/5thMember.git
cd 5thMember
````

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv .venv
# Activate:
source .venv/bin/activate      # macOS / Linux
# or
.venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧩 Environment Configuration

Create a `.env` file in your project root directory:

```env
# Ollama Settings
OLLAMA_URL=http://localhost:11434
OLLAMA_TEXT_MODEL=llama3
OLLAMA_EMBED_MODEL=embedding-model

# Qdrant Settings
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=memories
```

---

## 🐳 Running Services

### 🧠 Run Qdrant via Docker

```bash
docker run -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

### ⚙️ Run Ollama (Local LLM)

```bash
ollama pull llama3
ollama serve
```

> 💡 You can also use other models like `mistral`, `codellama`, or `phi3` by updating the `.env` file.

---

## 🚀 Launch the FastAPI Server

```bash
uvicorn main:app --reload --port 8000
```

> Server runs at: [http://localhost:8000](http://localhost:8000)

---

## 💡 Usage Examples

### 🔹 Basic Chat Endpoint

Send messages via `/chat`:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum entanglement"}'
```

### 🔹 RAG Chat Endpoint (with memory)

Uses Qdrant-stored context to enhance replies:

```bash
curl -X POST http://localhost:8000/rag-chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "prompt": "Remind me what we discussed earlier about ML agents"}'
```

---

## 🧠 How RAG Memory Works

Every message is **embedded and stored** in Qdrant.
When a new message arrives:

1. Qdrant searches for similar past messages by vector similarity
2. Relevant context is retrieved
3. A new, context-rich prompt is constructed
4. Ollama generates a response with awareness of previous conversations
5. Older memories are periodically summarized and compressed

---

## 📂 Project Structure

```
5thMember/
│
├── main.py           # FastAPI app and API endpoints
├── utils.py          # RAG logic, summarization, Qdrant operations
├── db.py             # Database (Qdrant) user management
├── requirements.txt  # Python dependencies
├── .env              # Environment variables
└── README.md         # Documentation (you’re reading this!)
```

---

## 🧰 Example Models

You can use any Ollama-supported model:

```bash
ollama pull mistral
ollama pull phi3
ollama pull codellama
```

Then, update `.env`:

```env
OLLAMA_TEXT_MODEL=phi3
```

---

## 🧑‍💻 Development Tips

* Use `--reload` flag in Uvicorn for hot-reloading during development
* Check your Qdrant dashboard at [http://localhost:6333/dashboard](http://localhost:6333/dashboard)
* Logs can be viewed via Docker:

  ```bash
  docker logs <container_id>
  ```

---

## 🧾 Example `.env` Template

```env
# LLM Settings
OLLAMA_URL=http://localhost:11434
OLLAMA_TEXT_MODEL=llama3
OLLAMA_EMBED_MODEL=embedding-model

# Vector DB
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=memories
```

---

## 📜 License

**MIT License © 2025 — Created by utsav-develops**

> “The best teammate never sleeps — it just keeps learning.”

