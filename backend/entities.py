from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


# ------------------------------------- #
#            database models            #
# ------------------------------------- #

class UserChatLinkInDB(SQLModel, table=True):
    """Database model for many-to-many relation of users to chats."""

    __tablename__ = "user_chat_links"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    chat_id: int = Field(foreign_key="chats.id", primary_key=True)


class UserInDB(SQLModel, table=True):
    """Database model for user."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    chats: list["ChatInDB"] = Relationship(
        back_populates="users",
        link_model=UserChatLinkInDB,
    )


class ChatInDB(SQLModel, table=True):
    """Database model for chat."""

    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner: UserInDB = Relationship()
    users: list[UserInDB] = Relationship(
        back_populates="chats",
        link_model=UserChatLinkInDB,
    )
    messages: list["MessageInDB"] = Relationship(back_populates="chat")


class MessageInDB(SQLModel, table=True):
    """Database model for message."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    user_id: int = Field(foreign_key="users.id")
    chat_id: int = Field(foreign_key="chats.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: UserInDB = Relationship()
    chat: ChatInDB = Relationship(back_populates="messages")


# ------------------------------------- #
#            request models             #
# ------------------------------------- #


# metadata
class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int


class ChatMetaData(BaseModel):
    message_count: int
    user_count: int


# users
class UserCreate(SQLModel):
    """Represents parameters for adding a new user to the system."""

    id: int


class UserUpdate(SQLModel):
    """Represents parameters for updating a user in the system."""

    id: int
    created_at: datetime


# messages
class MessageCreate(SQLModel):
    text: str


# chats
class ChatUpdate(SQLModel):
    """Represents parameters for updating a chat in the system."""

    name: str


# ------------------------------------- #
#            response models            #
# ------------------------------------- #


class User(SQLModel):
    """Represents an API response for a user."""

    id: int
    username: str
    email: str
    created_at: datetime


class UserResponse(BaseModel):
    """Represents an API response for a User."""

    user: User


class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[User]


# messages-----------

class Message(SQLModel):
    id: int
    text: str
    user_id: int
    chat_id: int
    created_at: datetime
    user: User


class MessageCollection(BaseModel):
    meta: Metadata
    messages: list[Message]


class MessageResponse(BaseModel):
    message: Message


class GetMessagesForChat(BaseModel):
    """Represents parameters for updating a chat in the system."""
    meta: Metadata
    messages: list[Message]


class UsersInChatResponse(BaseModel):
    meta: Metadata
    users: list[User]


# chats-----

class Chat(SQLModel):
    id: int
    name: str
    owner: User
    created_at: datetime


class ChatResponse(BaseModel):
    """Represents an API response for a User."""

    chat: Chat


class ChatByIDResponse(BaseModel):
    meta: ChatMetaData
    chat: Chat
    messages: Optional[list[Message]] = None
    users: Optional[list[User]] = None


class ChatsForUserResponse(BaseModel):
    """Represents an API response for chats for user"""

    meta: Metadata
    chats: list[Chat]


class ChatCollection(BaseModel):
    meta: Metadata
    chats: list[Chat]
