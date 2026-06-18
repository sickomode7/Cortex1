from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.dashboard import DashboardOverviewRead, DailyActivity
from app.services.dashboard import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverviewRead)
def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve aggregated data for the Learner Dashboard.
    Includes overall progress, mastery map, weak areas, and the next recommended action.
    """
    return DashboardService.get_dashboard_overview(db, current_user.id)

@router.get("/activity-history", response_model=list[DailyActivity])
def get_activity_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a chronologically sorted history of the user's daily learning activities 
    over the last 30 days. This endpoint queries QuizAttempts and Lessons, aggregates 
    them by date, and calculates daily metrics such as 'quizzes taken', 
    'lessons completed', and 'average accuracy'.
    
    This feeds into the frontend Activity Heatmap and Accuracy Trend charts.
    """
    try:
        from datetime import datetime, timedelta
        from collections import defaultdict
        from app.models.content import QuizAttempt, Lesson
        from app.models.enums import LessonStatus

        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        quizzes = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.created_at >= thirty_days_ago
        ).all()
        
        lessons = db.query(Lesson).filter(
            Lesson.user_id == current_user.id,
            Lesson.created_at >= thirty_days_ago,
            Lesson.status == LessonStatus.COMPLETED
        ).all()
        
        daily_stats = defaultdict(lambda: {"quizzes": 0, "lessons": 0, "accuracies": []})
        
        for q in quizzes:
            d = q.created_at.date()
            daily_stats[d]["quizzes"] += 1
            if getattr(q, 'accuracy', None) is not None:
                daily_stats[d]["accuracies"].append(q.accuracy)
                
        for l in lessons:
            d = (l.completed_at or l.created_at).date()
            daily_stats[d]["lessons"] += 1
            
        result = []
        for d, stats in daily_stats.items():
            if stats["quizzes"] > 0 or stats["lessons"] > 0:
                avg_acc = sum(stats["accuracies"]) / len(stats["accuracies"]) if stats["accuracies"] else None
                result.append(DailyActivity(
                    date=d,
                    quizzes_taken=stats["quizzes"],
                    lessons_completed=stats["lessons"],
                    avg_accuracy=avg_acc
                ))
        
        result.sort(key=lambda x: x.date)
        return result
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Failed to fetch activity history: {e}")
        return []
