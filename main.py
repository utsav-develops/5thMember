# The 5th Member

import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from utils import ensure_collection, get_embedding, search_memories, upsert_memory, generate_rag_chat
from fastapi.responses import StreamingResponse
from db import init_db
from auth import login_user, register_user

load_dotenv()
init_db()

app = FastAPI(title='The 5th Member - Memory-Augmented Chatbot')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    password: str


TOP_K = int(os.getenv('TOP_K', '6'))

# Ensure qdrant collection on startup. Adjust embedding dim if your embed model uses other size.
@app.on_event('startup')
async def startup_event():
    ensure_collection(dim=1024)

class ChatRequest(BaseModel):
    user_id: str
    session_id: str
    message: str

class MemoryRequest(BaseModel):
    user_id: str
    text: str
    tags: Optional[List[str]] = None

@app.post('/memory')
async def add_memory(payload: MemoryRequest):
    # create embedding and upsert to qdrant
    print("adding memory")
    emb = await get_embedding(payload.text)
    mid = await upsert_memory(payload.text, emb, payload.user_id, metadata={'tags': payload.tags or []})
    return {'memory_id': mid}

sessions = {}

@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "")
    user_id = body.get("user_id", "")
    return StreamingResponse(generate_rag_chat(prompt, user_id), media_type="text/plain")

@app.post("/register")
def register(user: User):
    return register_user(user.username, user.password)

@app.post("/login")
def login(user: User):
    return login_user(user.username, user.password)
