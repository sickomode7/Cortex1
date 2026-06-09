from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.assessment import (
    AssessmentSubmissionRequest,
    AssessmentSubmissionResponse,
    AssessmentSessionRead,
    MasteryRecordRead,
)
from app.services.assessment import (
    get_assessment_questions_for_user,
    get_mastery_snapshot_for_user,
    submit_assessment_for_user,
)

router = APIRouter(prefix="/assessment", tags=["assessment"])


@router.get("/users/{user_id}/questions", response_model=AssessmentSessionRead)
def get_assessment_questions_route(
    user_id: UUID,
    limit: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
) -> AssessmentSessionRead:
    return get_assessment_questions_for_user(db, user_id, limit=limit)


@router.post("/users/{user_id}/submit", response_model=AssessmentSubmissionResponse)
def submit_assessment_route(
    user_id: UUID,
    payload: AssessmentSubmissionRequest,
    db: Session = Depends(get_db),
) -> AssessmentSubmissionResponse:
    return submit_assessment_for_user(db, user_id, payload)


@router.get("/users/{user_id}/mastery", response_model=list[MasteryRecordRead])
def get_mastery_snapshot_route(
    user_id: UUID,
    db: Session = Depends(get_db),
) -> list[MasteryRecordRead]:
    return get_mastery_snapshot_for_user(db, user_id)

