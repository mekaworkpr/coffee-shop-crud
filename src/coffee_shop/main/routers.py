from fastapi import FastAPI

from coffee_shop.api.root import root_router, ws_router


def init_routers(app: FastAPI):
    app.include_router(root_router)
    app.include_router(ws_router)