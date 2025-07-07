from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import StrEnum


class UserStatus(StrEnum):
    # Verification Pending
    PENDING = "PENDING"
    # Verified and Active
    ACTIVE = "ACTIVE"
    # Inactive or Temperorily in-accessible
    INACTIVE = "INACTIVE"
    # Soft Deleted
    DELETED = "DELETED"
    # Blocked
    BLOCKED = "BLOCKED"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    full_name: str | None = Field(index=True, nullable=True)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str | None = Field(default=None)
    is_active: bool = Field(default=False, nullable=False)
    is_disabled: bool = Field(default=False, nullable=True)
    status: UserStatus = Field(default=UserStatus.PENDING)

