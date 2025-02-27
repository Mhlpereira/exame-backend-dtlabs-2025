from fastapi import APIRouter

from app.api.services.server_service import ServerService
from app.schemas.server_dto import OutputRegisterDataDTO, PayloadDTO


router = APIRouter(tags=["server"])


@router.get("/getPayload")
async def get_payload() -> PayloadDTO:
    
    data = await ServerService.get_payload()
    
    return data

@router.post("/data")
async def register_data(id: str) -> OutputRegisterDataDTO:
    data = await ServerService.register_data(id)
    
    return data