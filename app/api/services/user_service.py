from app.api.repositories.user_repository import UserRepository
from app.schemas.user_dto import CreateUserDTO
from app.api.models.user_model import UserModel
import bcrypt

class UserService:


    def hash_password(password: str) -> str:
        salt= bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    async def create_user(data: CreateUserDTO) -> UserModel:
        hashed_password = UserService.hash_password(data.password)
        confirm = UserService.verify_password(data.password, hashed_password)
        if confirm == False:
            raise Exception("Error encrypting password")
        else:
            user = UserRepository.create_user(data.email, hashed_password)
        return user
