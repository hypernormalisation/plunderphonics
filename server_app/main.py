"""
Main web application script.

Run me from the project root with

    uvicorn server_app.main:app

"""
from datetime import datetime, timedelta
from typing import Optional, Union, List

from fastapi import (
    Depends, FastAPI, HTTPException,
    status, File, UploadFile, Form,
    Response, Cookie
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from .oauth2_password_bearer_with_cookie import OAuth2PasswordBearerWithCookie
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import user_crud, original_track_crud, schemas, models
from .database import get_db
from uuid import uuid4
from .sessions import create_session, delete_session, update_session_expiry

SECRET_KEY = "883b94400740a6912d8c614d757678fee01ee11e8a782466fc8fa1e3ff4de5e4"
ALGORITHM = "HS256"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

#########################################################################
# Functions and token/login endpoint for OAuth2.
#########################################################################
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(
        db: Session, username: str, password: str) -> Union[schemas.User, bool]:
    user = user_crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token_update_session(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        session_data = schemas.TokenData(username=username)
        if not update_session_expiry(payload.get("session_id")):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        return session_data


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    response: Response, 
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    session_id = create_session(user.id)
    access_token = create_access_token(
        data={"sub": user.username, "session_id": session_id}
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}", 
        httponly=True,
        samesite='None',
        secure=True)

@app.post("/logout", response_model=schemas.SimpleMessage)
async def logout(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    delete_session(payload["session_id"])
    return {'message': 'Logout successful'}


#########################################################################
# Custom FastAPI dependencies.
#########################################################################
async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> models.User:
    
    session_data = verify_token_update_session(token)
    user = user_crud.get_user_by_username(db, session_data.username)
    if user is None:
        raise credentials_exception
    return user


#########################################################################
# Testing endpoints in our API.
#########################################################################
@app.get("/private/test", dependencies=[Depends(get_current_user)],
         response_model=schemas.SimpleMessage)
async def private_test():
    """
    A test endpoint that requires authentication.
    """
    return {'message': 'you are part of the secret club'}


@app.get("/public/test", response_model=schemas.SimpleMessage)
async def public_test():
    """
    A test public endpoint that requires no authentication.
    """
    return {'message': 'anyone can see this'}


#########################################################################
# Data creation endpoints in our API.
#########################################################################
@app.post("/users/create", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@app.post("/tracks/upload")
async def upload_track(
    user_id: str = Form(...), 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    session_data = verify_token_update_session(token)
    """Uploads a track from the web app."""
    track_metadata =  {
        'name': file.filename,
        'date_modified': datetime.utcnow(),
        'date_created': datetime.utcnow(),
        'user_id': user_id
    }
    original_track_crud.create_track(db, track_metadata, file.file)


#########################################################################
# Data read endpoints in our API.
#########################################################################
@app.get("/users/me", response_model=schemas.User)
async def read_users_me(
    current_user: schemas.User = Depends(get_current_user)
):
    """Get information on the current User."""
    return current_user


@app.get("/tracks/original", response_model=List[schemas.TrackBase])
async def get_my_original_tracks(
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get the current user's list of original tracks."""
    return original_track_crud.get_tracks_by_user_id(db, current_user.id)


#########################################################################
# Data update endpoints in our API.
#########################################################################
@app.post("/users/update/email", response_model=schemas.User)
async def update_email(
        new_email: schemas.EmailUpdate,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """Change the current user's email address."""
    return user_crud.update_email(db, current_user.id, new_email.new_email)


@app.post("/users/update/password", response_model=schemas.User)
async def update_password(
        new_password: schemas.PasswordUpdate,
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """Change the current user's password."""
    return user_crud.update_password(db, current_user.id, new_password.new_password)


#########################################################################
# Data delete endpoints in our API.
#########################################################################
@app.post("/users/delete", response_model=schemas.SimpleMessage)
async def delete_user(
        current_user: schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """Delete the current user."""
    return user_crud.delete_user(db, current_user.id)
