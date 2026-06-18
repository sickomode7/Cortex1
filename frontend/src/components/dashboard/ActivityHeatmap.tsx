"use client";

import React from "react";

interface DailyActivity {
  date: string;
  quizzes_taken: number;
  lessons_completed: number;
  avg_accuracy: number | null;
}

interface ActivityHeatmapProps {
  data: DailyActivity[];
}

export function ActivityHeatmap({ data }: ActivityHeatmapProps) {
  if (!data || data.length === 0) {
    return <div className="text-muted-foreground italic text-sm">No activity yet.</div>;
  }

  const today = new Date();
  const days = [];
  for (let i = 29; i >= 0; i--) {
    const d = new Date();
    d.setDate(today.getDate() - i);
    days.push(d.toISOString().split("T")[0]);
  }

  const dataMap = new Map(data.map((d) => [d.date, d]));

  return (
    <div className="flex flex-col gap-2">
      <h3 className="text-sm font-medium">Activity (30 Days)</h3>
      <div className="flex flex-wrap gap-1">
        {days.map((day) => {
          const activity = dataMap.get(day);
          const isActive = !!activity && (activity.quizzes_taken > 0 || activity.lessons_completed > 0);
          
          let opacity = 0.1;
          let label = `${day}: No activity`;
          if (isActive) {
            const total = activity.quizzes_taken + activity.lessons_completed;
            opacity = Math.min(0.2 + total * 0.2, 1.0);
            label = `${day}: ${activity.quizzes_taken} quizzes, ${activity.lessons_completed} lessons`;
          }

          return (
            <div
              key={day}
              title={label}
              className={`w-4 h-4 rounded-sm ${isActive ? 'bg-primary' : 'bg-muted'}`}
              style={isActive ? { opacity } : {}}
            />
          );
        })}
      </div>
    </div>
  );
}
