from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse

from app.api.services.server_service import ServerService
from app.middleware.frequency_rate_middleware import FrequencyRateMiddleware
from app.middleware.get_id import get_user_id
from app.schemas.server_dto import CreateServerDTO, ListServerDTO, OutputCreateServerDTO, OutputRegisterDataDTO, PayloadDTO


router = APIRouter(tags=["server"])

frequency_limiter = FrequencyRateMiddleware()

@router.post("/data")
async def register_data(server_ulid: str) -> OutputRegisterDataDTO:
    try:
        frequency_limiter.check_rate(server_ulid)


        confirmed_id = await ServerService.get_server_id(server_ulid)
        
        if not confirmed_id:
            raise HTTPException(
                status_code=404,
                detail="Server not found!") 
        
        data = await ServerService.register_data(confirmed_id)
        
        return JSONResponse(content=data, status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/data")
async def get_sensor_data():
    data = await ServerService.get_sensor_data()
    return JSONResponse(content=data, status_code=200)

@router.post("/create-server")
async def create_server(body: CreateServerDTO, user_id: str = Depends(get_user_id)) -> OutputCreateServerDTO:
        
    server = await ServerService.create_server(body.name , user_id)
    
    output = OutputCreateServerDTO(
        server_name=server.name
    )
    
    return JSONResponse(content=output, status_code=201)

@router.get("/list-servers")
async def list_server() -> Response:
    
    servers_list = await ServerService.list_server()
    data = [ListServerDTO(name=server.server_name, server_ulid=server.server_ulid).model_dump() for server in servers_list]
    return JSONResponse(content=data, status_code=200)