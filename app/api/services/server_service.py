import datetime
from typing import List, Optional
from app.api.models.server_model import ServerModel
from app.api.repositories.server_repository import ServerRepository
from app.api.services.sensor_service import SensorService
from app.api.services.user_service import UserService
from app.schemas.server_dto import OutputRegisterDataDTO


class ServerService:

    async def valite_sensor(temperature: Optional[float], humidity: Optional[float], voltage: Optional[float], current: Optional[float]) -> bool:
        return any(
            value is not None
            for value in [temperature, humidity, voltage, current]
        )

    async def register_data(id:str) -> OutputRegisterDataDTO:
        server_ulid = await ServerService.get_server_id(id)
        timestamp = await ServerRepository.get_server_timestamp()


        temperature = await SensorService.get_temperature()
        humidity = await SensorService.get_humidity()
        voltage = await SensorService.get_voltage()
        current = await SensorService.get_current()
        
        if not await ServerService.valite_sensor(temperature, humidity, voltage, current):
        
            raise ValueError("At least one sensor value must be provided")
        
        sensors = [
            ("temperature", temperature),
            ("humidity", humidity),
            ("voltage", voltage),
            ("current", current)
        ]

        for sensor_type, value in sensors:
            if value is not None:
                await ServerRepository.save_sensor_data(
                    server_ulid=server_ulid,
                    sensor_type=sensor_type,
                    value=value,
                    timestamp=timestamp
                )

        
        sensor_data = OutputRegisterDataDTO(
            server_ulid=server_ulid,
            timestamp=timestamp,
            temperature=temperature,
            humidity=humidity,
            voltage=voltage,
            current=current
        )
        
        return sensor_data

    async def get_sensor_data():
        data = await ServerRepository()
        return data

    async def create_server(name:str, userId: str)-> ServerModel:
        user = await UserService.get_user_by_id(userId)
        server = await ServerRepository.create_server(name, user)
        return server
    
    async def server_time()-> datetime:
        timestamp = await ServerRepository.server_time()
        return timestamp
    
    async def list_server()-> List[ServerModel]:
        server = await ServerRepository.list_server()
        return server
    
    async def get_server_id(id:str) -> str:
        server_id = await ServerRepository.get_server_id(id)
        return server_id