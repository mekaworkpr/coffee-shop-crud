import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jwt import PyJWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from coffee_shop.repositories.user import UserRepository
from coffee_shop.schemas.rest.auth import TokenPayload
from coffee_shop.settings import settings
from coffee_shop.sqlalchemy_db.di import get_db_session
from coffee_shop.sqlalchemy_db.models.user import User

bearer_header = HTTPBearer()


async def get_current_user(
        session: AsyncSession = Depends(get_db_session),
        token = Depends(bearer_header)
) -> User:
    print(token)
    try:
        payload = jwt.decode(
            token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user_repository = UserRepository()
    user = await user_repository.get_by_pk(pk=token_data.user_id, pk_name="id", session=session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return current_user


async def get_current_active_superuser(
        current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user
