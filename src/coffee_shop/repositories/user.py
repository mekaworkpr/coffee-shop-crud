from typing import Union

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from coffee_shop.repositories.base import BaseCRUD
from coffee_shop.sqlalchemy_db.models.user import User


class UserRepository(BaseCRUD):
    model = User

    async def get_by_email(self, email: Union[str, EmailStr], session: AsyncSession):
        result = await session.execute(select(self.model).where(self.model.email == email))
        return result.scalars().first()
