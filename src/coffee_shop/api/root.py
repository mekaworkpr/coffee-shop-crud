from fastapi import APIRouter

from coffee_shop.api.rest.auth.controller import auth_router
from coffee_shop.api.websocket.chat import chat_router

root_router = APIRouter(prefix="/api")

root_router.include_router(
    auth_router,
    prefix="/auth"
)

ws_router = APIRouter(prefix="/ws")
ws_router.include_router(chat_router)