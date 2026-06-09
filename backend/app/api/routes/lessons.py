from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.lesson import LessonCreate, LessonComplete, LessonResponse
from app.services.lesson import LessonService

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.post("/generate", response_model=LessonResponse)
def generate_lesson(
    req: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a new lesson for a specific concept, tailored to the learner's profile.
    """
    return LessonService.generate_lesson(
        db=db,
        user_id=current_user.id,
        concept_id=req.concept_id,
        learning_path_item_id=req.learning_path_item_id,
    )


@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve an existing lesson.
    """
    return LessonService.get_lesson(db=db, lesson_id=lesson_id, user_id=current_user.id)


@router.post("/{lesson_id}/complete", response_model=LessonResponse)
def complete_lesson(
    lesson_id: UUID,
    req: LessonComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mark a lesson as completed. This will also update the associated learning path item.
    """
    if not req.completed:
        return LessonService.get_lesson(db=db, lesson_id=lesson_id, user_id=current_user.id)
        
    return LessonService.complete_lesson(db=db, lesson_id=lesson_id, user_id=current_user.id)
