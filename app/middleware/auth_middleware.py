from fastapi import Request, HTTPException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
import os

ALGORITHM = "HS256"

async def auth_middleware(request: Request, call_next):
    public_routes = [
        {"path": "/"},
        {"path": "/list-servers", "methods": ["GET"]},
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
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing token: {str(e)}")

    return await call_next(request)