import json
from datetime import date
from uuid import uuid4

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


def get_all_users() -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return [UserInDB(**user_data) for user_data in DB["users"].values()]


def create_user(user_create: UserCreate) -> UserInDB:
    """
    Create a new user in the database.

    :param user_create: attributes of the user to be created
    :return: the newly created user
    """

    user = UserInDB(
        id=uuid4().hex,
        intake_date=date.today(),
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

    return UserInDB(**DB["users"][user_id])


def update_user(user_id: str, user_update: UserUpdate) -> UserInDB:
    """
    Update an user in the database.

    :param user_id: id of the user to be updated
    :param user_update: attributes to be updated on the user
    :return: the updated user
    """

    user = get_user_by_id(user_id)
    for key, value in user_update.update_attributes().items():
        setattr(user, key, value)
    return user


def delete_user(user_id: str):
    """
    Delete an user from the database.

    :param user_id: the id of the user to be deleted
    """

    user = get_user_by_id(user_id)
    del DB["users"][user.id]