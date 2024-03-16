from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.auth import AuthException, get_current_user
from backend import database as db
from backend.entities import *

users_router = APIRouter(prefix="/users", tags=["Users"])


# GET /users returns a list of users sorted by id alongside some metadata. The metadata has the count of users (
# integer). The response has HTTP status code 200 and adheres to the following format:
@users_router.get("", status_code=200, response_model=UserCollection)
def get_users(session: Session = Depends(db.get_session)):
    """

    :return: a list of users
    returns a list of users sorted by id with metadata

    """
    users = db.get_all_users(session)
    return UserCollection(
        meta={"count": len(users)},
        users=users,
    )


# GET /users/{user_id} returns a user for a given id. If a user with the id exists, the response has status code 200
# and adheres to the format:
@users_router.get(
    "/{user_id}",
    status_code=200,
    response_model=UserResponse,
    description="get a user given a user_id")
def get_user(user_id: int, session: Session = Depends(db.get_session)):
    """

    :param session:
    :param user_id: the user id
    :return: UserResponse
    returns a user for a given id

    """
    return UserResponse(user=db.get_user_by_id(user_id, session))


# GET /users/{user_id}/chats returns a list of chats for a given user id alongside some metadata.
@users_router.get(
    "/{user_id}/chats",
    status_code=200,
    response_model=ChatsForUserResponse,
    description="return list of chats for a given user id")
def get_user_chats(user_id: int, session: Session = Depends(db.get_session)):
    """
    :param session:
    :param user_id: the user_id
    :return: a list of chats for user
    return list of chats for a given user id
    """

    chats = db.get_chats_by_user_id(user_id, session)

    return ChatsForUserResponse(
        meta={"count": len(chats)},
        chats=sorted(chats, key=lambda chat: getattr(chat, "name")),
    )


# GET /users/me returns the current user. It requires a valid bearer token. If the token is valid, the response has
# HTTP status code 200 and the response adheres to the format:
@users_router.get(
    "/me",
    response_model=UserResponse,
    status_code=200)
def get_self(user: UserInDB = Depends(get_current_user)):
    """Get current user."""
    if user:
        return UserResponse(user=user)
    else:
        raise AuthException()


# PUT /users/me can be used to update the username or email of the current user. It requires a valid bearer token.
# The request body has two optional fields username and email, ie, it is of the form
@users_router.put("/me", status_code=200, response_model=UserResponse)
def get_self(
    user: UserInDB = Depends(get_current_user),
    new_username: str = None,
    new_email: str = None,
    session: Session = Depends(db.get_session)
):
    """update user."""

    return UserResponse(user=db.update_user(session, user, new_username, new_email))
