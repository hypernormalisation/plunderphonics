import bcrypt

from sqlalchemy.orm import Session

from . import models, schemas


#########################################################################
# Create.
#########################################################################
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password_bytes = bcrypt.hashpw(user.password.encode('utf-8'),
                                          bcrypt.gensalt())
    hashed_password_str = hashed_password_bytes.decode('utf-8')
    print(hashed_password_str, type(hashed_password_str))
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password_str,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#########################################################################
# Read.
#########################################################################
def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, user_name: str) -> models.User:
    return db.query(models.User).filter(models.User.username == user_name).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


#########################################################################
# Update.
#########################################################################
def update_email(db: Session, user_id: int, new_email: str) -> models.User:
    current_user = db.query(models.User).filter(models.User.id == user_id).first()
    current_user.email = new_email
    db.commit()
    return current_user


def update_password(db: Session, user_id: int, new_password: str) -> models.User:
    hashed_password_bytes = bcrypt.hashpw(new_password.encode('utf-8'),
                                          bcrypt.gensalt())
    hashed_password_str = hashed_password_bytes.decode('utf-8')
    current_user = db.query(models.User).filter(models.User.id == user_id).first()
    current_user.hashed_password = hashed_password_str
    db.commit()
    return current_user
