import bcrypt
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.user import UserCreate, UserInDB, UserPublic


def _hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def create_user(db: AsyncIOMotorDatabase, user: UserCreate) -> UserPublic:
    """
    Create a new user record if the email is not already registered.
    """
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    user_in_db = UserInDB(
        email=user.email,
        full_name=user.full_name,
        hashed_password=_hash_password(user.password),
    )
    result = await db["users"].insert_one(user_in_db.model_dump())

    return UserPublic(
        id=str(result.inserted_id),
        email=user_in_db.email,
        full_name=user_in_db.full_name,
        created_at=user_in_db.created_at,
    )



