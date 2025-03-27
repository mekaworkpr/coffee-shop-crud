from typing import Any, AsyncGenerator

from coffee_shop.sqlalchemy_db.session import async_session


async def get_db_session() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
