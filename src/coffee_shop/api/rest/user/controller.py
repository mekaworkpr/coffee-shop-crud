from fastapi import APIRouter, Depends

from coffee_shop.api.deps import get_current_active_user, get_current_active_superuser
from coffee_shop.schemas.rest.user import User

user_router = APIRouter()


@user_router.get("/me/", response_model=User)
async def get_user_me(
        current_user: User = Depends(get_current_active_user)
):
    return current_user


@user_router.get("/admin/me/", response_model=User)
async def get_admin_me(
        current_admin: User = Depends(get_current_active_superuser)
):
    return current_admin
