from fastapi import APIRouter, Depends
from services.mongo import db
from services.qdrant_client import client, COL
from services.ai import embed_text
from security import require_role

router = APIRouter()

@router.get("/text", dependencies=[Depends(require_role(["admin","analyst","viewer"]))])
def text_search(q:str, k:int=10):
    cur = db.iocs.find({"value":{"$regex":q,"$options":"i"}})
    return [ {"type":d["type"],"value":d["value"],"tags":d.get("tags",[])} for d in cur.limit(k) ]

@router.get("/semantic", dependencies=[Depends(require_role(["admin","analyst","viewer"]))])
def semantic_search(query:str, k:int=10):
    vec = embed_text(query)
    hits = client.search(COL, query_vector=vec, limit=k)
    ids = [h.id for h in hits]
    match = [{"value": i.split(":",1)[1], "type": i.split(":",1)[0]} for i in ids]
    ors = [{"type":m["type"],"value":m["value"]} for m in match]
    docs = list(db.iocs.find({"$or": ors})) if ors else []
    return [{"type":d["type"],"value":d["value"],"tags":d.get("tags",[])} for d in docs]
