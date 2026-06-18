"use client";

import React from "react";

/**
 * Represents a single day of user activity.
 */
interface DailyActivity {
  /** ISO date string (YYYY-MM-DD) */
  date: string;
  /** Number of quizzes taken on this day */
  quizzes_taken: number;
  /** Number of lessons successfully completed */
  lessons_completed: number;
  /** The average score of all quizzes taken, or null if none taken */
  avg_accuracy: number | null;
}

interface ActivityHeatmapProps {
  /** Array of daily activities spanning the last 30 days */
  data: DailyActivity[];
}

/**
 * ActivityHeatmap Component
 * 
 * Renders a GitHub-style activity contribution map for the last 30 days.
 * The opacity of each square increases based on the total volume of activities 
 * (quizzes + lessons) completed on that day.
 * 
 * @param {ActivityHeatmapProps} props - The component props containing the daily activity data.
 */
export function ActivityHeatmap({ data }: ActivityHeatmapProps) {
  if (!data || data.length === 0) {
    return <div className="text-muted-foreground italic text-sm">No activity yet.</div>;
  }

  const today = new Date();
  const days = [];
  
  // Generate a list of the past 30 days chronologically
  for (let i = 29; i >= 0; i--) {
    const d = new Date();
    d.setDate(today.getDate() - i);
    days.push(d.toISOString().split("T")[0]);
  }

  // Map dates to activity for fast lookup O(1)
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
          
          // Calculate dynamic opacity based on activity volume
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
