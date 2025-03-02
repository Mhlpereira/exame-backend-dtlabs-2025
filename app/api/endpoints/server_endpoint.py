import datetime
from app.api.core.dependency import oauth2_scheme
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import JSONResponse
from datetime import datetime
from app.api.core.redis import get_redis_client
from app.api.services.server_service import ServerService
from app.middleware.frequency_rate_middleware import FrequencyRateMiddleware
from app.middleware.get_id import get_user_id
from app.schemas.server_dto import (
    CreateServerDTO,
    ListServerDTO,
    OutputCreateServerDTO,
    OutputRegisterDataDTO,
    OutputServerHealthDTO,
)


router = APIRouter(tags=["server"])


@router.post("/data")
async def register_data(
    server_ulid: str, redis=Depends(get_redis_client)
) -> OutputRegisterDataDTO:
    try:

        frequency_limiter = FrequencyRateMiddleware(redis, "sensor_data_queue")

        confirmed_id = await ServerService.get_server_id(server_ulid)

        if not confirmed_id:
            raise HTTPException(status_code=404, detail="Server not found!")

        data = await ServerService.register_data(confirmed_id, redis)
        await frequency_limiter.check_frequency()
        return JSONResponse(content=data.model_dump(), status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/data")
async def get_sensor_data(
    server_ulid: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    sensor_type: Optional[str] = Query(None),
    aggregation: Optional[str] = Query(None),
    token: str = Depends(oauth2_scheme),
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
    token: str = Depends(oauth2_scheme),
) -> OutputCreateServerDTO:

    server = await ServerService.create_server(body.name, user_id)

    output = OutputCreateServerDTO(server_name=server.name)

    return JSONResponse(content=output, status_code=201)


@router.get("/list-servers")
async def list_server() -> Response:

    servers = await ServerService.list_server()

    return JSONResponse(content=servers, status_code=200)


@router.get("/health/:server_id")
async def get_server_healt_by_id(
    server_id, token: str = Depends(oauth2_scheme)
) -> OutputServerHealthDTO:
    server_health = await ServerService.get_server_health_by_id(server_id)

    return JSONResponse(content=server_health, status_code=200)


@router.get("/health/all")
async def get_all_server_health(token: str = Depends(oauth2_scheme)):
    servers_health = await ServerService.get_all_server_health()
    return JSONResponse(content=servers_health, status_code=200)
