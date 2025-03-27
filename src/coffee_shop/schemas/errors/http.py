from pydantic import BaseModel


class NotAuthorizedError(BaseModel):
    detail: str = "Not authorized"


class NotAuthenticatedError(BaseModel):
    detail: str = "Not authenticated"


class InternalServerError(BaseModel):
    detail: str = "Internal server error"
