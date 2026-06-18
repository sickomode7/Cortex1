import React from "react";

interface BadgeShelfProps {
  /** Array of string badge codes (e.g., 'first_lesson', 'streak_3') representing the badges the user has earned */
  badges: string[];
}

/** 
 * Static configuration mapping internal badge codes to human-readable labels and emoji icons.
 * This ensures the frontend defines the presentation logic while the backend manages state.
 */
const BADGE_INFO: Record<string, { label: string; icon: string }> = {
  "first_lesson": { label: "First Lesson", icon: "🌱" },
  "streak_3": { label: "3-Day Streak", icon: "🔥" },
  "streak_7": { label: "7-Day Streak", icon: "🚀" },
  "quiz_10": { label: "Quiz Master", icon: "🧠" },
};

/**
 * BadgeShelf Component
 * 
 * Displays a flex-wrap container showing all the gamification badges a user has unlocked.
 * Automatically maps raw backend badge codes into styled pills with icons.
 * 
 * @param {BadgeShelfProps} props - The array of badge codes assigned to the current user.
 */
export function BadgeShelf({ badges }: BadgeShelfProps) {
  // Gracefully hide the component if the user hasn't earned any badges yet
  if (!badges || badges.length === 0) return null;

  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-sm font-medium">Badges</h3>
      <div className="flex flex-wrap gap-2">
        {badges.map((code) => {
          // Fallback to a generic star and raw code if the badge isn't in our predefined map
          const info = BADGE_INFO[code] || { label: code, icon: "⭐" };
          return (
            <div 
              key={code} 
              className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-secondary text-secondary-foreground text-xs font-medium border border-border"
              title={info.label}
            >
              <span>{info.icon}</span>
              <span>{info.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
