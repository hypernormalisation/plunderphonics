import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


# noinspection SpellCheckingInspection
class User(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    emailaddress = Column(String)
    datemodified = Column(TIMESTAMP)
    datecreated = Column(TIMESTAMP, default=datetime.datetime.utcnow)
