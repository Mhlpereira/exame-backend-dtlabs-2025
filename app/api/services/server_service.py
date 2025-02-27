import datetime
from app.api.repositories.server_repository import ServerRepository
from app.api.services.sensor_service import SensorService
from app.schemas.server_dto import OutputRegisterDataDTO, PayloadDTO


class ServerService:

    async def register_data(id:str) -> OutputRegisterDataDTO:
        server_ulid = await ServerRepository.get_server_id(id)
        timestamp = await SensorService.get_server_date()
        temperature = await SensorService.get_temperature()
        humidity = await SensorService.get_humidity()
        voltage = await SensorService.get_voltage()
        current = await SensorService.get_current()

        sensor_data = OutputRegisterDataDTO(
            server_ulid=server_ulid,
            timestamp=timestamp,
            temperature=temperature,
            humidity=humidity,
            voltage=voltage,
            current=current
        )
        
        return sensor_data

    async def get_timestamp()-> datetime:
        timestamp = await ServerRepository.get_server_date()
        return timestamp
    
    async def get_payload() -> PayloadDTO:
        payloadId = await ServerRepository.get_server_id