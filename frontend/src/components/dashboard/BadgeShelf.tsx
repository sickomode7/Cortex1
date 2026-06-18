import React from "react";

interface BadgeShelfProps {
  badges: string[];
}

const BADGE_INFO: Record<string, { label: string; icon: string }> = {
  "first_lesson": { label: "First Lesson", icon: "🌱" },
  "streak_3": { label: "3-Day Streak", icon: "🔥" },
  "streak_7": { label: "7-Day Streak", icon: "🚀" },
  "quiz_10": { label: "Quiz Master", icon: "🧠" },
};

export function BadgeShelf({ badges }: BadgeShelfProps) {
  if (!badges || badges.length === 0) return null;

  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-sm font-medium">Badges</h3>
      <div className="flex flex-wrap gap-2">
        {badges.map((code) => {
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
