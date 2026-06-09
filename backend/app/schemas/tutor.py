from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import TutorConversationStatus, TutorMessageRole
from app.schemas.common import CortexSchema


class TutorMessageCreate(BaseModel):
    content: str
    referenced_concept_id: UUID | None = None


class TutorMessageRead(CortexSchema):
    id: UUID
    conversation_id: UUID
    referenced_concept_id: UUID | None = None
    role: TutorMessageRole
    content: str
    hint_level: int
    created_at: datetime


class TutorConversationCreate(BaseModel):
    concept_id: UUID | None = None
    learning_path_item_id: UUID | None = None
    initial_message: str | None = None


class TutorConversationRead(CortexSchema):
    id: UUID
    user_id: UUID
    concept_id: UUID | None = None
    learning_path_item_id: UUID | None = None
    status: TutorConversationStatus
    summary: str | None = None
    last_message_at: datetime | None = None
    created_at: datetime
    messages: list[TutorMessageRead] = []
