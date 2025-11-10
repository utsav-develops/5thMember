import os
import json
import httpx
import datetime
import uuid
import bcrypt
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue, Distance
from qdrant_client.http.models import PointIdsList
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "memories")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "embedding-model")
OLLAMA_TEXT_MODEL = os.getenv("OLLAMA_TEXT_MODEL", "text-model")

qdrant = QdrantClient(url=QDRANT_URL.split("://")[-1])

# Ensure collection exists
def ensure_collection(dim: int = 1024):
    try:
        qdrant.get_collection(collection_name=QDRANT_COLLECTION)
    except Exception:
        qdrant.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config={"size": dim, "distance": Distance.COSINE},
        )

ensure_collection()

# ==============================
# EMBEDDING
# ==============================
async def get_embedding(text: str) -> List[float]:
    async with httpx.AsyncClient() as client:
        payload = {"model": OLLAMA_EMBED_MODEL, "input": text}
        r = await client.post(f"{OLLAMA_URL}/api/embed", json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        if "embeddings" in data and isinstance(data["embeddings"], list):
            return data["embeddings"][0]
        raise RuntimeError(f"Unexpected embedding response: {data}")

# ==============================
# MEMORY MANAGEMENT
# ==============================
async def search_memories(embedding: List[float], top_k: int = 6, user_id: str = None):
    filter_ = {"must": [{"key": "user_id", "match": {"value": user_id}}]} if user_id else None
    hits = qdrant.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=embedding,
        limit=top_k,
        query_filter=filter_,
    )
    return [{"id": h.id, "payload": h.payload, "score": h.score} for h in hits]

async def upsert_memory(text: str, embedding: List[float], user_id: str, metadata: Dict[str, Any] = None):
    if metadata is None:
        metadata = {}
    payload = {"text": text, "user_id": user_id, **metadata}
    point_id = str(uuid.uuid4())
    qdrant.upsert(
        collection_name=QDRANT_COLLECTION,
        points=[{"id": point_id, "vector": embedding, "payload": payload}],
    )
    return point_id

# ==============================
# PROGRESSIVE SUMMARIZATION
# ==============================
MAX_CONTEXT_CHARS = 3000
SUMMARY_THRESHOLD = 2500
SUMMARY_BATCH_SIZE = 5

async def progressive_summarize(user_id: str):
    memories = await search_memories([0]*1024, top_k=100, user_id=user_id)
    memories.sort(key=lambda m: m['payload'].get('timestamp', ''))
    old_memories = [m for m in memories if m['payload'].get('type') in ("user_input", "assistant_reply")]
    total_chars = sum(len(m["payload"]["text"]) for m in old_memories)

    if total_chars < SUMMARY_THRESHOLD:
        return

    to_summarize = old_memories[:SUMMARY_BATCH_SIZE]
    combined_text = "\n---\n".join([m["payload"]["text"] for m in to_summarize])
    prompt = f"Summarize this conversation into concise key facts:\n{combined_text}"

    summary = ""
    async with httpx.AsyncClient(timeout=None) as client:
        payload = {"model": OLLAMA_TEXT_MODEL, "prompt": prompt, "stream": False}
        r = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        r.raise_for_status()
        data = r.json()
        summary = data.get("response", "")

    summary_embedding = await get_embedding(summary)
    await upsert_memory(
        text=summary,
        embedding=summary_embedding,
        user_id=user_id,
        metadata={"type": "summary", "timestamp": datetime.datetime.utcnow().isoformat()}
    )


# ==============================
# RAG-ENABLED CHAT
# ==============================
async def generate_rag_chat(prompt: str, user_id: str):
    # 1. Summarize old memories
    await progressive_summarize(user_id)

    # 2. Embed prompt
    embedding = await get_embedding(prompt)

    # 3. Retrieve top relevant memories
    memories = await search_memories(embedding, top_k=8, user_id=user_id)
    context_texts = [m["payload"]["text"] for m in memories]

    # 4. Construct final prompt with context
    final_prompt = f"Context:\n{'---\n'.join(context_texts)}\n\nUser: {prompt}\nAssistant:"

    # 5. Stream Ollama response token-by-token
    async with httpx.AsyncClient(timeout=None) as client:
        payload = {"model": OLLAMA_TEXT_MODEL, "prompt": final_prompt, "stream": True}
        async with client.stream("POST", f"{OLLAMA_URL}/api/generate", json=payload) as r:
            async for line in r.aiter_lines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]
                except json.JSONDecodeError:
                    continue

    # 6. Save user prompt & assistant response
    await upsert_memory(prompt, embedding, user_id, metadata={"type": "user_input", "timestamp": datetime.datetime.utcnow().isoformat()})
    reply_embedding = await get_embedding(final_prompt)
    await upsert_memory(final_prompt, reply_embedding, user_id, metadata={"type": "assistant_reply", "timestamp": datetime.datetime.utcnow().isoformat()})
