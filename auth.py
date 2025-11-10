from fastapi import HTTPException
import bcrypt
from db import find_user, create_user

def login_user(username: str, password: str):
    user = find_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "username": username}

def register_user(username: str, password: str):
    if find_user(username):
        raise HTTPException(status_code=400, detail="User already exists")
    return create_user(username, password)
