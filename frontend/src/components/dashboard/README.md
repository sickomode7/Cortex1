# Dashboard Components

This directory contains the React components responsible for rendering the Gamification and Analytics features on the learner's dashboard.

## Components

- **`ActivityHeatmap.tsx`**: A GitHub-style contribution graph that visualizes the user's daily activity (quizzes taken, lessons completed) over a rolling 30-day window.
- **`AccuracyTrendChart.tsx`**: An area chart powered by `recharts` that plots the user's average quiz accuracy across the days they were active.
- **`XPBar.tsx`**: A dynamic progress bar indicating the user's current level and visually mapping their experience points (XP) towards the next level requirement.
- **`BadgeShelf.tsx`**: A display container mapping internal backend badge codes (e.g., `first_lesson`, `streak_3`) to visual pills with styled icons and labels.

## Data Flow
These components primarily ingest aggregated data retrieved from the backend `/dashboard/overview` and `/dashboard/activity-history` endpoints. They are highly defensive and gracefully render empty states if data arrays are empty or API calls fail.
