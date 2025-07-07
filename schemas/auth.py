from pydantic import BaseModel, EmailStr

class AuthCredentials(BaseModel):
    username: EmailStr
    password: str
