"use client";

import React from "react";
import { DecisionRoomOverview } from "@/lib/api/decision_rooms";
import { Shield, Brain, Users, AlertTriangle, CheckCircle, Scale, FileText } from "lucide-react";

interface Props {
  data: DecisionRoomOverview;
}

export const DecisionRoomOverviewView: React.FC<Props> = ({ data }) => {
  const { room, evidence, options, reviews, consensus, approvals } = data;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                {room.decision_type}
              </span>
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
                room.importance === "CRITICAL"
                  ? "bg-rose-500/10 text-rose-400 border-rose-500/20"
                  : room.importance === "HIGH"
                  ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
                  : "bg-slate-800 text-slate-300 border-slate-700"
              }`}>
                {room.importance} PRIORITY
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                STATUS: {room.status}
              </span>
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">{room.title}</h1>
            <p className="text-slate-400 text-sm mt-1 max-w-3xl">{room.question}</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right">
              <div className="text-xs text-slate-400">Specialist Consensus</div>
              <div className="text-xl font-bold text-emerald-400">{consensus.consensus_pct}%</div>
            </div>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>EVIDENCE ITEMS</span>
            <FileText className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold text-white">{evidence.length}</div>
          <div className="text-xs text-slate-400 mt-1">Fact vs inference bounded</div>
        </div>

        <div className="grid grid-cols-1 bg-slate-900/80 border border-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>CANDIDATE OPTIONS</span>
            <Scale className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold text-white">{options.length}</div>
          <div className="text-xs text-slate-400 mt-1">Multi-criteria scored</div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>ADVERSARIAL CRITIQUES</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-white">{reviews.length}</div>
          <div className="text-xs text-slate-400 mt-1">Stress-tested assumptions</div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-4">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>APPROVAL GATES</span>
            <Shield className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            {approvals.filter(a => a.status === "APPROVED").length} / {approvals.length}
          </div>
          <div className="text-xs text-slate-400 mt-1">Separation of duties enforced</div>
        </div>
      </div>
    </div>
  );
};
