from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.userid == user_id).first()


def get_user_by_username(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.username == user_name).first()