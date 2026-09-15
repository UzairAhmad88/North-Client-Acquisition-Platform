"use client";

import React from "react";
import Link from "next/link";
import { Building2, ArrowRight, MapPin } from "lucide-react";
import { RecentBusinessItem } from "@/lib/api/dashboard";

interface RecentBusinessesCardProps {
  businesses: RecentBusinessItem[];
}

export function RecentBusinessesCard({ businesses }: RecentBusinessesCardProps) {
  return (
    <div className="p-6 rounded-xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
          <div className="flex items-center gap-2">
            <Building2 className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            <h2 className="text-base font-bold text-gray-900 dark:text-gray-100">
              Recent Businesses
            </h2>
          </div>
          <Link
            href="/businesses"
            className="text-xs font-medium text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1"
          >
            <span>View all</span>
            <ArrowRight className="w-3 h-3" />
          </Link>
        </div>

        {businesses.length === 0 ? (
          <div className="py-8 text-center text-sm text-gray-500 dark:text-gray-400">
            No businesses registered yet.
          </div>
        ) : (
          <div className="divide-y divide-gray-100 dark:divide-gray-800">
            {businesses.map((biz) => (
              <div key={biz.id} className="py-3 flex items-center justify-between gap-3">
                <div className="min-w-0 flex-1">
                  <Link
                    href={`/businesses/${biz.id}`}
                    className="text-sm font-semibold text-gray-900 dark:text-gray-100 hover:underline truncate block"
                  >
                    {biz.name}
                  </Link>
                  <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    <span>{biz.industry || "General"}</span>
                    {biz.city && (
                      <span className="flex items-center gap-0.5">
                        <MapPin className="w-3 h-3" />
                        {biz.city}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <span
                    className={`px-2 py-0.5 text-xs font-semibold rounded ${
                      biz.data_quality_score >= 80
                        ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300"
                        : biz.data_quality_score >= 50
                        ? "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300"
                        : "bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300"
                    }`}
                    title="Data Quality Score"
                  >
                    {biz.data_quality_score}% Quality
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
