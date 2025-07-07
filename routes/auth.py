from typing import Annotated
from dependencies.connections import SessionDep
from fastapi import APIRouter, HTTPException, status, Form, Body
from schemas.auth import AuthCredentials
from schemas.user import UserCreate, UserPublicResponse
from models.user import User, UserStatus
from sqlmodel import select

router = APIRouter()


@router.post("/register", response_model=UserPublicResponse)
def create_user(user_data: Annotated[UserCreate, Body()], session: SessionDep):
    already_exists = select(User).where(User.email == user_data.username).exists()
    if already_exists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "This email is already registered to an existing account",
        )

    user = User(
        **user_data,
        email=user_data.username,
        hashed_password="hashed_" + user_data.password,
        status=UserStatus.ACTIVE,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {
        "message": "User Registration completed",
        "data": user,
    }


@router.post("/token")
def generate_auth_tokens(
    credentials: Annotated[AuthCredentials, Form()], session: SessionDep
):
    statement = select(User).where(
        (User.email == credentials.username)
        & (User.hashed_password == "hashed_" + credentials.password)
    )
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return {
        "access_token": f"token__{user.id}",
        "token_type": "bearer",
    }
