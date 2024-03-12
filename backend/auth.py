import os

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session
from backend import database as db
from entities import NewUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

jwt_key = os.environ.get("JWT_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/registration", status_code=200)
def register_new_user(new_user: NewUser, session: Session = Depends(db.get_session)):
    # 1) If the username and email fields do not match any existing users (the database schema has uniqueness
    # constraints on these fields), a new user is added to the database with the appropriate hashed_password, and the
    # response has HTTP status code 201 and adheres to the following format:

    # 2) If the field username or email has a value that matches an existing user, the response has HTTP status code
    # 422 and the response adheres to the format:

    pass


@auth_router.post(path='/token', status_code=200)
def get_jwt_token():
    pass

