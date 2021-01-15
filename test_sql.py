from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import user_crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

u = user_crud.get_user(db=db, user_id=1)
print(u, u.username)