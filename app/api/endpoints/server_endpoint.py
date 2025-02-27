from fastapi import APIRouter

from app.api.services.server_service import ServerService
from app.schemas.server_dto import OutputRegisterDataDTO, PayloadDTO


router = APIRouter(tags=["server"])

@router.post("/data")
async def register_data() -> OutputRegisterDataDTO:
    id = await ServerService.get_payload_id()
    
    data = await ServerService.register_data(id)
    
    return data