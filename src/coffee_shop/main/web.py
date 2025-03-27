from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from coffee_shop.main.routers import init_routers
from coffee_shop.settings import settings


def create_app(*args, **kwargs):
    title_prefix = f"[{settings.ENVIRONMENT.upper()}]" if settings.ENVIRONMENT != "prod" else ""
    title = f"{title_prefix} {settings.PROJECT_NAME}"

    app = FastAPI(
        title=title,
        default_response_class=ORJSONResponse
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_routers(app)

    return app