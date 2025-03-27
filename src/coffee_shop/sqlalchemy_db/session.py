from sqlalchemy.ext.asyncio import async_sessionmaker

from coffee_shop.sqlalchemy_db.base import engine

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)
