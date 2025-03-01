from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.api.services.auth_service import AuthService
from app.api.services.user_service import UserService
from app.schemas.login_dto import LoginDTO, TokenDTO
from app.schemas.user_dto import CreateUserDTO, OutputUserDTO


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def create_user(data: CreateUserDTO) -> OutputUserDTO:
    user = await UserService.create_user(data.email, data.password)

    data = OutputUserDTO(email=user.email)
    return JSONResponse(content=data, status_code=201)


@router.post("/login")
async def login(data: LoginDTO) -> TokenDTO:
    token = await AuthService.authenticate(data.email, data.password)
    data = TokenDTO(access_token=token, token_type="bearer")
    return JSONResponse(content=data, status_code=200)
