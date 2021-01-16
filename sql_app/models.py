import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


# noinspection SpellCheckingInspection
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    email_address = Column(String)
    date_modified = Column(TIMESTAMP)
    date_created = Column(TIMESTAMP, default=datetime.datetime.utcnow)
