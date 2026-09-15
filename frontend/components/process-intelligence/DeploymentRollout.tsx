'use client';

import React from 'react';
import { GitPullRequest, RotateCcw, CheckCircle2, ShieldCheck, Activity } from 'lucide-react';

interface Props {
  processId: string;
}

export default function DeploymentRollout({ processId }: Props) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <GitPullRequest className="w-5 h-5 text-indigo-400" /> Controlled Workflow Deployments & Canary Gates
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Zero-downtime workflow version promotion with automatic health checks and rollback guarantees
          </p>
        </div>
      </div>

      <div className="bg-slate-950 border border-slate-800 rounded-lg p-5 space-y-4">
        <div className="flex justify-between items-start">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono text-indigo-400">DEP-CAN-88F12A</span>
              <span className="px-2 py-0.5 text-xs rounded bg-emerald-500/20 text-emerald-300 font-semibold">
                ACTIVE (10% CANARY)
              </span>
            </div>
            <h4 className="text-base font-bold text-white mt-1">Lead Qualification & Outreach Automation v2</h4>
            <p className="text-xs text-slate-400">Target Version: v2 &bull; Approved by Governance Committee</p>
          </div>

          <button className="bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 text-xs font-medium py-1.5 px-3 rounded flex items-center gap-1.5 transition">
            <RotateCcw className="w-3.5 h-3.5" /> Instant Rollback
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div className="bg-slate-900 border border-slate-800 rounded p-3">
            <span className="text-xs text-slate-400">Routed Cases</span>
            <p className="text-base font-bold text-white mt-0.5">14 cases</p>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded p-3">
            <span className="text-xs text-slate-400">Canary Error Rate</span>
            <p className="text-base font-bold text-emerald-400 mt-0.5">0.0% (Health: Normal)</p>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded p-3">
            <span className="text-xs text-slate-400">Avg Cycle Time</span>
            <p className="text-base font-bold text-white mt-0.5">6.8 hrs (-24%)</p>
          </div>
        </div>
      </div>
    </div>
  );
}
