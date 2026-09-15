'use client';

import React, { useState } from 'react';
import { GitBranch, CheckCircle2, Clock, AlertCircle, ArrowRight, Sparkles, Cpu } from 'lucide-react';
import { AIWorkTask } from '../../lib/api/workforce';

interface TaskGraphProps {
  tasks: AIWorkTask[];
  onDecomposeObjective?: (objective: string) => Promise<void>;
  isLoading?: boolean;
}

export const TaskGraph: React.FC<TaskGraphProps> = ({ tasks, onDecomposeObjective, isLoading }) => {
  const [objectiveInput, setObjectiveInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleDecompose = async () => {
    if (!objectiveInput.trim() || !onDecomposeObjective) return;
    setIsSubmitting(true);
    try {
      await onDecomposeObjective(objectiveInput);
      setObjectiveInput('');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return { icon: <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />, color: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' };
      case 'ASSIGNED':
      case 'QUEUED':
        return { icon: <Clock className="h-3.5 w-3.5 text-blue-400" />, color: 'bg-blue-500/10 text-blue-400 border-blue-500/30' };
      case 'REVIEW_REQUIRED':
        return { icon: <AlertCircle className="h-3.5 w-3.5 text-amber-400" />, color: 'bg-amber-500/10 text-amber-400 border-amber-500/30' };
      default:
        return { icon: <Cpu className="h-3.5 w-3.5 text-slate-400" />, color: 'bg-slate-500/10 text-slate-400 border-slate-500/30' };
    }
  };

  return (
    <div className="space-y-6">
      {/* Objective Decomposition Input Bar */}
      <div className="p-5 rounded-xl border border-slate-700/60 bg-slate-900/60 backdrop-blur-sm space-y-3">
        <div className="flex items-center gap-2 text-sm font-bold text-white">
          <Sparkles className="h-4 w-4 text-indigo-400" />
          <span>Objective Decomposition & Task Graph Generator</span>
        </div>
        <p className="text-xs text-slate-400">
          Input any business goal to decompose it into a directed acyclic task graph (DAG) with specialized AI worker assignments.
        </p>

        <div className="flex gap-2">
          <input
            type="text"
            value={objectiveInput}
            onChange={(e) => setObjectiveInput(e.target.value)}
            placeholder="e.g. Expand enterprise outreach across Texas healthcare practices with automated qualification..."
            className="flex-1 rounded-lg bg-slate-950/80 border border-slate-700/80 px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
          <button
            disabled={isSubmitting || !objectiveInput.trim()}
            onClick={handleDecompose}
            className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/20 disabled:opacity-50 transition-all cursor-pointer flex items-center gap-1.5"
          >
            <GitBranch className="h-3.5 w-3.5" />
            Decompose Goal
          </button>
        </div>
      </div>

      {/* Task Graph Visualizer List */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs font-bold text-slate-300">
          <div className="flex items-center gap-2">
            <GitBranch className="h-4 w-4 text-indigo-400" />
            <span>Task Graph Sequence ({tasks.length} Nodes)</span>
          </div>
        </div>

        {tasks.length === 0 ? (
          <div className="p-8 text-center rounded-xl border border-dashed border-slate-700/60 bg-slate-900/40 text-slate-500 text-xs">
            No active task graph nodes. Decompose an objective above to generate tasks.
          </div>
        ) : (
          <div className="space-y-3">
            {tasks.map((task, idx) => {
              const badge = getStatusBadge(task.status);
              return (
                <div
                  key={task.task_code || idx}
                  className="p-4 rounded-xl border border-slate-700/60 bg-slate-900/50 hover:border-slate-600 transition-all space-y-2"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono font-bold text-indigo-400 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
                        Node #{idx + 1}
                      </span>
                      <h4 className="text-xs font-bold text-white">{task.objective}</h4>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                        Worker: {task.worker_code || 'UNASSIGNED'}
                      </span>
                      <span className={`flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold border ${badge.color}`}>
                        {badge.icon}
                        <span>{task.status}</span>
                      </span>
                    </div>
                  </div>

                  <p className="text-xs text-slate-400 leading-relaxed">{task.description}</p>

                  {task.dependencies && task.dependencies.length > 0 && (
                    <div className="pt-2 border-t border-slate-800 flex items-center gap-2 text-[10px] text-slate-500">
                      <ArrowRight className="h-3 w-3 text-indigo-400" />
                      <span>Depends on: {task.dependencies.join(', ')}</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
