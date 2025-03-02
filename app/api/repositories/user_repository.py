from fastapi import HTTPException
from app.api.models.user_model import UserModel
from typing import Optional
from ulid import ULID


class UserRepository:

    async def create_user(email: str, hash_password: str) -> UserModel:
        id = str(ULID())
        try:
            user = await UserModel.create(id, email=email, password=hash_password)
            return user
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error creating user: {e}")

    async def get_user_by_email(email: str) -> Optional[UserModel]:
        try:
            user = await UserModel.get_or_none(email=email)
            return user
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail="An error occurred while fetching the user by email.",
            )

    async def get_user_by_id(id: str) -> UserModel:
        try:
            user = await UserModel.get_or_none(id=id)
            if user:
                return user
        except HTTPException:
            raise HTTPException(
                status_code=404,
                detail="User not found.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while fetching the user by ID. {e}",
            )
