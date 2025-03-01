from fastapi import HTTPException , Request
from tortoise import Tortoise
import ulid
from datetime import datetime
from typing import List
from tortoise.exceptions import DoesNotExist
from app.api.models.server_model import ServerModel
from app.api.models.user_model import UserModel


class ServerRepository:
    
    async def get_server_id(id: str) -> str:
        try:
            server = await ServerModel.get(server_ulid=id)
            return server.server_ulid
        except DoesNotExist:
            raise DoesNotExist(status_code=404, detail="User not found")
        
    async def get_server_timestamp() -> datetime:
        timestamp = datetime.now().isoformat()
        
        return timestamp
    
    async def list_server() -> List[ServerModel]:
        try:
            server = await ServerModel.all()
            return server
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error listing servers")   
        
    async def save_sensor_data(server_ulid: str, sensor_type: str, value:float, timestamp:datetime) -> None:
        try:
            print("antes da conexão")
            connection = Tortoise.get_connection("default")
            if not connection:
                raise HTTPException(status_code=500, detail="Database connection not initialized")
            print("depois da conexão")
            print(server_ulid, sensor_type, value,timestamp)

            await connection.execute_query_dict("INSERT INTO sensor_data (server_ulid, sensor_type, value,timestamp) VALUES ($1, $2, $3, $4)",[server_ulid, sensor_type, value,timestamp])
            print(connection)
            print("depois do save")
            redis = Request.app.state.redis
            await redis.rpush(
                "sensor_data_querue",
                f"{server_ulid}:{sensor_type}:{value}:{timestamp.isoformat()}"
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Error saving data")
        

    
    async def create_server(name: str, user: UserModel) -> ServerModel:
        try:
            id = ulid.new()
            server = await ServerModel.create(id, name, user)
            return server
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error creating server")