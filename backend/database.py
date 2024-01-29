import json
from datetime import datetime, timezone
from fastapi import HTTPException

from backend.entities import (
    UserInDB,
    UserCreate,
    UserUpdate,
    ChatInDB,
    ChatUpdate,
)

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)


class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id


#   -------- users --------   #


def get_all_users() -> list[UserInDB]:
    return [UserInDB(**user_data) for user_data in DB["users"].values()]


def create_user(user_create: UserCreate) -> UserInDB:
    """
    Create a new user in the database.

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
        created_at=datetime.now(timezone.utc).isoformat(),
        **user_create.model_dump(),
    )
    DB["users"][user_id] = user.model_dump()
    # return user


def get_user_by_id(user_id: str) -> UserInDB:
    """
    Retrieve a user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """

    if user_id in DB["users"]:
        return UserInDB(**DB["users"][user_id])

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)


#   -------- users --------   #
def get_all_chats() -> list[ChatInDB]:
    return [ChatInDB(**chat_data) for chat_data in DB["chats"].values()]


def get_chats_by_user_id(user_id: str) -> list[ChatInDB]:
    if user_id not in DB["users"]:
        raise EntityNotFoundException(entity_name="User", entity_id=user_id)

    ret = []
    chats = get_all_chats()

    for chat in chats:
        if chat.user_ids.__contains__(user_id):
            ret.append(chat)

    return ret


def get_chat_by_id(chat_id: str) -> ChatInDB:
    """
    Retrieve a chat from the database.

    :param chat_id: the id of the chat
    :return: the retrieved chat
    """

    if chat_id in DB["chats"]:
        return ChatInDB(**DB["chats"][chat_id])

    raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)


def update_chat(chat_id: str, chat_update: ChatUpdate) -> ChatInDB:
    """
    Update an animal in the database.

    :param chat_id: id of the chat to be updated
    :param chat_update: attributes to be updated on the chat
    :return: the updated animal
    :raises EntityNotFoundException: if no such animal id exists
    """

    chat = get_chat_by_id(chat_id)
    if chat_update.name is not None:
        chat.name = chat_update.name

    # update in database
    DB["chats"][chat.id] = chat.model_dump()

    return chat


def delete_chat(chat_id: str):
    """
    Delete a chat from the database.

    :param chat_id: the id of the chat to be deleted
    :raises EntityNotFoundException: if no such animal exists
    """

    chat = get_chat_by_id(chat_id)
    del DB["chats"][chat.id]


def get_messages_for_chat(chat_id: str):
    pass
