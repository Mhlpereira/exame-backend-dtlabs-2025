from app.api.repositories.user_repository import UserRepository
from app.schemas.user_dto import CreateUserDTO
from app.api.models.user_model import UserModel
import bcrypt


class UserService:

    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def confirm_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    async def create_user(email: str, password: str) -> UserModel:
        hashed_password = UserService.hash_password(password)
        confirm = UserService.confirm_password(password, hashed_password)
        if confirm == False:
            raise Exception("Error encrypting password")
        else:
            user = await UserRepository.create_user(email, hashed_password)
            print(user)
        return user

    async def verify_password(email: str, password: str) -> UserModel:
        user = await UserRepository.get_user_by_email(email)
        confirm_password = await UserService.confirm_password(password, user.password)
        if confirm_password == True:
            return user
        else:
            raise Exception("Email or password incorrect")

    async def get_user_by_id(id: str) -> UserModel:
        user = await UserRepository.get_user_by_id(id)
        return user
