from pydantic import BaseModel, EmailStr


class AuthCredentials(BaseModel):
    username: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
