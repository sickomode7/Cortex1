"""
Gamification Models
===================
Defines the database schema for the gamification system, including the `Badge` catalog 
and the `UserBadge` records tracking which users have earned which badges.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base import TimestampMixin, UUIDPrimaryKeyMixin


class Badge(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    Represents a specific badge type available to be earned in the system.
    
    Attributes:
        code (str): A unique string identifier for the badge (e.g., 'streak_3').
        name (str): The human-readable name of the badge (e.g., '3-Day Streak').
        description (str): A detailed explanation of how to earn the badge.
        icon_key (str): A key or emoji representing the visual icon for the badge.
    """
    __tablename__ = "badges"

    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    icon_key: Mapped[str] = mapped_column(String, nullable=False)


class UserBadge(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """
    Represents an instance of a badge earned by a specific user.
    
    Attributes:
        user_id (UUID): Foreign key mapping to the User who earned the badge.
        badge_code (str): The string identifier of the earned badge.
        earned_at (datetime): The UTC timestamp of when the user achieved the badge.
    """
    __tablename__ = "user_badges"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    badge_code: Mapped[str] = mapped_column(String, nullable=False)
    earned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
