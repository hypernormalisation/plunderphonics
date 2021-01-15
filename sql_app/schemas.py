import datetime

from typing import List, Optional

from pydantic import BaseModel


# noinspection SpellCheckingInspection
class UserBase(BaseModel):
    emailaddress: str


# noinspection SpellCheckingInspection
class User(UserBase):
    userid: int
    username: str
    datemodified: datetime.datetime
    datecreated: datetime.datetime

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    password: str
