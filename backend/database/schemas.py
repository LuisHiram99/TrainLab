from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

# ------------------------ User Schemas ------------------ 
class UserBase(BaseModel): 
    username: str = Field(..., min_length=2,max_length=100)
    email: EmailStr= Field(..., min_length=2, max_length=50)

    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)

    role: RoleEnum

class UserCreate(UserBase):
    password: str = Field(..., min_length=10, max_length=100)

    model_config = {"json_schema_extra": {"example": {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "john@example.com",
        "password": "Secretpassword1!",
        "role": "admin",
    }}}

class createUserRequest(BaseModel):
    username: str = Field(..., min_length=2,max_length=100)
    email: EmailStr= Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=10, max_length=100)

    model_config = {"json_schema_extra": 
                    {"example": {
                        "username": "johndoe",
                        "email": "john@example.com",
                        "password": "Secretpassword1!"
                    }}}
    