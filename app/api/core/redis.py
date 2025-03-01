from redis.asyncio import Redis
from fastapi import FastAPI

async def get_redis_client() -> Redis:
    return Redis.from_url("redis://localhost:6379", db=0)

async def connect_redis(app: FastAPI):
    app.state.redis = await get_redis_client()

async def disconnect_redis(app: FastAPI):
    if app.state.redis:
        await app.state.redis.close()
