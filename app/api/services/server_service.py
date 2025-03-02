import datetime
from typing import List, Optional

from fastapi import HTTPException
from app.api.endpoints.server_endpoint import list_server
from app.api.models.server_model import ServerModel
from app.api.repositories.server_repository import ServerRepository
from app.api.services.sensor_service import SensorService
from app.api.services.user_service import UserService
from app.schemas.server_dto import (
    ListServerDTO,
    OutputRegisterDataDTO,
    OutputServerHealthDTO,
)
from redis.asyncio import Redis
from app.api.core.redis import start_process_task
from datetime import datetime


class ServerService:

    async def valite_sensor(
        temperature: Optional[float],
        humidity: Optional[float],
        voltage: Optional[float],
        current: Optional[float],
    ) -> bool:
        return any(
            value is not None for value in [temperature, humidity, voltage, current]
        )

    async def register_data(id: str, redis: Redis) -> OutputRegisterDataDTO:
        server_ulid = await ServerService.get_server_id(id)
        server_time = datetime.datetime.now()

        temperature = await SensorService.get_temperature()
        humidity = await SensorService.get_humidity()
        voltage = await SensorService.get_voltage()
        current = await SensorService.get_current()

        if not await ServerService.valite_sensor(
            temperature, humidity, voltage, current
        ):

            raise ValueError("At least one sensor value must be provided")

        sensors = [
            ("temperature", temperature),
            ("humidity", humidity),
            ("voltage", voltage),
            ("current", current),
        ]
        start_process_task(redis)
        for sensor_type, value in sensors:
            if value is not None:
                await redis.lpush(
                    "sensor_data_queue",
                    f"{server_ulid}:{sensor_type}:{value}:{server_time}",
                )

        sensor_data = OutputRegisterDataDTO(
            server_ulid=server_ulid,
            timestamp=server_time,
            temperature=temperature,
            humidity=humidity,
            voltage=voltage,
            current=current,
        )

        return sensor_data

    async def get_sensor_data(
        server_ulid: Optional[str],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        sensor_type: Optional[str],
        aggregation: Optional[str],
    ):

        data = await ServerRepository(
            server_ulid=server_ulid,
            start_time=start_time,
            end_time=end_time,
            sensor_type=sensor_type,
            aggregation=aggregation,
        )
        return data

    async def create_server(name: str, userId: str) -> ServerModel:
        user = await UserService.get_user_by_id(userId)
        server = await ServerRepository.create_server(name, user)
        return server

    async def server_time(server_ulid: str) -> datetime:
        timestamp = await ServerRepository.get_server_timestamp(server_ulid)
        return timestamp

    async def list_server() -> List[ListServerDTO]:
        servers_list = await ServerRepository.list_server()
        data = [
            ListServerDTO(
                name=server.server_name, server_ulid=server.server_ulid
            ).model_dump()
            for server in servers_list
        ]
        return data

    async def get_server_by_id(id: str) -> ServerModel:
        server = await ServerRepository.get_server_by_id(id)
        return server

    async def get_server_healt_by_id(server_id: str) -> OutputServerHealthDTO:
        server = await ServerService.get_server_by_id(server_id)

        last_online = await ServerService.server_time(server.ulid)
        status = ServerService.server_health(last_online)
        print(f"status no get_server_healt_by_id{status}")

        server_health = OutputServerHealthDTO(
            server_ulid=server.ulid, status=status, server_name=server.name
        )
        return server_health

    def server_health(last_online: datetime) -> str:
        current_time = datetime.datetime.now().isoformat()
        time_diff = (current_time - last_online).total_seconds()
        if time_diff > 10:
            return "offline"
        else:
            return "online"

    async def get_all_server_health() -> List[OutputServerHealthDTO]:

        server_list = await ServerService.list_server()

        for server in server_list:
            server_health = await ServerService.get_server_healt_by_id(
                server.server_ulid
            )
            data = [
                OutputServerHealthDTO(
                    server_ulid=server_health.ulid,
                    status=server_health.status,
                    server_name=server_health.name,
                ).model_dump()
            ]

        return data
