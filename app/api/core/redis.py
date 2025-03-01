import aioredis
from fastapi import FastAPI

async def get_redis_client() -> aioredis.Redis:
    redis_client = aioredis.from_url("redis://redis:6379", db=0)
    return redis_client

async def connect_redis(app: FastAPI):
    app.state.redis = await get_redis_client()

async def disconnect_redis(app: FastAPI):
    await app.state.redis.close()