# Backend Models

This directory defines the SQLAlchemy Object-Relational Mapping (ORM) classes that structure the PostgreSQL database for the Cortex application. 

## Domains

- **Gamification (`gamification.py`)**: 
  - `Badge`: The catalog of all available badges in the system (e.g., 3-Day Streak, Quiz Master).
  - `UserBadge`: The bridging table mapping a specific `User` to a specific `Badge` they have earned, including the UTC timestamp of acquisition.

- **Analytics (`analytics.py`)**: 
  - Tracks aggregate user statistics such as `total_xp`, `current_streak_days`, and historical counts (`quizzes_attempted_count`, `lessons_completed_count`). It updates frequently via the `AnalyticsService`.

- **Curriculum & Content**: Defines the core learning items (`Concept`, `Lesson`, `QuizAttempt`) that users interact with.

## Migrations Note
When adding new models or modifying columns, you must use Alembic to generate a migration script (located in `../alembic/versions`). Never modify the database schema directly without version control. All new columns must be `nullable=True` or provide a default value to guarantee backwards compatibility with active clients.
