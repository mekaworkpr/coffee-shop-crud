import logging
from abc import ABCMeta
from typing import TypeVar, Any, Sequence

import sqlalchemy
from sqlalchemy import select, update, exists, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from coffee_shop.sqlalchemy_db.base import Base

logger = logging.getLogger(__name__)

SqlaModelType = TypeVar("SqlaModelType", bound=Base)


class BaseCRUD(metaclass=ABCMeta):
    model: SqlaModelType = SqlaModelType

    @staticmethod
    def set_limit_and_offset(query: sqlalchemy.Select, limit: int | None = None,
                             offset: int | None = None) -> sqlalchemy.Select:
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        return query

    @staticmethod
    def set_order_by(query: sqlalchemy.Select, by: list | None = None) -> sqlalchemy.Select:
        if by:
            query = query.order_by(*by)

        return query

    @staticmethod
    def set_options(query: sqlalchemy.Select, options: list | None = None) -> sqlalchemy.Select:
        if options:
            query = query.options(*options)

        return query

    async def prepare_record(self, record):
        pass

    async def get_by_pk(self, pk: Any, pk_name: str, session: AsyncSession) -> model:
        return await self.get(
            filters=[getattr(self.model, pk_name) == pk], session=session
        )

    async def get(self, filters: list, order_by: list | None = None, options: list | None = None,
                  session: AsyncSession = None) -> model:
        query = select(self.model).where(*filters)

        query = self.set_order_by(query=query, by=order_by)
        query = self.set_options(query=query, options=options)
        query = self.set_limit_and_offset(query=query, limit=1)

        result = await session.execute(query)

        return result.scalar()

    async def get_list(self, filters: list, limit: int | None = None,
                       offset: int | None = None, order_by: list | None = None,
                       options: list | None = None, session: AsyncSession = None) -> Sequence[model]:
        query = select(self.model).where(*filters)

        query = self.set_limit_and_offset(query=query, limit=limit, offset=offset)
        query = self.set_order_by(query=query, by=order_by)
        query = self.set_options(query=query, options=options)

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def add_obj(obj: model, session: AsyncSession = None) -> model:
        session.add(obj)
        logger.debug(f"BaseCRUD.create_by_obj: {obj}")
        return obj

    async def add(self, session: AsyncSession = None, **fields) -> model:
        obj = self.model(**fields)
        session.add(obj)
        logger.debug(f"BaseCRUD.create model: {self.model} obj: {obj}")

        return obj

    async def update(self, filters: list, data: dict, session: AsyncSession = None) -> Sequence[model]:
        query = update(self.model).where(*filters).values(**data).returning(self.model)
        result = await session.execute(query)
        r_all = result.scalars().all()

        logger.debug(f"BaseCRUD.update model: {self.model} data: {data} result: {r_all}")

        return r_all

    async def update_by_pk(self, pk: Any, pk_name: str, data: dict, session: AsyncSession = None) -> model:
        query = update(self.model).where(getattr(self.model, pk_name) == pk).values(**data).returning(self.model)
        rq = await session.execute(query)
        result = rq.scalar()

        logger.debug(f"BaseCRUD.update_by_pk model: {self.model} data: {data} result: {result}")

        return result

    async def exists(self, filters: list, session: AsyncSession = None) -> bool:
        model_db = exists(self.model).where(and_(*filters)).select()
        result = await session.execute(model_db)

        return bool(result.scalar())

    async def count(self, pk_name: str, filters: list, session: AsyncSession = None) -> int:
        query = select(func.count(getattr(self.model, pk_name)).label('count')).where(*filters)
        rq = await session.execute(query)

        return rq.fetchone().count
