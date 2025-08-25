from fastapi import APIRouter, HTTPException, Depends
from services.mongo import db
from services.qdrant_client import client, COL
from services.ai import embed_text, explain_ioc
from security import require_role

router = APIRouter()

@router.post("/upsert", dependencies=[Depends(require_role(["admin","analyst"]))])
def upsert_ioc(doc: dict):
    if not {"type","value"} <= set(doc): 
        raise HTTPException(400,"missing fields")
    doc.setdefault("tags", [])
    db.iocs.update_one({"type":doc["type"],"value":doc["value"]}, {"$set":doc}, upsert=True)
    vec = embed_text(doc.get("context","") + " " + doc.get("value",""))
    client.upsert(COL, points=[{"id": f'{doc["type"]}:{doc["value"]}', "vector": vec}])
    db.audit.insert_one({"act":"upsert_ioc","who":"api","doc":doc})
    return {"ok": True}

@router.get("/explain", dependencies=[Depends(require_role(["admin","analyst","viewer"]))])
def explain(value:str, type:str="ip"):
    doc = db.iocs.find_one({"type":type,"value":value})
    if not doc: 
        raise HTTPException(404,"not found")
    return {"explanation": explain_ioc(doc)}
