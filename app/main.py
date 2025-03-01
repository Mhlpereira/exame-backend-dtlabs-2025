from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.base  import BaseHTTPMiddleware
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
from app.api.core.redis import connect_redis, disconnect_redis
from app.middleware.auth_middleware import auth_middleware
from app.api.endpoints import auth_router , server_router
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_redis(app)
    yield
    await disconnect_redis(app)


app =  FastAPI(lifespan=lifespan)
load_dotenv("../.env")
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)


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

@app.get("/test-redis")
async def test_redis():
    redis = app.state.redis
    await redis.set("test_key", "test_value")
    value = await redis.get("test_key")
    return {"value": value}