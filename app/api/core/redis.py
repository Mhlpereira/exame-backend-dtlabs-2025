import typing
from redis.asyncio import Redis
from fastapi import FastAPI, Request
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis


async def connect_redis(app: FastAPI):
    app.state.redis = await Redis.from_url("redis://localhost:6379/0")
    try:
        await app.state.redis.ping()
        logger.info("Conexão com Redis está funcionando.")
    except Exception as e:
        logger.error(f"Erro ao conectar ao Redis: {e}")


async def disconnect_redis(app: FastAPI):
    if app.state.redis:
        await app.state.redis.close()


async def process_sensor_data(
    redis: Redis, stream_key: str, stop_events: asyncio.Event
):
    try:
        await redis.xgroup_create(stream_key, "sensor_workers", id="0", mkstream=True)
    except Exception as e:
        if "BUSYGROUP" not in str(e):
            raise e
    while not stop_events.is_set():
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
                    await saving_data(message_data)
                    await redis.xack(stream_key, "sensor_workers", message_id)


async def saving_data(message_data):
    server_ulid = message_data[b"server_ulid"].decode("utf-8")
    sensor_type = message_data[b"sensor_type"].decode("utf-8")
    value = message_data[b"value"].decode("utf-8")
    server_time = message_data[b"server_time"].decode("utf-8")

    from app.api.services.server_service import ServerService

    await ServerService.save_register_data(server_ulid, sensor_type, value, server_time)
