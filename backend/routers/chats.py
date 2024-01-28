from datetime import date
from typing import Literal

from fastapi import APIRouter

from backend import database as db

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("/chats")
def get_chats():
    pass
