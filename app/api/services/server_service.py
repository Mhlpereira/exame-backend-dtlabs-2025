import asyncio
import datetime
from typing import List, Optional

from fastapi import HTTPException

from app.api.core.redis import process_sensor_data
from app.api.models.server_model import ServerModel
from app.api.repositories.server_repository import ServerRepository
from app.api.services.sensor_service import SensorService
from app.api.services.user_service import UserService
from app.schemas.server_dto import (
    ListServerDTO,
    OutputRegisterDataDTO,
    OutputServerHealthDTO,
    SensorDataDTO,
)
from redis.asyncio import Redis
from datetime import datetime


class ServerService:

    process_task: Optional[asyncio.Task] = None
    stop_event: asyncio.Event = asyncio.Event()

    async def save_register_data(server_ulid, sensor_type, value, server_time):
        value_fmt = float(value)
        await ServerRepository.save_sensor_data(
            server_ulid=server_ulid,
            sensor_type=sensor_type,
            value=value_fmt,
            server_time=server_time,
        )

    async def valite_sensor(
        temperature: Optional[float],
        humidity: Optional[float],
        voltage: Optional[float],
        current: Optional[float],
    ) -> bool:
        return any(
            value is not None for value in [temperature, humidity, voltage, current]
        )

    async def register_sensor_data(
        id: str, redis: Redis, stream_key
    ) -> OutputRegisterDataDTO:
        server = await ServerService.get_server_by_id(id)

        data = await ServerService.generate_sensor_data(id)

        if not await ServerService.valite_sensor(
            data.temperature, data.humidity, data.voltage, data.current
        ):
            raise ValueError("At least one sensor value must be provided")

        sensors = [
            ("temperature", data.temperature),
            ("humidity", data.humidity),
            ("voltage", data.voltage),
            ("current", data.current),
        ]
        for sensor_type, value in sensors:
            if value is not None:
                message = {
                    "server_ulid": server.server_ulid,
                    "sensor_type": sensor_type,
                    "value": str(value),
                    "server_time": str(data.server_time),
                }
                await redis.xadd(stream_key, message)

        sensor_data = OutputRegisterDataDTO(
            server_ulid=server.server_ulid,
            timestamp=data.server_time,
            temperature=data.temperature,
            humidity=data.humidity,
            voltage=data.voltage,
            current=data.current,
        )

        return sensor_data

    async def generate_sensor_data(server_ulid: str) -> SensorDataDTO:
        server_time = datetime.now().isoformat()

        temperature = await SensorService.get_temperature()
        humidity = await SensorService.get_humidity()
        voltage = await SensorService.get_voltage()
        current = await SensorService.get_current()

        sensor_data = SensorDataDTO(
            server_time=server_time,
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

        result = await ServerRepository.query_data(
            server_ulid=server_ulid or None,
            start_time=start_time or None,
            end_time=end_time or None,
            sensor_type=sensor_type or None,
            aggregation=aggregation or None,
        )
        list = []

        for data in result:
            list.append(data)

        return list

    async def create_server(name: str, userId: str) -> ServerModel:
        if not name:
            raise HTTPException(status_code=400, detail="Invalid server name")
        user = await UserService.get_user_by_id(userId)
        server = await ServerRepository.create_server(name, user)
        return server

    async def server_time(server_ulid: str) -> datetime | None:
        timestamp = await ServerRepository.get_server_timestamp(server_ulid)
        print(timestamp, "server_time time")
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

    async def get_server_health_by_id(server_id: str) -> OutputServerHealthDTO:
        server = await ServerService.get_server_by_id(server_id)
        print("antes do last", server.server_ulid)
        last_online = await ServerService.server_time(server.server_ulid)
        status = ServerService.server_health(last_online)

        server_health = OutputServerHealthDTO(
            server_ulid=server.server_ulid,
            status=status,
            server_name=server.server_name,
        ).model_dump()
        return server_health

    def server_health(last_online: datetime) -> str:
        if last_online is None:
            return "offline"
        current_time = datetime.now()
        last_online_fmt = datetime.strptime(last_online, "%Y-%m-%d %H:%M:%S")
        print(current_time, "current")
        print(last_online_fmt, "last")
        time_diff = (current_time - last_online_fmt).total_seconds()
        print(time_diff)
        if time_diff > 10000:
            return "offline"
        else:
            return "online"

    async def get_all_server_health() -> List[OutputServerHealthDTO]:
        data = []
        server_list = await ServerService.list_server()

        for server in server_list:
            server_health = await ServerService.get_server_health_by_id(
                server["server_ulid"]
            )
            print(server_health, "all server health")
            data.append(
                OutputServerHealthDTO(
                    server_ulid=server_health["server_ulid"],
                    status=server_health["status"],
                    server_name=server_health["server_name"],
                ).model_dump()
            )

        return data
