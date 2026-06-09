from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import LessonStatus

class LessonBase(BaseModel):
    title: str
    status: LessonStatus
    content_payload: dict[str, Any]
    personalization_context: dict[str, Any] | None = None

class LessonCreate(BaseModel):
    concept_id: UUID
    learning_path_item_id: UUID | None = None

class LessonResponse(LessonBase):
    id: UUID
    user_id: UUID
    concept_id: UUID
    learning_path_item_id: UUID | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LessonComplete(BaseModel):
    completed: bool = True
