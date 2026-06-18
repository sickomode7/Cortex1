# Backend Services

This directory contains the core business logic and service layers for the Cortex application. Services mediate between the API routing layer (`app/api/routes`) and the Database/ORM layer (`app/models`).

## Key Services

- **`AnalyticsService`** (`analytics.py`): The brain behind the gamification system. Hooked directly into the quiz and lesson submission workflows. Responsibilities include:
  - Incrementing and breaking daily streaks based on UTC timestamps.
  - Granting Base XP for completions and Bonus XP for streak milestones (3-day, 7-day, 14-day, 30-day).
  - Checking analytics thresholds (e.g., 10 quizzes taken) to dynamically issue `UserBadge` records.
  - Featuring robust error swallowing (`try/except`) to ensure that missing Gamification database tables do not crash core learning paths.

- **`DashboardService`** (`dashboard.py`): Aggregates user metrics, mastery maps, and badge arrays to efficiently serve the frontend `/dashboard/overview` route in a single call.

- **`LessonService` / `QuizService`**: Handle the primary curriculum progression, validating answers, computing scores, and triggering the `AnalyticsService.record_activity` hooks.
