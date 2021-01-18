import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

User = Base.classes.users
OriginalTrack = Base.classes.original_tracks


# noinspection SpellCheckingInspection
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True)
#     password = Column(String)
#     email_address = Column(String)
#     date_modified = Column(TIMESTAMP)
#     date_created = Column(TIMESTAMP, default=datetime.datetime.utcnow)
#
#
# class OriginalTrack(Base):
#     __tablename__ = "original_tracks"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, nullable=False)
#     url = Column(String)
#     name = Column(String)
#     date_modified = Column(TIMESTAMP)
#     date_created = Column(TIMESTAMP)
#
