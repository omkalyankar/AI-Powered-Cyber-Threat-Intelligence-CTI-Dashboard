import os, time
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

JWT_SECRET = os.getenv("JWT_SECRET","dev")
ALGO="HS256"
auth_scheme = HTTPBearer()

def sign_jwt(sub:str, role:str):
    return jwt.encode({"sub":sub,"role":role,"iat":int(time.time())}, JWT_SECRET, algorithm=ALGO)

def require_role(roles: list[str]):
    def dep(creds: HTTPAuthorizationCredentials = Depends(auth_scheme)):
        try:
            data = jwt.decode(creds.credentials, JWT_SECRET, algorithms=[ALGO])
            if data.get("role") not in roles:
                raise HTTPException(403, "insufficient role")
            return data
        except Exception:
            raise HTTPException(401, "invalid token")
    return dep

def add_security_headers(resp):
    resp.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
