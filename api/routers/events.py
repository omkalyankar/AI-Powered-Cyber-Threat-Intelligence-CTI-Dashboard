from fastapi import APIRouter, Depends
from services.mongo import db
from security import require_role

router = APIRouter()

@router.post("/ingest", dependencies=[Depends(require_role(["admin","sensor"]))])
def ingest(evt: dict):
    db.events.insert_one(evt)
    return {"ok": True}
