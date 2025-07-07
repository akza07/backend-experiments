from sqlmodel import Session
from models.user import User
from fastapi import HTTPException,status

def get_current_user(session: Session, token:str):
    print(token)
    user_id = token.split("token__")[1]
    print(user_id)
    user: User | None = session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,"User does not exist")
    if user.is_disabled:
        raise HTTPException(status.HTTP_403_FORBIDDEN,"This account has been blocked")
    return user

