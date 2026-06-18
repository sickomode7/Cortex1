import React from "react";

interface XPBarProps {
  /** The current integer level of the user */
  level: number;
  /** The total absolute XP the user has accumulated since onboarding */
  total_xp: number;
}

/**
 * XPBar Component
 * 
 * Renders a progress bar indicating how far the user has progressed within their current level.
 * Level requirements scale quadratically (level^2 * 50).
 * 
 * @param {XPBarProps} props - The level and absolute total_xp metrics.
 */
export function XPBar({ level, total_xp }: XPBarProps) {
  // Quadratic scaling formula matching the backend analytics.py calculation
  const currentLevelXP = Math.pow(level, 2) * 50;
  const nextLevelXP = Math.pow(level + 1, 2) * 50;
  
  // Calculate the percentage filled from current level baseline to next level requirement
  const progress = Math.min(100, Math.max(0, ((total_xp - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100));

  return (
    <div className="flex flex-col gap-2 w-full">
      <div className="flex justify-between items-end">
        <div>
          <span className="text-2xl font-bold text-primary">Level {level}</span>
        </div>
        <div className="text-sm text-muted-foreground">
          {total_xp} / {nextLevelXP} XP
        </div>
      </div>
      {/* Container for the progress track */}
      <div className="h-3 w-full bg-muted rounded-full overflow-hidden">
        {/* Animated fill representing percentage progress */}
        <div 
          className="h-full bg-primary transition-all duration-500 ease-out" 
          style={{ width: `${progress}%` }} 
        />
      </div>
    </div>
  );
}
