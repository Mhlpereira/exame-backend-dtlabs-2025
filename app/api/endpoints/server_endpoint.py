from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.api.services.server_service import ServerService
from app.middleware.frequency_rate_middleware import FrequencyRateMiddleware
from app.middleware.get_id import get_user_id
from app.schemas.server_dto import CreateServerDTO, ListServerDTO, OutputCreateServerDTO, OutputRegisterDataDTO, PayloadDTO


router = APIRouter(tags=["server"])

frequency_limiter = FrequencyRateMiddleware()

@router.post("/data")
async def register_data(server_ulid: str) -> OutputRegisterDataDTO:

    frequency_limiter.check_rate(server_ulid)


    confirmed_id = await ServerService.get_server_id(server_ulid)
    
    if not confirmed_id:
        raise HTTPException(
            status_code=404,
            detail="Server not found!") 
    
    data = await ServerService.register_data(confirmed_id)
    
    return data

@router.post("/create-server")
async def create_server(body: CreateServerDTO, user_id: str = Depends(get_user_id)) -> OutputCreateServerDTO:
        
    server = await ServerService.create_server(body.name , user_id)
    
    output = OutputCreateServerDTO(
        server_name=server.name
    )
    
    return output

@router.get("/list-servers")
async def list_server() -> List[ListServerDTO]:
    
    servers_list = await ServerService.list_server()
    return [ListServerDTO(name=server.server_name, server_ulid=server.server_ulid) for server in servers_list]