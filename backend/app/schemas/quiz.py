from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import QuizType
from app.schemas.assessment import AssessmentAnswerSubmission, AssessmentQuestionRead
from app.schemas.common import CortexSchema


class QuizCreate(CortexSchema):
    concept_id: UUID
    learning_path_item_id: UUID | None = None
    quiz_type: QuizType = QuizType.MASTERY_CHECK
    question_count: int = 6


class QuizRead(CortexSchema):
    id: UUID
    user_id: UUID
    concept_id: UUID
    learning_path_item_id: UUID | None = None
    title: str
    quiz_type: QuizType
    question_count: int
    questions: list[AssessmentQuestionRead] = []
    created_at: datetime


class QuizAttemptSubmission(CortexSchema):
    answers: list[AssessmentAnswerSubmission]


class QuizAttemptResult(CortexSchema):
    id: UUID
    quiz_id: UUID
    user_id: UUID
    score: float
    accuracy: float
    submitted_answers: dict
    feedback_payload: dict
    completed_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
