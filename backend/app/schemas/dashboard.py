from typing import Optional
from uuid import UUID

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


class DashboardOverviewRead(CortexSchema):
    user_id: UUID
    domain_key: str
    total_concepts_mastered: int
    total_concepts_in_domain: int
    overall_progress_percentage: float
    mastery_map: list[MasteryRecordRead]
    weak_areas: list[MasteryRecordRead]
    next_action: Optional[NextActionRead] = None
