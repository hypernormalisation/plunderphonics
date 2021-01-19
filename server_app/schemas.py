import datetime

from typing import List, Optional

from pydantic import BaseModel


# noinspection SpellCheckingInspection
class UserBase(BaseModel):
    email_address: str


# noinspection SpellCheckingInspection
class User(UserBase):
    id: int
    username: str
    email_address: str
    date_modified: datetime.datetime
    date_created: datetime.datetime

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class SimpleMessage(BaseModel):
    message: str


class TrackBase(BaseModel):
    id: int
    name: str
    date_modified: datetime.datetime
    date_created: datetime.datetime

    class Config:
        orm_mode = True
