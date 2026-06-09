from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.curriculum import CurriculumPlanResponse, LearningPathRead
from app.services.curriculum import generate_learning_path_for_user, get_active_learning_path_for_user

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


@router.post("/users/{user_id}/generate", response_model=CurriculumPlanResponse)
def generate_learning_path_route(
    user_id: UUID,
    db: Session = Depends(get_db),
) -> CurriculumPlanResponse:
    return generate_learning_path_for_user(db, user_id)


@router.get("/users/{user_id}/active-path", response_model=LearningPathRead)
def get_active_learning_path_route(
    user_id: UUID,
    db: Session = Depends(get_db),
) -> LearningPathRead:
    return get_active_learning_path_for_user(db, user_id)


@router.post("/users/{user_id}/adapt", response_model=CurriculumPlanResponse)
def adapt_learning_path_route(
    user_id: UUID,
    db: Session = Depends(get_db),
) -> CurriculumPlanResponse:
    """
    Force an adaptive replanning of the user's active path based on current mastery levels.
    """
    from app.services.curriculum import adapt_learning_path_for_user
    return adapt_learning_path_for_user(db, user_id)

