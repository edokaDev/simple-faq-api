from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import validator, EmailStr


class UserBase(SQLModel):
    username: str = Field(index=True)
    password: str
    email: EmailStr


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    password2: str

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords mismatched')
        return v


class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserLogin(SQLModel):
    username: str
    password: str
