from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from database.database import get_db
from database.models import User
from secrets import token_hex
from database.schemas import UserCreate
from config import Settings
from .validateFuncs import email_exists, authenticate_user, create_access_token

settings = Settings()


router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = token_hex(32) 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

db_dependency = Annotated[AsyncSession, Depends(get_db)]

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: db_dependency):
    create_user_model = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=pwd_context.hash(user.password)
    )

    if await email_exists(user.email, db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db.add(create_user_model)
    await db.commit()
    await db.refresh(create_user_model)
    return {"message": "User created successfully", "user": create_user_model}

@router.post("/login", response_model=Token)
async def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user = await authenticate_user(db, username, password)

    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    token = create_access_token(email=user.email, user_id=str(user.user_id), token_version=user.token_version)
    return {"access_token": token, "token_type": "bearer"}

