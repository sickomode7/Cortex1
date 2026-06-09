from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from app.schemas.common import CortexSchema


class UserCreate(CortexSchema):
    email: EmailStr
    full_name: str | None = None
    auth_provider: str | None = None
    auth_subject: str | None = None


class UserRead(CortexSchema):
    id: UUID
    email: EmailStr | None
    full_name: str | None
    auth_provider: str | None
    auth_subject: str | None
    created_at: datetime
    updated_at: datetime

