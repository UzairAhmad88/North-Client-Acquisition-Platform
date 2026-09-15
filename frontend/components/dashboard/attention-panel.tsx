"use client";

import React from "react";
import Link from "next/link";
import { AlertCircle, Clock, BookOpen, ArrowRight } from "lucide-react";
import { AttentionSummary, OverdueAction } from "@/lib/api/dashboard";

interface AttentionPanelProps {
  attention: AttentionSummary;
  overdueActions: OverdueAction[];
}

export function AttentionPanel({ attention, overdueActions }: AttentionPanelProps) {
  const hasItems =
    attention.high_priority_leads_count > 0 ||
    attention.overdue_actions_count > 0 ||
    attention.incomplete_data_businesses_count > 0;

  return (
    <div className="p-6 rounded-xl bg-white border border-slate-200/90 shadow-2xs">
      <div className="flex items-center justify-between pb-4 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-[#b45309]" />
          <h2 className="text-base font-extrabold text-slate-900">
            Attention Required
          </h2>
        </div>
        <span className="text-xs font-semibold text-slate-500">
          Operational items needing priority review
        </span>
      </div>

      {!hasItems ? (
        <div className="py-6 text-center text-xs font-semibold text-slate-500">
          ✨ All clear! Zero urgent items or overdue actions require attention.
        </div>
      ) : (
        <div className="mt-4 space-y-4">
          {/* Summary Badges */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <Link
              href="/leads?priority=HIGH"
              className="p-3.5 rounded-xl bg-[#fef3c7] border border-[#fde68a] flex items-center justify-between hover:bg-[#fde68a]/60 transition-colors"
            >
              <div className="flex items-center gap-2.5">
                <AlertCircle className="w-4 h-4 text-[#b45309]" />
                <div>
                  <div className="text-xs font-bold text-[#78350f]">
                    High Priority Leads
                  </div>
                  <div className="text-xs text-[#b45309] font-semibold">
                    {attention.high_priority_leads_count} opportunities
                  </div>
                </div>
              </div>
              <ArrowRight className="w-4 h-4 text-[#b45309]" />
            </Link>

            <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <Clock className="w-4 h-4 text-rose-700" />
                <div>
                  <div className="text-xs font-bold text-rose-900">
                    Overdue Actions
                  </div>
                  <div className="text-xs text-rose-700 font-semibold">
                    {attention.overdue_actions_count} items pending
                  </div>
                </div>
              </div>
            </div>

            <Link
              href="/knowledge"
              className="p-3.5 rounded-xl bg-[#fdf8f3] border border-[#f7ede2] flex items-center justify-between hover:bg-[#f7ede2]/80 transition-colors"
            >
              <div className="flex items-center gap-2.5">
                <BookOpen className="w-4 h-4 text-[#78350f]" />
                <div>
                  <div className="text-xs font-bold text-[#582c12]">
                    Knowledge & Incomplete Data
                  </div>
                  <div className="text-xs text-[#78350f] font-semibold">
                    {attention.incomplete_data_businesses_count} records
                  </div>
                </div>
              </div>
              <ArrowRight className="w-4 h-4 text-[#78350f]" />
            </Link>
          </div>

          {/* Overdue Action Item List */}
          {overdueActions.length > 0 && (
            <div className="mt-4 pt-3 border-t border-slate-100">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                Pending Overdue Actions
              </h3>
              <div className="divide-y divide-slate-100">
                {overdueActions.map((action) => (
                  <div
                    key={action.lead_id}
                    className="py-2.5 flex items-center justify-between text-sm"
                  >
                    <div>
                      <Link
                        href={`/leads/${action.lead_id}`}
                        className="font-bold text-slate-900 hover:text-[#0f4c3a] transition-colors"
                      >
                        {action.lead_title}
                      </Link>
                      <span className="text-xs text-slate-500 ml-2 font-medium">
                        ({action.business_name})
                      </span>
                      <div className="text-xs text-rose-600 font-semibold mt-0.5">
                        Action: {action.next_action || "Follow up required"} &bull; Due:{" "}
                        {new Date(action.next_action_at).toLocaleDateString()}
                      </div>
                    </div>
                    <Link
                      href={`/leads/${action.lead_id}`}
                      className="px-3 py-1 text-xs font-bold text-[#78350f] bg-[#fef3c7] rounded-md border border-[#fde68a] hover:bg-[#fde68a] transition-colors"
                    >
                      Resolve
                    </Link>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
