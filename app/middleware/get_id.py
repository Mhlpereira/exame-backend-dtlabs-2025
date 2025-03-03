from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request
import jwt
import os

load_dotenv()


async def get_user_id(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization missing or invalid!")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, os.getenv("DT_SECRET"), algorithms="HS256")
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401, detail="Invalid token: subject not found!"
            )

        return user_id

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
