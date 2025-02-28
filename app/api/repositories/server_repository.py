from fastapi import HTTPException
import ulid
from datetime import datetime
from typing import List, Optional
from tortoise.exceptions import DoesNotExist
from app.api.models.request_model import ServerTimeModel
from app.api.models.server_model import ServerModel
from app.api.models.user_model import UserModel


class ServerRepository:
    
    async def get_server_id(id: str) -> Optional[str]:
        try:
            server = await ServerModel.get(server_ulid=id)
            return server.server_ulid
        except DoesNotExist:
            return None
        
    async def get_server_timestamp() -> datetime:
        timestamp = datetime.now().isoformat()
        
        return timestamp
    
    async def list_server() -> List[ServerModel]:
        try:
            server = await ServerModel.all()
            return server
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado: {e}")
    
    async def create_server(name: str, user: UserModel) -> ServerModel:
        try:
            id = ulid.new()
            server = await ServerModel.create(id, name, user)
            return server
        except Exception as e:
            print(f"Error creating server: {e}")
            raise HTTPException(status_code=500, detail="Error creating server")
        
    # async def server_time(server_ulid:str):
    #     try:
    #         timestamp = datetime.now().isoformat()
    #         await ServerTimeModel(server_ulid, timestamp).save()
    #         return timestamp
    #     except Exception as e:
    #         print(f"Error creating server: {e}")
    #         raise HTTPException(status_code=500, detail="Error creating server")