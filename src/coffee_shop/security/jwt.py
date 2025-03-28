from datetime import timedelta, datetime, timezone

import jwt
from jwt import PyJWTError

from coffee_shop.settings import settings


def create_access_token(
        user_id: int,
        expires_delta: timedelta
) -> str:
    expire = datetime.now(tz=timezone.utc) + expires_delta

    to_encode = {"exp": expire, "user_id": user_id, "type": "access"}

    return jwt.encode(payload=to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(
        user_id: int,
        expires_delta: timedelta
) -> str:
    expire = datetime.now(tz=timezone.utc) + expires_delta

    to_encode = {"exp": expire, "user_id": user_id, "type": "refresh"}

    return jwt.encode(payload=to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_refresh_token(
        token: str
) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])

    if payload.get("type") != "refresh":
        raise PyJWTError("Invalid token type: expected refresh")

    return payload
