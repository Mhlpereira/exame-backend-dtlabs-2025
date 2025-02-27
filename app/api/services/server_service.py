import datetime
from typing import Optional
from app.api.repositories.server_repository import ServerRepository
from app.api.services.sensor_service import SensorService
from app.schemas.server_dto import OutputRegisterDataDTO, PayloadDTO


class ServerService:

    async def valite_sensor(temperature: Optional[float], humidity: Optional[float], voltage: Optional[float], current: Optional[float]) -> bool:
        return any(
            value is not None
            for value in [temperature, humidity, voltage, current]
        )

    async def register_data(id:str) -> OutputRegisterDataDTO:
        server_ulid = await ServerService.get_payload_id()
        timestamp = await ServerService.get_timestamp()
        temperature = await SensorService.get_temperature()
        humidity = await SensorService.get_humidity()
        voltage = await SensorService.get_voltage()
        current = await SensorService.get_current()
        
        if not await ServerService.valite_sensor(temperature, humidity, voltage, current):
        
            raise ValueError("At least one sensor value must be provided")
        
        
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
    
    async def get_payload_id()-> str:
        payload_id = await ServerRepository.get_payload_id()
        return payload_id
    
    async def get_server_id(id:str) -> str:
        server_id = await ServerRepository.get_server_id(id)
        return server_id