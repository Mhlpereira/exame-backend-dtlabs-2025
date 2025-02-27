from fastapi import APIRouter
from app.api.services.auth_service import AuthService
from app.api.services.user_service import UserService
from app.schemas.login_dto import LoginDTO, TokenDTO
from app.schemas.user_dto import CreateUserDTO, OutputUserDTO

class AuthEndpoint:

    router = APIRouter(prefix="/auth", tags="Auth")

    @router.post("/register")
    async def create_user(data: CreateUserDTO) -> OutputUserDTO:
        user = await UserService.create_user(data.email, data.password)

        return OutputUserDTO(email=user.email)
    
    @router.post("/login")
    async def login(data: LoginDTO) -> TokenDTO:
        token = await AuthService.authenticate(data.email, data.password)
        return TokenDTO(token=token, token_type="bearer")

