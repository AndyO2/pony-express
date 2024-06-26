import json
from typing import Sequence, Type

from fastapi import HTTPException
from backend.entities import *
from sqlmodel import Session, SQLModel, create_engine, select

from backend.entities import ChatInDB, UserInDB
import os

# DB funcs should return SQL Models (Routes should return BaseModel)

if os.environ.get("DB_LOCATION") == "EFS":
    db_path = "/mnt/efs/pony_express.db"
    echo = False
else:
    db_path = "backend/pony_express.db"
    echo = True

engine = create_engine(
    f"sqlite:///{db_path}",
    echo=echo,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# END A3 ADDITIONS------------------------

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)


class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id


#   -------- users --------   #
def get_all_users(session: Session) -> Sequence[UserInDB]:
    return session.exec(select(UserInDB)).all()


def create_user(user_create: UserCreate, session: Session) -> UserInDB:
    """
    Create a new user in the database.

    :param session:
    :param user_create: attributes of the user to be created
    :return: the newly created user
    """
    user_id = user_create.id

    if user_id in DB["users"]:
        error_detail = {
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": user_id
        }
        raise HTTPException(422, detail=error_detail)

    user = UserInDB(
        id=user_id,
        created_at=datetime.now(),
    )
    DB["users"][user_id] = user.model_dump()
    return user


def get_user_by_id(user_id: int, session: Session) -> UserInDB:
    """
    Retrieve a user from the database.

    :param session:
    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """
    user = session.get(UserInDB, user_id)
    if user:
        return user

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)


def update_user(session: Session, user_id: int, user_update: UserUpdate) -> UserInDB:
    user = get_user_by_id(user_id, session)

    for attr, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, attr, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


#   -------- chats --------   #
def get_all_chats(session: Session) -> list[ChatInDB]:
    return session.exec(select(ChatInDB)).all()


def get_chats_by_user_id(user_id: int, session: Session) -> list[ChatInDB]:
    # check if user exists
    user = session.exec(select(UserInDB).where(UserInDB.id == user_id)).one()

    return user.chats


def get_chat_by_id(chat_id: int, session: Session) -> ChatInDB:
    """
    Retrieve a chat from the database.

    :param session:
    :param chat_id: the id of the chat
    :return: the retrieved chat
    """
    chat = session.get(ChatInDB, chat_id)
    if chat:
        return chat

    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)


def update_chat(chat_id: int, chat_update: ChatUpdate, session: Session) -> Type[ChatInDB]:
    """
    Update an animal in the database.

    :param session:
    :param chat_id: id of the chat to be updated
    :param chat_update: attributes to be updated on the chat
    :return: the updated animal
    :raises EntityNotFoundException: if no such animal id exists
    """

    chat = get_chat_by_id(chat_id, session)
    for attr, val in chat_update.model_dump(exclude_unset=True).items():
        setattr(chat, attr, val)

    session.add(chat)
    session.commit()
    session.refresh(chat)

    return chat


def delete_chat(chat_id: int, session: Session):
    """
    Delete a chat from the database.

    :param session:
    :param chat_id: the id of the chat to be deleted
    :raises EntityNotFoundException: if no such animal exists
    """

    chat = get_chat_by_id(chat_id, session)
    del DB["chats"][chat.id]


def get_messages_in_chat(chat_id: int, session: Session) -> list[MessageInDB]:
    chat = get_chat_by_id(chat_id, session)

    return chat.messages


def get_users_in_chat(chat_id: int, session: Session) -> list[UserInDB]:
    chat = get_chat_by_id(chat_id, session)

    return chat.users


# messages ----------------------------
def create_message(session: Session, chat_id: int, text: str):
    chat = get_chat_by_id(chat_id, session)

    pass
