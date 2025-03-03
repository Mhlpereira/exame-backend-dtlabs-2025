from redis.asyncio import Redis
from fastapi import FastAPI, Request
import asyncio
import logging

from app.api.repositories.server_repository import ServerRepository


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

process_task = None
process_event = asyncio.Event()
INACTIVITY_TIMEOUT = 60


async def get_redis_client(request: Request) -> Redis:
    return request.app.state.redis


async def connect_redis(app: FastAPI):
    app.state.redis = Redis.from_url("redis://localhost:6379", db=0)


async def disconnect_redis(app: FastAPI):
    if app.state.redis:
        await app.state.redis.close()


async def process_queue(redis: Redis):
    global process_task, process_event
    queue_key = "sensor_data_queue"

    while not process_event.is_set():
        await asyncio.sleep(0.1)

        requests = await redis.lrange(queue_key, 0, -1)
        if requests:
            batch = []
            for request in requests:
                if isinstance(request, bytes):
                    request = request.decode("utf-8")
                    try:
                        server_ulid, sensor_type, value, server_time = request.split(
                            ":"
                        )
                        await ServerRepository.save_sensor_data(
                            server_ulid=server_ulid,
                            sensor_type=sensor_type,
                            value=value,
                            server_time=server_time,
                        )
                    except Exception as e:
                        logger.error(f"Error prossenig data in stream {request}: {e}")
                batch.append(request)
            await redis.delete(queue_key)
            logger.info("Queue cleared after processing.")
        try:
            await asyncio.wait_for(process_event.wait(), timeout=INACTIVITY_TIMEOUT)
        except asyncio.TimeoutError:
            logger.info("Inactivity, stopping the stream.")
            break


def start_process_task(redis: Redis):

    if process_task is None or process_task.done():
        process_event.clear()
        process_task = asyncio.create_task(process_queue(redis))


async def stop_process_task():

    if process_task and not process_task.done():
        process_event.set()
        await process_task
        process_task = None
        logger.info("Process task stopped.")
    else:
        logger.info("No process task running.")
