from fastapi import APIRouter, FastAPI, Depends
import CreateUserDTO

class UserEndpoint():

    router = APIRouter(prefix="/user", tags="Users")

    @router.post("/user")
    async def create_user(data: CreateUserDTO):
        return