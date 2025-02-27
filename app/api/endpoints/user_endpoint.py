from fastapi import APIRouter, FastAPI, Depends
from app.api.services.user_service import UserService
from app.schemas.user_dto import CreateUserDTO, OutputUserDTO


router = APIRouter(prefix="/user", tags="Users")
