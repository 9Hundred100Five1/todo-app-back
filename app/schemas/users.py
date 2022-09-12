from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    id: int
    
    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserSignup(UserBase):
    pass


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass

class UserDelete(UserBase):
    pass

class SnsType(str, Enum):
    email: str = "email"
    facebook: str = "facebook"
    google: str = "google"
    kakao: str = "kakao"

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    username: Union[str, None] = None

    class Config:
        orm_mode = True

class UserInDB(UserBase):
    hashed_password: str