import os
from datetime import datetime, timezone
from typing import Annotated, Dict, Type
from typing_extensions import Annotated, Doc

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from sqlmodel import Session, SQLModel, select

from backend import database as db
from backend.entities import User, UserInDB, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_duration = 3600  # seconds
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
jwt_key = os.environ.get("JWT_KEY", default="insecure-jwt-key-for-dev")
jwt_alg = "HS256"

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


# MODELS ------------------------------------
class UserRegistration(SQLModel):
    """Request model to register new user."""

    username: str
    email: str
    password: str


class AccessToken(BaseModel):
    """Response model for access token."""

    access_token: str
    token_type: str
    expires_in: int


class Claims(BaseModel):
    """Access token claims (aka payload)."""

    sub: str  # id of user
    exp: int  # unix timestamp


class AuthException(HTTPException):
    def __init__(self, error: str, description: str):
        super().__init__(
            status_code=401,
            detail={
                "error": error,
                "error_description": description,
            },
        )


class InvalidCredentials(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="invalid username or password",
        )


class InvalidToken(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="invalid access token",
        )


class ExpiredToken(AuthException):
    def __init__(self):
        super().__init__(
            error="invalid_client",
            description="expired bearer token",
        )


# Any route that requires a bearer token should have get_current_user as a dependency. This is accomplished by
# including the following parameter in the function signature.
# user: UserInDB = Depends(get_current_user)
def get_current_user(
        session: Session = Depends(db.get_session),
        token: str = Depends(oauth2_scheme),
) -> Type[UserInDB]:
    """FastAPI dependency to get current user from bearer token."""
    user = _decode_access_token(session, token)
    return user


# AUTH ROUTES -----------------------------------------
@auth_router.post(
    "/registration",
    response_model=UserResponse,
    status_code=201)
def register_new_user(
        registration: UserRegistration,
        # session: Session = Depends(db.get_session),
        session: Annotated[Session, Depends(db.get_session)],
):
    """Register new user."""
    same_username = session.exec(select(UserInDB).where(
        UserInDB.username == registration.username)).first()
    if same_username:
        detail = {
            "type": "duplicate_value",
            "entity_name": "User",
            "entity_field": "username",
            "entity_value": registration.username
        }
        raise HTTPException(status_code=422, detail=detail)

    same_email = session.exec(select(UserInDB).where(
        UserInDB.email == registration.email)).first()
    if same_email:
        detail = {
            "type": "duplicate_value",
            "entity_name": "User",
            "entity_field": "email",
            "entity_value": registration.email
        }
        raise HTTPException(status_code=422, detail=detail)

    hashed_password = pwd_context.hash(registration.password)
    user = UserInDB(
        **registration.model_dump(),
        hashed_password=hashed_password,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(user=user)


@auth_router.post(path="/token", response_model=AccessToken)
def get_access_token(
        form: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(db.get_session),
):
    """Get access token for user."""

    user = _get_authenticated_user(session, form)
    return _build_access_token(user)


def _get_authenticated_user(
        session: Session,
        form: OAuth2PasswordRequestForm,
) -> UserInDB:
    user = session.exec(
        select(UserInDB).where(UserInDB.username == form.username)
    ).first()

    if user is None or not pwd_context.verify(form.password, user.hashed_password):
        raise InvalidCredentials()

    return user


def _build_access_token(user: UserInDB) -> AccessToken:
    expiration = int(datetime.now(timezone.utc).timestamp()) + \
        access_token_duration
    claims = Claims(sub=str(user.id), exp=expiration)
    access_token = jwt.encode(
        claims.model_dump(), key=jwt_key, algorithm=jwt_alg)

    return AccessToken(
        access_token=access_token,
        token_type="Bearer",
        expires_in=access_token_duration,
    )


def _decode_access_token(session: Session, token: str) -> Type[UserInDB]:
    try:
        claims_dict = jwt.decode(token, key=jwt_key, algorithms=[jwt_alg])
        claims = Claims(**claims_dict)
        user_id = claims.sub
        user = session.get(UserInDB, user_id)

        if user is None:
            raise InvalidToken()

        return user
    except ExpiredSignatureError:
        raise ExpiredToken()
    except JWTError:
        raise InvalidToken()
    except ValidationError():
        raise InvalidToken()


def check_user_exists(session: Session, username: str, email: str) -> str:
    statement = select(UserInDB).where(UserInDB.username == username)
    user = session.exec(statement).first()
    if user is not None:
        return "username"
    statement = select(UserInDB).where(UserInDB.email == email)
    user = session.exec(statement).first()
    if user is not None:
        return "email"
    else:
        return ""
