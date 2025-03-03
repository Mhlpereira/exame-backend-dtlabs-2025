import os
from dotenv import load_dotenv
import jwt
from app.api.services.user_service import UserService
from app.schemas.user_dto import UserPayloadDTO

load_dotenv()


class AuthService:

    async def login(email: str, password: str) -> str:
        user = await UserService.verify_password(email, password)
        if user == None:
            raise Exception("Email or password incorrect")
        else:
            data_dict = UserPayloadDTO(sub=user.id, email=user.email).model_dump()
            token = jwt.encode(data_dict, key=os.getenv("DT_SECRET"), algorithm="HS256")
            return token
