from datetime import timedelta
from typing import Union, Optional

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from coffee_shop.repositories.user import UserRepository
from coffee_shop.schemas.rest.auth import Token
from coffee_shop.schemas.rest.user import UserCreate
from coffee_shop.security.jwt import create_access_token, create_refresh_token
from coffee_shop.security.password import get_password_hash, verify_password
from coffee_shop.settings import settings
from coffee_shop.sqlalchemy_db.models.user import User


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        # self.email_service = EmailService() # Если бы был EmailService

    async def register(self, user_in: UserCreate, session: AsyncSession):
        user = await self.user_repository.get_by_email(user_in.email, session)

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = get_password_hash(user_in.password)

        user_data = user_in.model_dump(exclude={"password"})

        user = User(**user_data, hashed_password=hashed_password)

        await self.user_repository.add_obj(user, session)
        await session.commit()
        await session.refresh(user)

        return user


    async def login(self, session: AsyncSession, email: Union[str, EmailStr], password: str) -> Token:
        user = await self.user_repository.authenticate(session, email=email, password=password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        elif not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(user_id=user.id, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(user_id=user.id, expires_delta=refresh_token_expires)

        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

