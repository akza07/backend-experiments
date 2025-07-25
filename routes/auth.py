from typing import Annotated
from datetime import timedelta
from dependencies.connections import SessionDep
from fastapi import APIRouter, HTTPException, status, Form, Body
from schemas.auth import AuthCredentials, Token
from schemas.user import UserCreate, UserPublicResponse
from services.auth_service import (
    get_password_hash,
    verify_password_hash,
    create_access_token,
)
from models.user import User, UserStatus
from sqlmodel import select, exists

router = APIRouter()


@router.post("/register", response_model=UserPublicResponse)
def create_user(user_data: Annotated[UserCreate, Body()], session: SessionDep):
    already_exists_stmt = select(exists().where(User.email == user_data.username))
    already_exists = session.exec(already_exists_stmt).first()
    if already_exists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "This email is already registered to an existing account",
        )

    user = User(
        **user_data.dict(),
        email=user_data.username,
        hashed_password=get_password_hash(user_data.password),
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
    statement = select(User).where((User.email == credentials.username))
    user: User = session.exec(statement).one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not verify_password_hash(credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token({"sub": str(user.id)}, timedelta(minutes=15))

    return Token(access_token=access_token, token_type="bearer")
