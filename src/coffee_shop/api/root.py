from fastapi import APIRouter

from coffee_shop.api.rest.auth.controller import auth_router
from coffee_shop.api.rest.user.controller import user_router
from coffee_shop.api.websocket.chat import chat_router

root_router = APIRouter(prefix="/api")

root_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)
root_router.include_router(
    user_router,
    prefix="/user",
    tags=["User"]
)

ws_router = APIRouter(prefix="/ws")
ws_router.include_router(chat_router)