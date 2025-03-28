from typing import Union, Optional

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from coffee_shop.repositories.base import BaseCRUD
from coffee_shop.security.password import verify_password
from coffee_shop.sqlalchemy_db.models.user import User


class UserRepository(BaseCRUD):
    model = User

    async def get_by_email(self, email: Union[str, EmailStr], session: AsyncSession):
        result = await session.execute(select(self.model).where(self.model.email == email))
        return result.scalars().first()

    async def authenticate(self, session: AsyncSession, email: Union[str, EmailStr], password: str) -> Optional[User]:
        user = await self.get_by_email(email, session)

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        return user

