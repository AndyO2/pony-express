from fastapi import APIRouter, HTTPException
from backend import database as db
from backend.entities import (
    ChatCollection,
    ChatResponse,
    ChatUpdate,
    UsersInChatResponse,
    MessageCollection,
)

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


# GET /chats returns a list of chats sorted by name alongside some metadata.
# The metadata has the count of chats (integer). The response has the HTTP status code 200
@chats_router.get("", status_code=200, response_model=ChatCollection)
def get_chats():
    """

    :return: a list of chats
    gets all chats sorted by name

    """
    chats = db.get_all_chats()
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=lambda chat: getattr(chat, "name")),
    )


@chats_router.get("/{chat_id}", status_code=200, response_model=ChatResponse)
def get_chat_by_id(chat_id: str):
    """

    :param chat_id: the chat id
    :return: the chat
    gets a chat by id
    """
    chat = db.get_chat_by_id(chat_id)
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
def update_chat(chat_id: str, chat_update: ChatUpdate):
    """

    :param chat_id: the chat id
    :param chat_update: how to update chat
    :return: the new chat
    updates a chat

    """
    chat = db.get_chat_by_id(chat_id)
    if chat is None:
        error_detail = {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        }
        raise HTTPException(status_code=404, detail=error_detail)

    return ChatResponse(
        chat=db.update_chat(chat_id, chat_update),
    )


# DELETE /chats/{chat_id} deletes a chat for a given id
@chats_router.delete(
    "/{chat_id}",
    status_code=204,
    response_model=None)
def delete_chat(chat_id: str):
    """

    :param chat_id: the chat id
    :return: nothing
    deletes a chat

    """
    chat = db.get_chat_by_id(chat_id)
    if chat is None:
        error_detail = {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        }
        raise HTTPException(status_code=404, detail=error_detail)
    db.delete_chat(chat_id)


# GET /chats/{chat_id}/messages returns a list of messages for a given chat id
# alongside some metadata.
@chats_router.get(
    "/{chat_id}/messages",
    status_code=200)
def get_messages_for_chat_id(chat_id: str):
    """

    :param chat_id: the chat id
    :return: a list of messages for a chat
    returns a list of messages for a given chat id

    """
    chat = db.get_chat_by_id(chat_id)
    if chat is None:
        error_detail = {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        }
        raise HTTPException(status_code=404, detail=error_detail)
    return MessageCollection(
        meta={"count": 1},
        messages=[]
    )


# GET /chats/{chat_id}/users returns a list of users for a given chat id alongside some metadata. The list of users
# consists of only those users participating in the corresponding chat, sorted by id. The metadata contains the count
# of users (integer). If a chat with the id exists, the response has the HTTP status code 200 and adheres to the format:
@chats_router.get(
    "/{chat_id}/users",
    status_code=200,
)
def get_users_for_chat(chat_id: str) -> UsersInChatResponse:
    """

    :param chat_id: id of the chat
    :return: a list of users in a chat
    returns a list of users for a given chat

    """
    chat = db.get_chat_by_id(chat_id)
    if chat is None:
        error_detail = {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        }
        raise HTTPException(status_code=404, detail=error_detail)

    users = []
    for user_id in sorted(chat.user_ids):
        user = db.get_user_by_id(user_id)
        users.append(user)

    return UsersInChatResponse(
        meta={"count": len(users)},
        users=users,
    )

