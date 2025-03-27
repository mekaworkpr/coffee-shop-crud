from fastapi import APIRouter

from coffee_shop.api.rest.auth.controller import auth_router

root_router = APIRouter(prefix="/api")

root_router.include_router(
    auth_router,
    prefix="/auth"
)
