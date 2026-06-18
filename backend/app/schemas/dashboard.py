from typing import Optional
from uuid import UUID
from datetime import date, datetime

from pydantic import BaseModel

from app.models.enums import LearningPathItemType
from app.schemas.assessment import MasteryRecordRead
from app.schemas.common import CortexSchema


class NextActionRead(CortexSchema):
    learning_path_item_id: UUID
    concept_id: UUID
    concept_name: str
    item_type: LearningPathItemType
    reason: str | None


class DailyActivity(BaseModel):
    date: date
    quizzes_taken: int
    lessons_completed: int
    avg_accuracy: Optional[float] = None


class DashboardOverviewRead(CortexSchema):
    user_id: UUID
    domain_key: str
    total_concepts_mastered: int
    total_concepts_in_domain: int
    overall_progress_percentage: float
    mastery_map: list[MasteryRecordRead]
    weak_areas: list[MasteryRecordRead]
    next_action: Optional[NextActionRead] = None
    current_streak_days: Optional[int] = 0
    last_activity_at: Optional[datetime] = None
    total_xp: Optional[int] = 0
    level: Optional[int] = 0
    badges: Optional[list[str]] = []
    new_badges: Optional[list[str]] = []
