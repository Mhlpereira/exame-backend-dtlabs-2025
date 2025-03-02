from fastapi import HTTPException
from tortoise import Tortoise
import ulid
from datetime import datetime
from typing import List, Optional
from app.api.models.server_model import ServerModel
from app.api.models.user_model import UserModel


class ServerRepository:

    async def get_server_id(id: str) -> str:
        try:
            server = await ServerModel.get(server_ulid=id)
            return server.server_ulid
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"User not found{e}")

    async def get_server_timestamp() -> datetime:
        timestamp = datetime.now().isoformat()

        return timestamp

    async def list_server() -> List[ServerModel]:
        try:
            server = await ServerModel.all()
            return server
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error listing servers{e}")

    async def save_sensor_data(
        server_ulid: str, sensor_type: str, value: float, server_time: datetime
    ) -> None:
        global process_task, process_event
        try:
            connection = Tortoise.get_connection("default")
            if not connection:
                raise HTTPException(
                    status_code=500, detail="Database connection not initialized"
                )
            timestamp = datetime.fromisoformat(server_time)
            print(server_ulid, sensor_type, value, timestamp)
            await connection.execute_query(
                "INSERT INTO sensor_data (server_ulid, sensor_type, value,timestamp) VALUES ($1, $2, $3, $4)",
                [server_ulid, sensor_type, value, timestamp],
            )

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error saving data: {e}")

    async def create_server(name: str, user: UserModel) -> ServerModel:
        try:
            id = str(ulid.new())
            server = await ServerModel.create(id=id, name=name, user=user)
            return server
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating server: {e}")

    async def query_data(
        server_ulid: Optional[str],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        sensor_type: Optional[str],
        aggregation: Optional[str],
    ):
        connection = Tortoise.get_connection("default")
        try:
            filters = []
            if server_ulid:
                filters.append(f"server_ulid = '{server_ulid}")
            if start_time and end_time:
                filters.append(f"timestamp BETWEEN '{start_time}' AND '{end_time}")
            if sensor_type:
                filters.append(f"sensor_type = '{sensor_type}'")
            query = "SELECT server_time , sensor_type , value FROM sensor_data"
            if filters:
                query += " WHERE " + " AND ".join(filters)
            if aggregation:
                if aggregation not in ["minute", "hour", "day"]:
                    raise HTTPException(
                        status_code=400, detail="Invalid aggregation value"
                    )

                interval = f"1 {aggregation}"
                query = f"""
                    SELECT time_bucket('{interval}'),server_time) AS bucket,
                            sensor_type,
                            AVG(value) AS avg_value
                    FROM sensor_data
                    {"WHERE " + " AND ".join(filters) if filters else ""}
                    GROUP BY bucket, sensor_type
                    ORBER BY bucket
                """
            results = await connection.execute_query(query)
            return results
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching data: {e}")
