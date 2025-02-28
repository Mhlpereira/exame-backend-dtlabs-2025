from fastapi import HTTPException, Request
from fastapi.middleware import BaseHTTPMiddleware
import os
import jwt

class IdMiddleware(BaseHTTPMiddleware):
    async def request_header(self, request: Request, callnext):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPException(
                status_code=401,
                detail="Authorization missing or invalid!"
            )
    
        token = auth_header.split(" ")[1]
        
        try:
            payload = jwt.decode(token, os.getenv("MY_SECRET"), algorithms = [os.getenv("ALGORITHM")])
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token: subject not found!"
                )
            request.state.user_id = user_id
        except jwt.PyJWTError as e:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
            
        response = await call_next(request)
        return response