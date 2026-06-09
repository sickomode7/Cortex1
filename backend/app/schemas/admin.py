from uuid import UUID
from datetime import datetime
from pydantic import Field
from app.models.enums import DifficultyLevel, QuestionType
from app.schemas.common import CortexSchema


class ConceptCreate(CortexSchema):
    domain_key: str = "python_programming"
    slug: str
    name: str
    description: str | None = None
    concept_order: int
    is_active: bool = True


class ConceptResponse(ConceptCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime


class AdminAssessmentQuestionRead(CortexSchema):
    id: UUID
    concept_id: UUID
    difficulty: DifficultyLevel
    question_type: QuestionType
    prompt: str
    choices: list[str] | None = None
    starter_code: str | None = None
    expected_answer: str | None = None
    explanation: str | None = None
    is_active: bool
    is_approved: bool
    created_at: datetime
    updated_at: datetime


class QuestionApprovalResponse(CortexSchema):
    id: UUID
    is_approved: bool
    message: str
