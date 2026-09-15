"use client";

import React from "react";
import { Sparkles, RefreshCw } from "lucide-react";

interface DashboardHeaderProps {
  userName?: string | null;
  onRefresh?: () => void;
  isRefreshing?: boolean;
}

export function DashboardHeader({ userName, onRefresh, isRefreshing }: DashboardHeaderProps) {
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
  };

  const displayName = userName || "Operator";

  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-200">
      <div>
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#7c3aed]">
          <Sparkles className="w-4 h-4 text-[#8b5cf6]" />
          <span>Operational Command Center</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1 tracking-tight">
          {getGreeting()}, <span className="text-[#0f4c3a]">{displayName}</span>
        </h1>
        <p className="text-sm text-slate-500 mt-0.5 font-medium">
          Real-time business intelligence, project execution, and autonomous AI fleet state.
        </p>
      </div>

      {onRefresh && (
        <button
          onClick={onRefresh}
          disabled={isRefreshing}
          className="inline-flex items-center gap-2 px-3.5 py-2 text-xs font-semibold text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors disabled:opacity-50 shadow-2xs self-start sm:self-auto cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 text-[#0f4c3a] ${isRefreshing ? "animate-spin" : ""}`} />
          <span>{isRefreshing ? "Refreshing..." : "Refresh Intelligence"}</span>
        </button>
      )}
    </div>
  );
}
