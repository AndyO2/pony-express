from fastapi import APIRouter

users_router = APIRouter(prefix="/users", tags=["Users"])


# GET /users returns a list of users sorted by id alongside some metadata. The metadata has the count of users (
# integer). The response has HTTP status code 200 and adheres to the following format:
@users_router.get("/users")
def get_users():
    pass


# POST /users creates a new user. The body of the request adheres to the format:
@users_router.post("/users")
def create_user():
    pass


# GET /users/{user_id} returns a user for a given id. If a user with the id exists, the response has status code 200
# and adheres to the format:
@users_router.get("users/{user_id}")
def get_user(user_id: str):
    pass


# GET /users/{user_id}/chats returns a list of chats for a given user id alongside some metadata.
@users_router.get("/users/{user_id}/chats")
def get_chats_for_user(user_id: str):
    pass
