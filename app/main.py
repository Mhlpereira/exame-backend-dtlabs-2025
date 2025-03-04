import asyncio
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, security
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
from app.api.core.redis import connect_redis, disconnect_redis, process_sensor_data
from app.middleware.auth_middleware import auth_middleware
from app.api.endpoints import auth_router, server_router
from app.config.db_config import db_config

process_task: Optional[asyncio.Task] = None
stop_event = asyncio.Event()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_redis(app)

    yield

    await disconnect_redis(app)


app = FastAPI(lifespan=lifespan)

load_dotenv("../.env")
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
app.security = [security]


register_tortoise(
    app,
    config=db_config,
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
