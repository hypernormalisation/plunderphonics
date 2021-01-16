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
