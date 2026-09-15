'use client';

import React from 'react';
import { WorkflowRun } from '@/lib/api/orchestration';
import { CheckCircle2, Clock, Play, AlertCircle, SkipForward, ArrowRight } from 'lucide-react';

interface WorkflowTimelineProps {
  workflowRun: WorkflowRun;
}

export const WorkflowTimeline: React.FC<WorkflowTimelineProps> = ({ workflowRun }) => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-base font-semibold text-slate-100">{workflowRun.workflow_key}</h3>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
              {workflowRun.workflow_version}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">Execution ID: {workflowRun.id}</p>
        </div>
        <span
          className={`text-xs font-semibold px-3 py-1 rounded-full ${
            workflowRun.status === 'COMPLETED'
              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
              : workflowRun.status === 'RUNNING'
              ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'
              : workflowRun.status === 'WAITING'
              ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
              : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
          }`}
        >
          {workflowRun.status}
        </span>
      </div>

      {/* Input Data Summary */}
      {workflowRun.input_data && Object.keys(workflowRun.input_data).length > 0 && (
        <div className="bg-slate-800/40 rounded-lg p-3 border border-slate-700/50">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
            Input Context
          </div>
          <pre className="text-xs font-mono text-slate-300 overflow-x-auto">
            {JSON.stringify(workflowRun.input_data, null, 2)}
          </pre>
        </div>
      )}

      {/* Output Data Summary */}
      {workflowRun.output_data && Object.keys(workflowRun.output_data).length > 0 && (
        <div className="bg-slate-800/40 rounded-lg p-3 border border-slate-700/50">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
            Workflow Outputs
          </div>
          <pre className="text-xs font-mono text-slate-300 overflow-x-auto">
            {JSON.stringify(workflowRun.output_data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};
