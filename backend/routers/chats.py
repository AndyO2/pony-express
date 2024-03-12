from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from backend import database as db
from backend.entities import *

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


# GET /chats returns a list of chats sorted by name alongside some metadata.
# The metadata has the count of chats (integer). The response has the HTTP status code 200
@chats_router.get("", status_code=200, response_model=ChatCollection)
def get_chats(session: Session = Depends(db.get_session)):
    """

    :return: a list of chats
    gets all chats sorted by name

    """
    chats = db.get_all_chats(session)
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=lambda chat: getattr(chat, "name")),
    )


@chats_router.get("/{chat_id}", status_code=200, response_model=ChatResponse)
def get_chat_by_id(chat_id: int, session: Session = Depends(db.get_session)):
    """

    :param session:
    :param chat_id: the chat id
    :return: the chat
    gets a chat by id

    """
    chat = db.get_chat_by_id(chat_id, session)
    if chat is None:
        error_detail = {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        }
        raise HTTPException(status_code=404, detail=error_detail)
    return ChatResponse(chat=chat)


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


# DELETE /chats/{chat_id} deletes a chat for a given id
@chats_router.delete(
    "/{chat_id}",
    status_code=204,
    response_model=None)
def delete_chat(chat_id: int, session: Session = Depends(db.get_session)):
    """

    :param session:
    :param chat_id: the chat id
    :return: nothing
    deletes a chat

    """
    db.delete_chat(chat_id, session)


# GET /chats/{chat_id}/messages returns a list of messages for a given chat id
# alongside some metadata.
@chats_router.get(
    "/{chat_id}/messages",
    status_code=200)
def get_messages_for_chat_id(chat_id: int, session: Session = Depends(db.get_session)):
    """

    :param session:
    :param chat_id: the chat id
    :return: a list of messages for a chat
    returns a list of messages for a given chat id

    """
    messages = db.get_messages_for_chat(chat_id, session)

    return MessageCollection(
        meta={"count": len(messages)},
        messages=messages
    )


# GET /chats/{chat_id}/users returns a list of users for a given chat id alongside some metadata. The list of users
# consists of only those users participating in the corresponding chat, sorted by id. The metadata contains the count
# of users (integer). If a chat with the id exists, the response has the HTTP status code 200 and adheres to the format:
@chats_router.get(
    "/{chat_id}/users",
    status_code=200,
)
def get_users_for_chat(chat_id: int, session: Session = Depends(db.get_session)) -> UsersInChatResponse:
    """

    :param session:
    :param chat_id: id of the chat
    :return: a list of users in a chat
    returns a list of users for a given chat

    """
    chat = db.get_chat_by_id(chat_id, session)

    users = []
    for user_id in sorted(chat.user_ids):
        user = db.get_user_by_id(user_id, session)
        users.append(user)

    return UsersInChatResponse(
        meta={"count": len(users)},
        users=users,
    )
