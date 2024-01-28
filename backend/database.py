import json
from datetime import datetime
from fastapi import HTTPException

from backend.entities import (
    UserInDB,
    UserCreate,
    UserUpdate,
)

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)


class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id


#   -------- users --------   #


def get_users() -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return [UserInDB(**user_data) for user_data in DB["users"].values()]


def get_all_users() -> list[UserInDB]:
    return [UserInDB(**user_data) for user_data in DB["users"].values()]


def create_user(user_create: UserCreate) -> UserInDB:
    """
    Create a new user in the database.

    :param user_create: attributes of the user to be created
    :return: the newly created user
    """
    user_id = user_create.id

    if user_create.id in DB["users"]:
        error_detail = {
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": user_id
        }
        raise HTTPException(422, detail=error_detail)

    user = UserInDB(
        id=user_create.id,
        created_at=datetime.now().isoformat(),
        **user_create.model_dump(),
    )
    DB["users"][user.id] = user.model_dump()
    return user


def get_user_by_id(user_id: str) -> UserInDB:
    """
    Retrieve an user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """

    if user_id in DB["users"]:
        return UserInDB(**DB["users"][user_id])

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)

