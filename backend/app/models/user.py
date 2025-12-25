from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Request payload for creating a new user account."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None


class UserInDB(BaseModel):
    """Internal representation persisted to MongoDB."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    hashed_password: str
    full_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserPublic(BaseModel):
    """Response model exposed to the client."""

    model_config = ConfigDict(extra="forbid")

    id: str
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime



