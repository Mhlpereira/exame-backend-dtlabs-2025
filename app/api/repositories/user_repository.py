from app.api.models.user_model import UserModel
from typing import Optional
import ulid

class UserRepository:

    async def create_user(email: str, hash_password: str) -> UserModel:
        id = ulid.new()
        user = await UserModel.create(id ,email=email, password=hash_password)
        return user
    
    async def get_user_by_email(email: str) -> Optional[UserModel]:
        user = await UserModel.get_or_none(email=email)
        if user:
            return user
        else:
            return None
