from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from coffee_shop.settings import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DB_ECHO)

Base = declarative_base()

