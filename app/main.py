from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.base  import BaseHTTPMiddleware
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
from app.middleware.auth_middleware import auth_middleware
from app.middleware.frequency_rate_middleware import FrequencyRateMiddleware
from app.api.endpoints import auth_router , server_router

import os

from app.middleware.get_id_middleware import IdMiddleware





app =  FastAPI()
load_dotenv("../.env")
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
app.add_middleware(IdMiddleware)


register_tortoise(
    app,
    db_url=f"postgres://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@localhost:5432/{os.getenv('PG_DB')}",
    modules={"models": ["app.api.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(auth_router)
app.include_router(server_router)

@app.get("/")
async def hellow():
    print("Hellow")