from fastapi import Request, HTTPException
from jwt import jwt, JWTError
import os


ALGORITHM = "HS256"

async def auth_middleware(request: Request, call_next):
    public_routes = [
        {"path": "/docs", "methods": ["GET"]},
        {"path": "/openapi.json", "methods": ["GET"]},
        {"path": "/auth/login", "methods": ["POST"]},
        {"path": "/auth/register", "methods": ["POST"]},
        {"path": "/data", "methods": ["POST"]}, 
    ]

    for route in public_routes:
        if request.url.path == route["path"] and request.method in route["methods"]:
            return await call_next(request)


    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, os.getenv('MY_SECRET'), algorithms=[ALGORITHM])
        request.state.user = payload 
    except JWTError:
        raise HTTPException(status_code=401, detail="Expired token")

    return await call_next(request)