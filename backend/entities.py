from datetime import date, datetime

from pydantic import BaseModel, Field


class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int


class User(BaseModel):
    """Represents an API response for a user."""

    id: str
    created_at: datetime


class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the system."""

    id: str


class UserUpdate(BaseModel):
    """Represents parameters for updating a user in the system."""

    id: str = None
    created_at: datetime


class UserInDB(BaseModel):
    """Represents a user in the database."""

    id: str
    created_at: datetime.isoformat()


class UserResponse(BaseModel):
    """Represents an API response for a User."""

    user: UserInDB


class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[UserInDB]
