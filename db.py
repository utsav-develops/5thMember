import os
import uuid
import bcrypt
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from qdrant_client.http.models import PointIdsList

# Load env vars
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "users")

# Connect to Qdrant (remove protocol for QdrantClient)
qdrant = QdrantClient(url=QDRANT_URL.split("://")[-1])

# Initialize user collection if not exists
def init_db():
    collections = qdrant.get_collections().collections
    if not any(c.name == QDRANT_COLLECTION for c in collections):
        qdrant.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config={"size": 1, "distance": "Cosine"}  # dummy vector field
        )

def create_user(username: str, password: str):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user_id = str(uuid.uuid4())
    qdrant.upsert(
        collection_name=QDRANT_COLLECTION,
        points=[
            PointStruct(
                id=user_id,
                vector=[0.0] * 1024,  # placeholder vector
                payload={"username": username, "password": hashed},
            )
        ],
    )
    return {"id": user_id, "username": username}

def find_user(username: str):
    scroll_result, _ = qdrant.scroll(
        collection_name=QDRANT_COLLECTION,
        scroll_filter=Filter(
            must=[FieldCondition(key="username", match=MatchValue(value=username))]
        ),
        limit=1
    )
    return scroll_result[0].payload if scroll_result else None
