from fastapi import APIRouter, Depends

from app.api.services.server_service import ServerService
from app.middleware.frequency_rate_middleware import FrequencyRateMiddleware
from app.schemas.server_dto import OutputRegisterDataDTO, PayloadDTO


router = APIRouter(tags=["server"])

frequency_limiter = FrequencyRateMiddleware()

@router.post("/data")
async def register_data(
    _=Depends(frequency_limiter)
    ) -> OutputRegisterDataDTO:
    id = await ServerService.get_payload_id()
    
    confirmed_id = await ServerService.get_server_id(id)
    
    data = await ServerService.register_data(confirmed_id)
    
    return data