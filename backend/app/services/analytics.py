import logging
import math
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.analytics import Analytics
from app.models.gamification import UserBadge

logger = logging.getLogger(__name__)

class AnalyticsService:

    @staticmethod
    def get_level(total_xp: int) -> int:
        if total_xp is None:
            return 0
        return math.floor(math.sqrt(total_xp / 50))

    @staticmethod
    def check_and_award_badges(db: Session, user_id: UUID, analytics: Analytics) -> list[str]:
        new_badges = []
        try:
            # Query existing badges gracefully
            earned_badges = db.query(UserBadge.badge_code).filter(UserBadge.user_id == user_id).all()
            earned_codes = {b[0] for b in earned_badges}
            
            milestones = []
            if analytics.lessons_completed_count >= 1:
                milestones.append("first_lesson")
            
            if analytics.current_streak_days >= 3:
                milestones.append("streak_3")
            if analytics.current_streak_days >= 7:
                milestones.append("streak_7")
                
            if analytics.quizzes_attempted_count >= 10:
                milestones.append("quiz_10")
                
            for code in milestones:
                if code not in earned_codes:
                    db.add(UserBadge(user_id=user_id, badge_code=code))
                    new_badges.append(code)
        except Exception as e:
            logger.warning(f"Badge check failed (tables might not exist): {e}")

        return new_badges

    @staticmethod
    def record_activity(db: Session, user_id: UUID, activity_type: str) -> None:
        try:
            analytics = db.query(Analytics).filter(Analytics.user_id == user_id).first()
            if not analytics:
                return

            now = datetime.utcnow()
            now_date = now.date()
            
            streak_milestone_hit = False
            
            if analytics.last_activity_at:
                last_date = analytics.last_activity_at.date()
                if last_date == now_date:
                    pass
                elif last_date == now_date - timedelta(days=1):
                    analytics.current_streak_days += 1
                    streak_milestone_hit = True
                else:
                    analytics.current_streak_days = 1
                    streak_milestone_hit = True
            else:
                analytics.current_streak_days = 1
                streak_milestone_hit = True

            analytics.last_activity_at = now
            
            # Gamification
            if getattr(analytics, 'total_xp', None) is not None:
                if activity_type == "quiz":
                    analytics.total_xp += 5
                elif activity_type == "lesson":
                    analytics.total_xp += 10
                    
                if streak_milestone_hit and analytics.current_streak_days in (3, 7, 14, 30):
                    analytics.total_xp += 20
            
            AnalyticsService.check_and_award_badges(db, user_id, analytics)
            
            db.commit()
        except Exception as e:
            logger.warning(f"Streak update failed: {e}")
            db.rollback()
