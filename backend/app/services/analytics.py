"""
Analytics Service
=================
Handles user activity tracking, streak calculations, and gamification rewards (XP and Badges).
This service is designed to be highly resilient, safely swallowing exceptions if the gamification 
tables are not yet migrated on the live database.
"""

import logging
import math
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.analytics import Analytics
from app.models.gamification import UserBadge

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service class responsible for tracking learning streaks, computing XP, and awarding badges.
    """

    @staticmethod
    def get_level(total_xp: int) -> int:
        """
        Computes the user's level based on their total XP.
        Formula: level = floor(sqrt(xp / 50))
        
        Args:
            total_xp: The user's total experience points.
            
        Returns:
            An integer representing the current level.
        """
        if total_xp is None:
            return 0
        return math.floor(math.sqrt(total_xp / 50))

    @staticmethod
    def check_and_award_badges(db: Session, user_id: UUID, analytics: Analytics) -> list[str]:
        """
        Evaluates the user's current analytics metrics and awards new badges if milestones are reached.
        
        Args:
            db: The active SQLAlchemy database session.
            user_id: The UUID of the user.
            analytics: The user's Analytics model instance containing their metrics.
            
        Returns:
            A list of badge codes that were newly awarded in this session.
        """
        new_badges = []
        try:
            # Query existing badges gracefully. Will throw if `user_badges` table is missing (pre-migration).
            earned_badges = db.query(UserBadge.badge_code).filter(UserBadge.user_id == user_id).all()
            earned_codes = {b[0] for b in earned_badges}
            
            milestones = []
            
            # Badge: First Lesson
            if analytics.lessons_completed_count >= 1:
                milestones.append("first_lesson")
            
            # Badge: 3-Day Streak
            if analytics.current_streak_days >= 3:
                milestones.append("streak_3")
                
            # Badge: 7-Day Streak
            if analytics.current_streak_days >= 7:
                milestones.append("streak_7")
                
            # Badge: 10 Quizzes Attempted
            if analytics.quizzes_attempted_count >= 10:
                milestones.append("quiz_10")
                
            # Insert any newly earned badges into the database
            for code in milestones:
                if code not in earned_codes:
                    db.add(UserBadge(user_id=user_id, badge_code=code))
                    new_badges.append(code)
                    
        except Exception as e:
            # Safe fallback if tables don't exist yet
            logger.warning(f"Badge check failed (tables might not exist): {e}")

        return new_badges

    @staticmethod
    def record_activity(db: Session, user_id: UUID, activity_type: str) -> None:
        """
        Records a learning activity (quiz or lesson), updates the user's daily streak, 
        grants experience points, and checks for new badge awards.
        
        This method is hooked into the QuizService and LessonService workflows.
        
        Args:
            db: The active SQLAlchemy database session.
            user_id: The UUID of the user performing the activity.
            activity_type: A string identifying the activity type ("quiz" or "lesson").
        """
        try:
            analytics = db.query(Analytics).filter(Analytics.user_id == user_id).first()
            if not analytics:
                return

            now = datetime.utcnow()
            now_date = now.date()
            
            streak_milestone_hit = False
            
            # ---------------------------------------------------------
            # 1. STREAK CALCULATION
            # ---------------------------------------------------------
            if analytics.last_activity_at:
                last_date = analytics.last_activity_at.date()
                if last_date == now_date:
                    # Already active today; do not increment streak again
                    pass
                elif last_date == now_date - timedelta(days=1):
                    # Active yesterday; increment the daily streak
                    analytics.current_streak_days += 1
                    streak_milestone_hit = True
                else:
                    # Gap > 1 day; streak is broken, reset to 1
                    analytics.current_streak_days = 1
                    streak_milestone_hit = True
            else:
                # First ever activity
                analytics.current_streak_days = 1
                streak_milestone_hit = True

            analytics.last_activity_at = now
            
            # ---------------------------------------------------------
            # 2. GAMIFICATION (XP & BONUSES)
            # ---------------------------------------------------------
            # Safely check if the `total_xp` column exists in the database
            if getattr(analytics, 'total_xp', None) is not None:
                
                # Base XP for completing the activity
                if activity_type == "quiz":
                    analytics.total_xp += 5
                elif activity_type == "lesson":
                    analytics.total_xp += 10
                    
                # Streak Milestone Bonus: Award extra XP if they hit a notable streak today
                if streak_milestone_hit and analytics.current_streak_days in (3, 7, 14, 30):
                    analytics.total_xp += 20
            
            # ---------------------------------------------------------
            # 3. BADGES
            # ---------------------------------------------------------
            AnalyticsService.check_and_award_badges(db, user_id, analytics)
            
            db.commit()
            
        except Exception as e:
            # Prevent gamification failures from breaking core curriculum workflows
            logger.warning(f"Streak update failed: {e}")
            db.rollback()
