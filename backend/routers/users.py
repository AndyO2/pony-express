from fastapi import APIRouter, HTTPException
from backend import database as db

from backend.entities import *

users_router = APIRouter(prefix="/users", tags=["Users"])


# GET /users returns a list of users sorted by id alongside some metadata. The metadata has the count of users (
# integer). The response has HTTP status code 200 and adheres to the following format:
@users_router.get("", status_code=200, response_model=UserCollection)
def get_users():
    """

    :return: a list of users
    returns a list of users sorted by id with metatdata

    """
    users = db.get_all_users()

    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=lambda user: getattr(user, "id")),
    )


# POST /users creates a new user
@users_router.post(
    "",
    status_code=200,
    response_model=UserResponse)
def create_user(user_create: UserCreate):
    """

    :param user_create: the user to create
    :return: User Response
    creates a new user

    """
    return UserResponse(user=db.create_user(user_create))


# GET /users/{user_id} returns a user for a given id. If a user with the id exists, the response has status code 200
# and adheres to the format:
@users_router.get(
    "/{user_id}",
    status_code=200,
    response_model=UserResponse,
    description="get a user given a user_id")
def get_user(user_id: int):
    """

    :param user_id: the user id
    :return: UserResponse
    returns a user for a given id

    """
    return UserResponse(user=db.get_user_by_id(user_id))


# GET /users/{user_id}/chats returns a list of chats for a given user id alongside some metadata.
@users_router.get(
    "/{user_id}/chats",
    status_code=200,
    response_model=ChatsForUserResponse,
    description="return list of chats for a given user id")
def get_user_chats(user_id: int):
    """
    :param user_id: the user_id
    :return: a list of chats for user
    return list of chats for a given user id
    """

    chats = db.get_chats_by_user_id(user_id)

    return ChatsForUserResponse(
        meta={"count": len(chats)},
        chats=sorted(chats, key=lambda chat: getattr(chat, "name")),
    )

