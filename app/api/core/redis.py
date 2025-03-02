import datetime
from redis.asyncio import Redis
from fastapi import FastAPI, Request
import asyncio
import logging


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
        await asyncio.sleep(1)
        requests = await redis.lrange(queue_key, 0, -1)
        if requests:
            batch = []
            for request in requests:
                if isinstance(request, bytes):
                    request = request.decode("utf-8")  
                logger.info(server_ulid, sensor_type, value, server_time )


                server_ulid, sensor_type, value, server_time = request.split(" ")
                server_time = datetime.fromisoformat(server_time)
                value = float(value)
                batch.append({
                    "server_ulid": server_ulid,
                    "sensor_type": sensor_type,
                    "value": value,
                    "server_time": server_time
                })
            print(f"Processing requisition: server_ulid={server_ulid}, sensor_type={sensor_type}, value={value}, server_time={server_time}")
            await redis.delete(queue_key)
        try:
            await asyncio.wait_for(process_event.wait(), timeout=INACTIVITY_TIMEOUT)
        except asyncio.TimeoutError:
            logger.info("Nenhuma requisição recebida. Parando o processamento da fila.")
            break  

def start_process_task(redis: Redis):
    global process_task, process_event

    if process_task is None or process_task.done():
        process_event.clear()  
        process_task = asyncio.create_task(process_queue(redis))
        logger.info("Tarefa de processamento iniciada.") 