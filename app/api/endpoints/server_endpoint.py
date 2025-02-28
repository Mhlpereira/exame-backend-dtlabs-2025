from fastapi import APIRouter

from app.api.services.server_service import ServerService
from app.schemas.server_dto import OutputRegisterDataDTO, PayloadDTO


router = APIRouter(tags=["server"])

@router.post("/data")
async def register_data() -> OutputRegisterDataDTO:
    id = await ServerService.get_payload_id()
    
    confirmed_id = await ServerService.get_server_id(id)
    
    data = await ServerService.register_data(confirmed_id)
    
    return data