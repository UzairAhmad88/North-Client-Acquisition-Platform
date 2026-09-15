"use client";

import React from "react";
import Link from "next/link";
import { Target, ArrowRight, Building2 } from "lucide-react";
import { RecentLeadItem } from "@/lib/api/dashboard";

interface RecentLeadsCardProps {
  leads: RecentLeadItem[];
}

export function RecentLeadsCard({ leads }: RecentLeadsCardProps) {
  const getStatusBadge = (status: string) => {
    switch (status) {
      case "QUALIFIED":
        return "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300";
      case "NEW":
        return "bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300";
      case "WON":
        return "bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300";
      case "LOST":
        return "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300";
      default:
        return "bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300";
    }
  };

  return (
    <div className="p-6 rounded-xl bg-white dark:bg-gray-850 border border-gray-200 dark:border-gray-800 shadow-sm flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <h2 className="text-base font-bold text-gray-900 dark:text-gray-100">Recent Leads</h2>
          </div>
          <Link
            href="/leads"
            className="text-xs font-medium text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
          >
            <span>View all</span>
            <ArrowRight className="w-3 h-3" />
          </Link>
        </div>

        {leads.length === 0 ? (
          <div className="py-8 text-center text-sm text-gray-500 dark:text-gray-400">
            No leads recorded yet.
          </div>
        ) : (
          <div className="divide-y divide-gray-100 dark:divide-gray-800">
            {leads.map((lead) => (
              <div key={lead.id} className="py-3 flex items-center justify-between gap-3">
                <div className="min-w-0 flex-1">
                  <Link
                    href={`/leads/${lead.id}`}
                    className="text-sm font-semibold text-gray-900 dark:text-gray-100 hover:underline truncate block"
                  >
                    {lead.title}
                  </Link>
                  <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    <Building2 className="w-3 h-3 shrink-0" />
                    <span className="truncate">{lead.business_name}</span>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <span
                    className={`px-2 py-0.5 text-xs font-medium rounded-full ${getStatusBadge(
                      lead.status
                    )}`}
                  >
                    {lead.status}
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
