from fastapi import APIRouter, HTTPException
from services.mongo import db
from security import sign_jwt
from passlib.hash import bcrypt
import os

router = APIRouter()

@router.post("/bootstrap")
def bootstrap():
    u = db.users.find_one({"email": os.getenv("ADMIN_EMAIL")})
    if not u:
        db.users.insert_one({"email": os.getenv("ADMIN_EMAIL"),
                             "password": bcrypt.hash(os.getenv("ADMIN_PASSWORD")),
                             "role":"admin"})
    return {"ok": True}

@router.post("/login")
def login(email:str, password:str):
    u = db.users.find_one({"email":email})
    if not u or not bcrypt.verify(password, u["password"]):
        raise HTTPException(401,"bad creds")
    return {"token": sign_jwt(email, u["role"])}
