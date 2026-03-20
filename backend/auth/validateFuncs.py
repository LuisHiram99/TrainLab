from secrets import token_hex
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = token_hex(32) 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def email_exists(email: str, db: AsyncSession) -> bool:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first() is not None


async def validate_user_exists(username: str, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await validate_user_exists(username, db)
    if not user and not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(email: str, user_id: str, token_version: int, expires_delta: timedelta | None = None):
    encode = {"sub": email, "user_id": user_id, "token_version": token_version}
    expires = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)