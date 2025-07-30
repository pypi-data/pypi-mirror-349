import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Schema for reading user data."""

    full_name: str | None = None


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating a new user."""

    full_name: str | None = None


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating user data."""

    full_name: str | None = None
