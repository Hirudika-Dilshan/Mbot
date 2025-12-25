from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.user import UserCreate, UserPublic
from app.services.auth_service import create_user
from app.utils.database import get_database

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> UserPublic:
    """
    Register a new user account.
    """
    return await create_user(db, user)



