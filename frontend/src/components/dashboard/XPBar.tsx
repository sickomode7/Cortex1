import React from "react";

interface XPBarProps {
  level: number;
  total_xp: number;
}

export function XPBar({ level, total_xp }: XPBarProps) {
  const currentLevelXP = Math.pow(level, 2) * 50;
  const nextLevelXP = Math.pow(level + 1, 2) * 50;
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
      <div className="h-3 w-full bg-muted rounded-full overflow-hidden">
        <div 
          className="h-full bg-primary transition-all duration-500 ease-out" 
          style={{ width: `${progress}%` }} 
        />
      </div>
    </div>
  );
}
