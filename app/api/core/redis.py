from redis import ConnectionPool
from redis.asyncio import Redis
from fastapi import FastAPI, Request
import asyncio
import logging

from app.api.services.server_service import ServerService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

process_task = None
process_event = asyncio.Event()


async def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis


async def connect_redis(app: FastAPI):
    pool = ConnectionPool.from_url("redis://localhost:6379", db=0)
    app.state.redis = Redis(connection_pool=pool)
    try:
        await app.state.redis.ping()
        logger.info("Conexão com Redis está funcionando.")
    except Exception as e:
        logger.error(f"Erro ao conectar ao Redis: {e}")


async def disconnect_redis(app: FastAPI):
    if app.state.redis:
        await app.state.redis.close()


async def process_sensor_data(redis: Redis, stream_key: str, stop_event: asyncio.Event):

    while not stop_event.is_set():
        messages = await redis.xreadgroup(
            "sensor_workers",
            "worker_1",
            {stream_key: ">"},
            count=10,
            block=1000,
        )

        if messages:
            for stream, message_list in messages:
                for message_id, message_data in message_list:
                    print(f"Processing message {message_id}: {message_data}")
                    await saving_data(message_data)
                    await redis.xack(stream_key, "sensor_workers", message_id)


async def saving_data(message_data):
    server_ulid = message_data["server_ulid"]
    sensor_type = message_data["sensor_type"]
    value = float(message_data["value"])
    server_time = message_data["server_time"]

    await ServerService.save_register_data(server_ulid, sensor_type, value, server_time)
