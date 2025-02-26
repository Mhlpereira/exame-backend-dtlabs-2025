from pydantic import BaseModel , EmailStr ,  field_validator

class CreateUserDTO(BaseModel):
    email: EmailStr 
    password: str
    confirm_password: str


    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, password, confirm:str):
        if 'password1' in confirm and password != confirm['password1']:
            raise ValueError('passwords do not match')
        return password