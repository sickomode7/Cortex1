from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Badge(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "badges"

    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    icon_key: Mapped[str] = mapped_column(String, nullable=False)


class UserBadge(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "user_badges"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    badge_code: Mapped[str] = mapped_column(String, nullable=False)
    earned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
