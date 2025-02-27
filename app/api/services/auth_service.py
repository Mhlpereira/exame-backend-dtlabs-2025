import os
import jwt
from app.api.services.user_service import UserService


class AuthService:

    async def login(email: str, password: str) -> str:
        user = await UserService.verify_password(email, password)
        if user == None:
            raise Exception ("Email or password incorrect")
        else:
            data = {user.id, user.email}
            token = jwt.encode(
                data,
                key=os.getenv('MY_SECRET')
            )
            return token