"use client";

import React from "react";
import Link from "next/link";
import { Layers, ArrowRight, Star } from "lucide-react";
import { ServiceSummary } from "@/lib/api/dashboard";

interface ServiceSnapshotCardProps {
  services: ServiceSummary;
}

export function ServiceSnapshotCard({ services }: ServiceSnapshotCardProps) {
  const categoryEntries = Object.entries(services.category_counts || {});

  return (
    <div className="p-6 rounded-xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            <h2 className="text-base font-bold text-gray-900 dark:text-gray-100">
              Service Catalog Overview
            </h2>
          </div>
          <Link
            href="/services"
            className="text-xs font-medium text-purple-600 dark:text-purple-400 hover:underline flex items-center gap-1"
          >
            <span>Manage Catalog</span>
            <ArrowRight className="w-3 h-3" />
          </Link>
        </div>

        <div className="grid grid-cols-2 gap-3 mt-4">
          <div className="p-3 rounded-lg bg-purple-50 dark:bg-purple-950/30 border border-purple-200 dark:border-purple-900/40">
            <span className="text-xs text-purple-700 dark:text-purple-300 font-semibold block">
              Active Offerings
            </span>
            <span className="text-2xl font-extrabold text-purple-900 dark:text-purple-100 mt-1 block">
              {services.active_services_count}
            </span>
          </div>

          <div className="p-3 rounded-lg bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/40">
            <div className="flex items-center gap-1 text-xs text-amber-700 dark:text-amber-300 font-semibold">
              <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
              <span>Featured</span>
            </div>
            <span className="text-2xl font-extrabold text-amber-900 dark:text-amber-100 mt-1 block">
              {services.featured_services_count}
            </span>
          </div>
        </div>

        {categoryEntries.length > 0 && (
          <div className="mt-4 pt-3 border-t border-gray-100 dark:border-gray-800">
            <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">
              Categories
            </h3>
            <div className="flex flex-wrap gap-1.5">
              {categoryEntries.map(([cat, count]) => (
                <span
                  key={cat}
                  className="px-2.5 py-1 text-xs font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 rounded-md"
                >
                  {cat.replace(/_/g, " ")} ({count})
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
