from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from coffee_shop.repositories.user import UserRepository
from coffee_shop.schemas.rest.user import UserCreate
from coffee_shop.security.password import get_password_hash
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
