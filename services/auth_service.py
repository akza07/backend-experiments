import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlmodel import select, Session
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from config import ENV
from models.user import User, UserStatus

# Deprecated flag disables the logger level for passlib
# and ignores version check for __about__.__version__
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta or timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=ENV.jwt_secret_key,
        algorithm=ENV.jwt_algorithm,
    )
    return encoded_jwt


def get_current_user_by_token(session: Session, token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=ENV.jwt_secret_key,
            algorithms=[ENV.jwt_algorithm],
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = get_user_by_id(session, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_by_id(session: Session, id: int):
    user = session.exec(
        select(User).where(User.id == id, User.status == UserStatus.ACTIVE)
    ).one_or_none()
    return user
