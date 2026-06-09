from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.models.enums import DifficultyLevel, QuestionType
from app.schemas.common import CortexSchema


class AssessmentQuestionRead(CortexSchema):
    id: UUID
    concept_id: UUID
    concept_slug: str
    concept_name: str
    difficulty: DifficultyLevel
    question_type: QuestionType
    prompt: str
    choices: list[str] | None = None
    starter_code: str | None = None


class AssessmentSessionRead(CortexSchema):
    user_id: UUID
    domain_key: str
    question_count: int
    questions: list[AssessmentQuestionRead]


class AssessmentAnswerSubmission(CortexSchema):
    question_id: UUID
    answer: str = Field(min_length=1)


class AssessmentSubmissionRequest(CortexSchema):
    answers: list[AssessmentAnswerSubmission]


class AssessmentResultRead(CortexSchema):
    question_id: UUID
    concept_id: UUID
    concept_slug: str
    concept_name: str
    difficulty: DifficultyLevel
    question_type: QuestionType
    answer: str
    expected_answer: str | None
    is_correct: bool
    score: float
    explanation: str | None
    assessed_at: datetime


class MasteryRecordRead(CortexSchema):
    concept_id: UUID
    concept_slug: str
    concept_name: str
    mastery_score: float
    quiz_accuracy: float
    practice_accuracy: float
    consistency_score: float
    confidence: float
    evidence_summary: str | None
    last_evaluated_at: datetime | None


class AssessmentSubmissionResponse(CortexSchema):
    user_id: UUID
    total_questions: int
    correct_answers: int
    overall_score: float
    results: list[AssessmentResultRead]
    mastery: list[MasteryRecordRead]

