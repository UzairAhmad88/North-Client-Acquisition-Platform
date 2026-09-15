"use client";

import React from "react";

export function DashboardSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Header skeleton */}
      <div className="h-16 bg-gray-200 dark:bg-gray-800 rounded-xl" />

      {/* KPI Cards skeleton */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-32 bg-gray-200 dark:bg-gray-800 rounded-xl" />
        ))}
      </div>

      {/* Attention skeleton */}
      <div className="h-40 bg-gray-200 dark:bg-gray-800 rounded-xl" />

      {/* Pipeline skeleton */}
      <div className="h-36 bg-gray-200 dark:bg-gray-800 rounded-xl" />

      {/* Grid skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="h-64 bg-gray-200 dark:bg-gray-800 rounded-xl" />
        <div className="h-64 bg-gray-200 dark:bg-gray-800 rounded-xl" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="h-64 bg-gray-200 dark:bg-gray-800 rounded-xl" />
        <div className="h-64 bg-gray-200 dark:bg-gray-800 rounded-xl" />
      </div>
    </div>
  );
}
