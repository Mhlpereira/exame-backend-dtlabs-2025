import asyncio
from fastapi import HTTPException , Request
from tortoise import Tortoise
import ulid
from datetime import datetime
from typing import List
from app.api.models.server_model import ServerModel
from app.api.models.user_model import UserModel
from redis.asyncio import Redis
from app.api.core.redis import start_process_task

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
        
    async def save_sensor_data(server_ulid: str, sensor_type: str, value:float, server_time:datetime, redis: Redis) -> None:
        global process_task, process_event
        try:
            print("antes da conexão")
            connection = Tortoise.get_connection("default")
            if not connection:
                raise HTTPException(status_code=500, detail="Database connection not initialized")
            print("depois da conexão")
            print(server_ulid, sensor_type, value,server_time)
            server_time_dt = datetime.fromisoformat(server_time)
            await connection.execute_query('INSERT INTO sensor_data (server_ulid, sensor_type, value,server_time) VALUES ($1, $2, $3, $4)',[server_ulid, sensor_type, value, server_time_dt])
            print(connection)
            print("depois do save")

            
            await redis.lpush(
                "sensor_data_queue",
                f"{server_ulid}:{sensor_type}:{value}:{server_time_dt}"
            )
            start_process_task(redis)
            

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error saving data: {e}")
        

    
    async def create_server(name: str, user: UserModel) -> ServerModel:
        try:
            id = ulid.new()
            server = await ServerModel.create(id, name, user)
            return server
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error creating server")