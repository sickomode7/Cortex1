"use client";

import React from "react";
import { Area, AreaChart, ResponsiveContainer, Tooltip as RechartsTooltip, XAxis, YAxis } from "recharts";

/**
 * Represents daily accuracy data point for charting.
 */
interface DailyActivity {
  /** ISO date string (YYYY-MM-DD) */
  date: string;
  /** The average score of all quizzes taken, or null if none taken */
  avg_accuracy: number | null;
}

interface AccuracyTrendChartProps {
  /** Array of daily activities containing accuracy metrics */
  data: DailyActivity[];
}

/**
 * AccuracyTrendChart Component
 * 
 * Renders an AreaChart plotting the user's average quiz accuracy over time.
 * Filters out days where no quizzes were taken (accuracy is null).
 * Built on top of Recharts library for responsive SVG graphs.
 * 
 * @param {AccuracyTrendChartProps} props - The component props containing the daily accuracy data.
 */
export function AccuracyTrendChart({ data }: AccuracyTrendChartProps) {
  if (!data || data.length === 0) return null;

  // Filter out days without accuracy data and format as percentages (0-100)
  const chartData = data
    .filter((d) => d.avg_accuracy !== null)
    .map((d) => ({
      date: d.date,
      accuracy: Math.round(d.avg_accuracy! * 100),
    }));

  if (chartData.length === 0) return null;

  return (
    <div className="flex flex-col gap-2 h-48">
      <h3 className="text-sm font-medium">Accuracy Trend</h3>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 5, right: 0, left: -20, bottom: 0 }}>
          <XAxis dataKey="date" hide />
          <YAxis domain={[0, 100]} hide />
          {/* Custom tooltip styled using CSS variables to support Dark Mode toggle */}
          <RechartsTooltip 
            contentStyle={{ backgroundColor: 'hsl(var(--background))', borderColor: 'hsl(var(--border))' }}
            itemStyle={{ color: 'hsl(var(--foreground))' }}
          />
          <Area
            type="monotone"
            dataKey="accuracy"
            stroke="hsl(var(--primary))"
            fill="hsl(var(--primary))"
            fillOpacity={0.2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
