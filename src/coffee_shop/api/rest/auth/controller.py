from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from coffee_shop.api.rest.auth.di import auth_service_dependency
from coffee_shop.api.rest.auth.service import AuthService
from coffee_shop.schemas.errors.http import InternalServerError
from coffee_shop.schemas.rest.user import UserCreate, User
from coffee_shop.sqlalchemy_db.di import get_db_session

auth_router = APIRouter(responses={
    500: {
        "model": InternalServerError
    }
})


@auth_router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(request_data: UserCreate, auth_service: AuthService = Depends(auth_service_dependency),
                        session: AsyncSession = Depends(get_db_session)):
    user = await auth_service.register(user_in=request_data, session=session)

    return user
