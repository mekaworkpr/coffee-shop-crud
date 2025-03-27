import uvicorn

from coffee_shop.settings import settings


def main():
    uvicorn.run(
        "coffee_shop.main.web:create_app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        workers=settings.UVICORN_WORKERS_COUNT,
        reload=settings.UVICORN_RELOAD,
        log_level=settings.LOG_LEVER.value.lower(),
        factory=True
    )

if __name__ == "__main__":
    main()
