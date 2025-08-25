from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from security import add_security_headers
from routers import auth, iocs, search, events

app = FastAPI(title="AI CTI Dashboard", version="0.1.0")

# Allow frontend (later React UI) to talk to API
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Secure session cookie
app.add_middleware(SessionMiddleware, secret_key="session-only", https_only=False)

@app.middleware("http")
async def sec_headers(request, call_next):
    resp = await call_next(request)
    add_security_headers(resp)
    return resp

# Routers (we’ll create these next)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(iocs.router, prefix="/iocs", tags=["iocs"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(events.router, prefix="/events", tags=["events"])

@app.get("/health")
def health(): 
    return {"ok": True}
