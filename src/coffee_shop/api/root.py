from fastapi import APIRouter

from coffee_shop.api.rest.test import test_router

root_router = APIRouter(prefix="/api")

root_router.include_router(
    test_router,
    prefix="/test"
)
