
import datetime
from typing import Optional
from tortoise.exceptions import DoesNotExist
from app.api.models.server_model import ServerModel


class ServerRepository:
    
    async def get_server_id(id: str) -> Optional[str]:
        try:
            server = await ServerModel.get(id=id)
            return server.id
        except DoesNotExist:
            return None
        
    async def get_server_date() -> datetime:
        timestamp = datetime.now().isoformat()
        
        return timestamp
    
    async def get_payload_id() -> str:
        try:
            server = await ServerModel.all().first()
            return server.id
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado: {e}")