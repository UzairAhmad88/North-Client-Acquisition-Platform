"use client";

import React from "react";

interface RecommendationBadgeProps {
  score: number;
  band: "STRONG" | "GOOD" | "POSSIBLE" | "WEAK" | string;
  priority?: "HIGH" | "MEDIUM" | "LOW" | string;
  confidence?: "HIGH" | "MEDIUM" | "LOW" | string;
  status?: "SUGGESTED" | "REVIEWED" | "ACCEPTED" | "REJECTED" | "STALE" | string;
  size?: "sm" | "md";
}

export function RecommendationBadge({
  score,
  band,
  priority,
  confidence,
  status,
  size = "md",
}: RecommendationBadgeProps) {
  const getBandStyles = (b: string) => {
    switch (b) {
      case "STRONG":
        return "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-200";
      case "GOOD":
        return "bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border-blue-200";
      case "POSSIBLE":
        return "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-200";
      default:
        return "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300 border-gray-200";
    }
  };

  const getStatusStyles = (s: string) => {
    switch (s) {
      case "ACCEPTED":
        return "bg-green-600 text-white";
      case "REJECTED":
        return "bg-red-600 text-white";
      case "STALE":
        return "bg-amber-500 text-white";
      default:
        return "bg-slate-700 text-white";
    }
  };

  const roundedScore = Math.round(score);

  if (size === "sm") {
    return (
      <div className="flex items-center gap-1.5 flex-wrap">
        <span className={`inline-flex items-center gap-1 px-2 py-0.5 text-[11px] font-bold rounded-md border ${getBandStyles(band)}`}>
          <span>{roundedScore}</span>
          <span className="text-[9px] opacity-75">({band})</span>
        </span>
        {status && (
          <span className={`inline-flex items-center px-1.5 py-0.5 text-[10px] font-semibold rounded ${getStatusStyles(status)}`}>
            {status}
          </span>
        )}
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2 flex-wrap">
      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-bold rounded-lg border ${getBandStyles(band)}`}>
        <span className="text-sm font-black">{roundedScore}</span>
        <span>{band} RELEVANCE</span>
      </span>
      {priority && (
        <span className="px-2 py-0.5 text-xs font-semibold rounded bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300 border border-purple-200">
          {priority} PRIORITY
        </span>
      )}
      {confidence && (
        <span className="px-2 py-0.5 text-xs font-medium rounded bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
          {confidence} CONFIDENCE
        </span>
      )}
      {status && (
        <span className={`px-2 py-0.5 text-xs font-bold rounded ${getStatusStyles(status)}`}>
          {status}
        </span>
      )}
    </div>
  );
}
