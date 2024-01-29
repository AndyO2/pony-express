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
    created_at: datetime


class UserResponse(BaseModel):
    """Represents an API response for a User."""

    user: UserInDB


class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[UserInDB]


# chats-----

class Chats(BaseModel):
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime


class ChatInDB(BaseModel):
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime


class ChatResponse(BaseModel):
    """Represents an API response for a User."""

    chat: ChatInDB


class ChatsForUserResponse(BaseModel):
    """Represents an API response for chats for user"""

    meta: Metadata
    chats: list[ChatInDB]


class ChatCollection(BaseModel):
    meta: Metadata
    chats: list[ChatInDB]


class ChatUpdate(BaseModel):
    """Represents parameters for updating a chat in the system."""

    name: str


# messages-----------
class Message(BaseModel):
    """Represents parameters for updating a chat in the system."""
    id: str
    user_id: str
    text: str
    created_at: datetime


class MessageCollection(BaseModel):
    """Represents parameters for updating a chat in the system."""
    meta: Metadata
    messages: list[Message]


class GetMessagesForChat(BaseModel):
    """Represents parameters for updating a chat in the system."""
    meta: Metadata
    messages: list[Message]


class UsersInChatResponse(BaseModel):
    meta: Metadata
    users: list[str]
