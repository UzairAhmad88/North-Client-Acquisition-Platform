"use client";

import React from "react";

interface ScoreBadgeProps {
  score: number;
  band: "HIGH" | "MEDIUM" | "LOW" | "VERY_LOW" | string;
  size?: "sm" | "md" | "lg";
}

export function ScoreBadge({ score, band, size = "md" }: ScoreBadgeProps) {
  const getBandStyles = (b: string) => {
    switch (b) {
      case "HIGH":
        return "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200";
      case "MEDIUM":
        return "bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border-blue-200";
      case "LOW":
        return "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-200";
      default:
        return "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300 border-gray-200";
    }
  };

  const roundedScore = Math.round(score);

  if (size === "sm") {
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-0.5 text-[11px] font-bold rounded-md border ${getBandStyles(band)}`}>
        <span>{roundedScore}</span>
        <span className="text-[9px] opacity-75">({band})</span>
      </span>
    );
  }

  if (size === "lg") {
    return (
      <div className={`p-4 rounded-2xl border flex items-center gap-4 ${getBandStyles(band)}`}>
        <div className="text-3xl font-black">{roundedScore}</div>
        <div>
          <div className="text-xs font-bold uppercase tracking-wider">Opportunity Priority</div>
          <div className="text-sm font-semibold mt-0.5">{band} PRIORITY BAND</div>
        </div>
      </div>
    );
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-bold rounded-lg border ${getBandStyles(band)}`}>
      <span className="text-sm">{roundedScore}</span>
      <span>{band}</span>
    </span>
  );
}
