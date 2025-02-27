from pydantic import BaseModel , EmailStr 

class LoginDTO(BaseModel):
    email: EmailStr
    password: str

class TokenDTO(BaseModel):
    token: str
    token_type: str