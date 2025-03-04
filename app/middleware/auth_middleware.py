import logging
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
import os

logger = logging.getLogger(__name__)
load_dotenv()


async def auth_middleware(request: Request, call_next):
    public_routes = [
        {"path": "/"},
        {"path": "/list-servers", "methods": ["GET"]},
        {"path": "/docs", "methods": ["GET"]},
        {"path": "/openapi.json", "methods": ["GET"]},
        {"path": "/auth/login", "methods": ["POST"]},
        {"path": "/auth/register", "methods": ["POST"]},
        {"path": "/data", "methods": ["POST"]},
        {"path": "/data/stop", "methods": ["POST"]},
        {"path": "/test-redis", "methods": "GET"},
    ]

    for route in public_routes:
        if request.url.path == route["path"] and request.method in route["methods"]:
            return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.error("Authorization header missing or invalid")
        raise HTTPException(status_code=401, detail="Invalid token")

    token = auth_header.split(" ")[1]

    secret_key = os.getenv("DT_SECRET")
    if not secret_key:
        logger.error("DT_SECRET is not set in environment variables")
        raise HTTPException(status_code=500, detail="Internal server error")

    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms="HS256",
        )
        request.state.user = payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=498, detail="Token has expired")
    except InvalidTokenError:
        logger.error("Invalid token")
        raise HTTPException(status_code=498, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error processing token: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing token: {str(e)}")

    return await call_next(request)
