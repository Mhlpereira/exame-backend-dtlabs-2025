from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.services.server_service import ServerService
from app.middleware.frequency_rate_middleware import FrequencyRateMiddleware
from app.schemas.server_dto import CreateServerDTO, OutputCreateServerDTO, OutputRegisterDataDTO, PayloadDTO


router = APIRouter(tags=["server"])

frequency_limiter = FrequencyRateMiddleware()

@router.post("/data")
async def register_data(
    _=Depends(frequency_limiter)
    ) -> OutputRegisterDataDTO:
    id = await ServerService.get_payload_id()
    
    confirmed_id = await ServerService.get_server_id(id)
    
    if not confirmed_id:
        raise HTTPException(
            status_code=404,
            detail="Server not found!") 
    
    data = await ServerService.register_data(confirmed_id)
    
    return data

@router.post("/create-server")
async def create_server(body: CreateServerDTO, request: Request) -> OutputCreateServerDTO:
    id = request.state.user_id
    
    server = await ServerService.create_server(body.name , id)
    
    output = OutputCreateServerDTO(
        server_name=server.name
    )
    
    return server