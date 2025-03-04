import asyncio
import datetime

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse
from datetime import datetime

from app.api.core.redis import process_sensor_data
from app.api.services.server_service import ServerService
from app.middleware.get_id import get_user_id
from app.schemas.server_dto import (
    CreateServerDTO,
    OutputCreateServerDTO,
    OutputRegisterDataDTO,
    OutputServerHealthDTO,
)


router = APIRouter(tags=["server"])


stop_event = asyncio.Event()
process_task: Optional[asyncio.Task] = None


@router.post("/data")
async def register_data(server_ulid: str, request: Request) -> OutputRegisterDataDTO:
    redis = request.app.state.redis
    global process_task

    try:
        server = await ServerService.get_server_by_id(server_ulid)

        stream_key = "sensor_data_stream"
        process_task = asyncio.create_task(
            process_sensor_data(redis, stream_key, stop_event)
        )
        if not server:
            raise HTTPException(status_code=404, detail="Server not found!")

        data = await ServerService.register_sensor_data(server_ulid, redis, stream_key)
        return JSONResponse(content=data.model_dump(), status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/data/stop")
async def server_stop():
    stop_event.set()
    if process_task:
        await process_task


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
    server_health = await ServerService.get_server_health_by_id(server_id)

    return JSONResponse(content=server_health, status_code=200)


@router.get("/health/all")
async def get_all_server_health(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    servers_health = await ServerService.get_all_server_health()
    return JSONResponse(content=servers_health, status_code=200)
