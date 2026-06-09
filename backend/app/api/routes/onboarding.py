from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.onboarding import LearnerOnboardingResponse, LearnerProfileRead, LearnerProfileUpsert
from app.schemas.users import UserRead
from app.services.onboarding import get_profile_or_404, get_user_or_404, upsert_learner_profile

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.put("/users/{user_id}/profile", response_model=LearnerOnboardingResponse)
def upsert_learner_profile_route(
    user_id: UUID,
    payload: LearnerProfileUpsert,
    db: Session = Depends(get_db),
) -> LearnerOnboardingResponse:
    profile = upsert_learner_profile(db, user_id, payload)
    user = get_user_or_404(db, user_id)
    return LearnerOnboardingResponse(
        user=UserRead.model_validate(user),
        learner_profile=LearnerProfileRead.model_validate(profile),
    )


@router.get("/users/{user_id}/profile", response_model=LearnerOnboardingResponse)
def get_learner_profile_route(
    user_id: UUID,
    db: Session = Depends(get_db),
) -> LearnerOnboardingResponse:
    user = get_user_or_404(db, user_id)
    profile = get_profile_or_404(db, user_id)
    return LearnerOnboardingResponse(
        user=UserRead.model_validate(user),
        learner_profile=LearnerProfileRead.model_validate(profile),
    )


@router.get("/domains", response_model=list[str])
def list_supported_domains() -> list[str]:
    return ["python_programming"]

