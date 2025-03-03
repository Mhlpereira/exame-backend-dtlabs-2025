import asyncio
import datetime

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse
from datetime import datetime


from app.api.core.redis import get_redis_client, process_sensor_data
from app.api.services.server_service import ServerService
from app.middleware.frequency_rate_middleware import FrequencyRateMiddleware
from app.middleware.get_id import get_user_id
from app.schemas.server_dto import (
    CreateServerDTO,
    OutputCreateServerDTO,
    OutputRegisterDataDTO,
    OutputServerHealthDTO,
)


router = APIRouter(tags=["server"])
stop_event = asyncio.Event()


@router.post("/data")
async def register_data(
    server_ulid: str, redis=Depends(get_redis_client)
) -> OutputRegisterDataDTO:
    global process_task
    try:
        confirmed_server = await ServerService.get_server_by_id(server_ulid)

        if not confirmed_server:
            raise HTTPException(status_code=404, detail="Server not found!")

        if process_task and not process_task.done():
            raise HTTPException(status_code=400, detail="Server already on!")
        stop_event.clear()
        process_task = asyncio.create_task(process_sensor_data(redis, stop_event))
        data = await ServerService.register_sensor_data(server_ulid, redis)
        return JSONResponse(content=data.model_dump(), status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/data/stop")
async def server_stop(server_ulid: str):
    if not process_task or process_task.done():
        raise HTTPException(status_code=400, detail="Stream não está em execução.")
    stop_event.set()
    await process_task
    server = await ServerService.get_server_by_id(server_ulid)
    return {f"stoping server {server.server_name}"}


@router.get("/data")
async def get_sensor_data(
    server_ulid: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    sensor_type: Optional[str] = Query(None),
    aggregation: Optional[str] = Query(None),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):

    data = await ServerService(
        server_ulid=server_ulid,
        start_time=start_time,
        end_time=end_time,
        sensor_type=sensor_type,
        aggregation=aggregation,
    )
    return JSONResponse(content=data, status_code=200)


@router.post("/create-server")
async def create_server(
    body: CreateServerDTO,
    user_id: str = Depends(get_user_id),
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> OutputCreateServerDTO:

    server = await ServerService.create_server(body.name, user_id)

    output = OutputCreateServerDTO(server_name=server.server_name).model_dump()

    return JSONResponse(content=output, status_code=201)


@router.get("/list-servers")
async def list_server() -> Response:

    servers = await ServerService.list_server()

    return JSONResponse(content=servers, status_code=200)


@router.get("/health/:server_id")
async def get_server_healt_by_id(
    server_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> OutputServerHealthDTO:
    server_health = await ServerService.get_server_healht_by_id(server_id)

    return JSONResponse(content=server_health, status_code=200)


@router.get("/health/all")
async def get_all_server_health(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    servers_health = await ServerService.get_all_server_health()
    return JSONResponse(content=servers_health, status_code=200)
