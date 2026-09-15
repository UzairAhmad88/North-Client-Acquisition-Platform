"use client";

import React from "react";
import Link from "next/link";
import { Calendar, ArrowRight } from "lucide-react";
import { UpcomingAction } from "@/lib/api/dashboard";

interface UpcomingActionsCardProps {
  actions: UpcomingAction[];
}

export function UpcomingActionsCard({ actions }: UpcomingActionsCardProps) {
  return (
    <div className="p-6 rounded-xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
          <div className="flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <h2 className="text-base font-bold text-gray-900 dark:text-gray-100">
              Upcoming Scheduled Actions
            </h2>
          </div>
          <Link
            href="/leads"
            className="text-xs font-medium text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-1"
          >
            <span>All actions</span>
            <ArrowRight className="w-3 h-3" />
          </Link>
        </div>

        {actions.length === 0 ? (
          <div className="py-8 text-center text-sm text-gray-500 dark:text-gray-400">
            No future lead actions currently scheduled.
          </div>
        ) : (
          <div className="divide-y divide-gray-100 dark:divide-gray-800">
            {actions.map((act) => (
              <div key={act.lead_id} className="py-3 flex items-center justify-between gap-3">
                <div className="min-w-0 flex-1">
                  <Link
                    href={`/leads/${act.lead_id}`}
                    className="text-sm font-semibold text-gray-900 dark:text-gray-100 hover:underline truncate block"
                  >
                    {act.lead_title}
                  </Link>
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    {act.next_action || "Follow up"} • {act.business_name}
                  </div>
                </div>

                <div className="text-right shrink-0">
                  <div className="text-xs font-medium text-gray-900 dark:text-gray-100">
                    {new Date(act.next_action_at).toLocaleDateString()}
                  </div>
                  <span className="text-[10px] font-semibold uppercase text-emerald-600 dark:text-emerald-400">
                    {act.priority}
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
