import datetime

from typing import List, Optional

from pydantic import BaseModel


class SimpleMessage(BaseModel):
    """Schema for a simple message."""
    message: str


#########################################################################
# OAuth2 Token schemas.
#########################################################################
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


#########################################################################
# User schemas.
#########################################################################
class UserBase(BaseModel):
    """Base user, with universally required fields."""
    username: str
    email: str


class UserCreate(UserBase):
    """Schema for user creation, taking the un-hashed password."""
    password: str


class User(UserBase):
    """The public schema for established users, leaves out hashed password."""
    id: int
    date_modified: datetime.datetime
    date_created: datetime.datetime

    class Config:
        orm_mode = True


class UserAuthenticate(User):
    """Schema for authentication."""
    hashed_password: str


#########################################################################
# Track schemas.
#########################################################################
class TrackBase(BaseModel):
    id: int
    name: str
    date_modified: datetime.datetime
    date_created: datetime.datetime

    class Config:
        orm_mode = True
