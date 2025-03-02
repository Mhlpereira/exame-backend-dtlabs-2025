from pydantic import BaseModel, EmailStr, field_validator


class CreateUserDTO(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, password, value):
        if "password1" in value.data and password != value.data["password1"]:
            raise ValueError("passwords do not match")
        return password


class OutputUserDTO(BaseModel):
    email: str
