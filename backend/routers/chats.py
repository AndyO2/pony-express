from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session

from backend.auth import get_current_user
from backend import database as db
from backend.entities import *

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


# GET /chats returns a list of chats sorted by name alongside some metadata.
# The metadata has the count of chats (integer). The response has the HTTP status code 200
@chats_router.get("", response_model=ChatCollection)
def get_chats(session: Session = Depends(db.get_session)):
    """

    :return: a list of chats
    gets all chats sorted by name

    """
    chats = db.get_all_chats(session)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=chats,
    )


@chats_router.get(
    "/{chat_id}",
    status_code=200,
    response_model=ChatByIDResponse,
    response_model_exclude_none=True)
def get_chat_by_id(
        chat_id: int,
        include: List[str] = Query(None),
        session: Session = Depends(db.get_session)):
    """

    :param session:
    :param chat_id: the chat id
    :return: the chat
    gets a chat by id

    """
    chat = db.get_chat_by_id(chat_id, session)
    chat_meta_data = ChatMetaData(
        message_count=len(chat.messages),
        user_count=len(chat.users)
    )
    ret = ChatByIDResponse(
        meta=chat_meta_data,
        chat=chat,
    )

    if "messages" in include:
        ret.messages = sorted(chat.messages, key=lambda message: getattr(
            message, "created_at")),
    if "users" in include:
        ret.users = chat.users

    return ret

# PUT /chats/{chat_id} updates a chat for a given id.


@chats_router.put("/{chat_id}", status_code=200, response_model=ChatResponse)
def update_chat(chat_id: int, chat_update: ChatUpdate, session: Session = Depends(db.get_session)):
    """

    :param session:
    :param chat_id: the chat id
    :param chat_update: how to update chat
    :return: the new chat
    updates a chat

    """
    return ChatResponse(
        chat=db.update_chat(chat_id, chat_update, session),
    )


# GET /chats/{chat_id}/messages returns a list of messages for a given chat id
# alongside some metadata. sort by created at
@chats_router.get(
    "/{chat_id}/messages",
    status_code=200,
    response_model=MessageCollection)
def get_messages_for_chat_id(chat_id: int, session: Session = Depends(db.get_session)):
    """

    :param session:
    :param chat_id: the chat id
    :return: a list of messages for a chat
    returns a list of messages for a given chat id

    """
    messages = db.get_messages_in_chat(chat_id, session)

    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=lambda message: getattr(
            message, "created_at"))
    )


# GET /chats/{chat_id}/users returns a list of users for a given chat id alongside some metadata. The list of users
# consists of only those users participating in the corresponding chat, sorted by id. The metadata contains the count
# of users (integer). If a chat with the id exists, the response has the HTTP status code 200 and adheres to the format:
@chats_router.get(
    "/{chat_id}/users",
    status_code=200,
    response_model=UsersInChatResponse
)
def get_users_for_chat(chat_id: int, session: Session = Depends(db.get_session)) -> UsersInChatResponse:
    """

    :param session:
    :param chat_id: id of the chat
    :return: a list of users in a chat
    returns a list of users for a given chat

    """
    users = db.get_users_in_chat(chat_id, session)
    return UsersInChatResponse(
        meta={"count": len(users)},
        users=users,
    )


# POST /chats/{chat_id}/messages creates a new message in the chat, authored by the current user. It requires a valid
# bearer token. The request body adheres to the format:
@chats_router.post(
    "/{chat_id}/messages",
    status_code=201,
    response_model=MessageResponse)
def create_message(
        session: Session = Depends(db.get_session),
        user: UserInDB = Depends(get_current_user),
        new_message_text: MessageCreate = None,
        chat_id: int = None):
    """

    :param new_message_text:
    :param session:
    :param user:
    :param chat_id:
    :return:
    """
    # checks that chat exists (throws exception if not)
    db.get_chat_by_id(chat_id, session=session)

    test = {
        "text": new_message_text.text,
        "user_id": user.id,
        "chat_id": chat_id
    }

    message = MessageInDB(**test)

    session.add(message)
    session.commit()
    session.refresh(message)

    return MessageResponse(
        message=message
    )
