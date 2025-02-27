from fastapi import APIRouter, FastAPI, Depends
from app.api.services.user_service import UserService
from app.schemas.user_dto import CreateUserDTO, OutputUserDTO

class UserEndpoint():

    router = APIRouter(prefix="/user", tags="Users")

    @router.post("/create")
    async def create_user(data: CreateUserDTO) -> OutputUserDTO:
        user = await UserService.create_user(data.email, data.password)

        return OutputUserDTO(email=user.email)