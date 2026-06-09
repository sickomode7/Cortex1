from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.quiz import QuizAttemptResult, QuizAttemptSubmission, QuizCreate, QuizRead
from app.services.quiz import QuizService

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("/generate", response_model=QuizRead)
def generate_quiz(
    req: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a quiz for a concept, drawing from the pre-seeded question bank.
    """
    quiz, questions = QuizService.generate_quiz(db, current_user.id, req)
    
    return QuizRead(
        id=quiz.id,
        user_id=quiz.user_id,
        concept_id=quiz.concept_id,
        learning_path_item_id=quiz.learning_path_item_id,
        title=quiz.title,
        quiz_type=quiz.quiz_type,
        question_count=quiz.question_count,
        questions=questions,
        created_at=quiz.created_at,
    )


@router.post("/{quiz_id}/submit", response_model=QuizAttemptResult)
def submit_quiz(
    quiz_id: UUID,
    submission: QuizAttemptSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit answers for a quiz.
    This deterministically grades the quiz and updates the Learner's Mastery Record.
    """
    return QuizService.submit_quiz(db, current_user.id, quiz_id, submission)
