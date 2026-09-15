'use client';

import React, { useState, useEffect } from 'react';
import { WorkflowRun, WorkflowTemplate, orchestrationApi } from '@/lib/api/orchestration';
import { Play, Pause, XCircle, RotateCcw, Activity, CheckCircle2, Clock, AlertTriangle, Layers } from 'lucide-react';

interface WorkflowDashboardProps {
  onSelectRun?: (run: WorkflowRun) => void;
}

export const WorkflowDashboard: React.FC<WorkflowDashboardProps> = ({ onSelectRun }) => {
  const [runs, setRuns] = useState<WorkflowRun[]>([]);
  const [templates, setTemplates] = useState<WorkflowTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [startingKey, setStartingKey] = useState<string>('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [runsData, tplsData] = await Promise.all([
        orchestrationApi.listWorkflows(statusFilter || undefined),
        orchestrationApi.getTemplates(),
      ]);
      setRuns(runsData);
      setTemplates(tplsData);
    } catch (err) {
      console.error('Failed to load workflows', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [statusFilter]);

  const handleStartWorkflow = async (key: string) => {
    try {
      await orchestrationApi.startWorkflow({ workflow_key: key, input_data: { source: 'dashboard_manual_start' } });
      setStartingKey('');
      loadData();
    } catch (err) {
      console.error('Failed to start workflow', err);
    }
  };

  const handlePause = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await orchestrationApi.pauseWorkflow(id);
      loadData();
    } catch (err) {
      console.error('Failed to pause workflow', err);
    }
  };

  const handleResume = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await orchestrationApi.resumeWorkflow(id);
      loadData();
    } catch (err) {
      console.error('Failed to resume workflow', err);
    }
  };

  const handleCancel = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await orchestrationApi.cancelWorkflow(id, 'User manual cancellation');
      loadData();
    } catch (err) {
      console.error('Failed to cancel workflow', err);
    }
  };

  // KPI Metrics
  const runningCount = runs.filter(r => r.status === 'RUNNING').length;
  const waitingCount = runs.filter(r => r.status === 'WAITING').length;
  const completedCount = runs.filter(r => r.status === 'COMPLETED').length;
  const failedCount = runs.filter(r => r.status === 'FAILED' || r.status === 'BLOCKED').length;

  return (
    <div className="space-y-6">
      {/* Top Controls & KPI Bar */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center gap-3">
          <div className="p-3 bg-cyan-500/10 text-cyan-400 rounded-lg">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100">{runningCount}</div>
            <div className="text-xs text-slate-400">Running Executions</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center gap-3">
          <div className="p-3 bg-amber-500/10 text-amber-400 rounded-lg">
            <Clock className="w-5 h-5" />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100">{waitingCount}</div>
            <div className="text-xs text-slate-400">Waiting Approvals</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center gap-3">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-lg">
            <CheckCircle2 className="w-5 h-5" />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100">{completedCount}</div>
            <div className="text-xs text-slate-400">Completed Runs</div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center gap-3">
          <div className="p-3 bg-rose-500/10 text-rose-400 rounded-lg">
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div>
            <div className="text-2xl font-bold text-slate-100">{failedCount}</div>
            <div className="text-xs text-slate-400">Failed / Blocked</div>
          </div>
        </div>
      </div>

      {/* Start New Workflow Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200">Start Workflow Run</h3>
          <p className="text-xs text-slate-400">Launch a declarative business orchestration template</p>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={startingKey}
            onChange={(e) => setStartingKey(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2 outline-none focus:border-cyan-500"
          >
            <option value="">Select Template...</option>
            {templates.map((t) => (
              <option key={t.workflow_key} value={t.workflow_key}>
                {t.name} ({t.version})
              </option>
            ))}
          </select>
          <button
            onClick={() => startingKey && handleStartWorkflow(startingKey)}
            disabled={!startingKey}
            className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors flex items-center gap-1.5"
          >
            <Play className="w-3.5 h-3.5" /> Launch
          </button>
        </div>
      </div>

      {/* Workflow Runs Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-200">Workflow Runs</h3>
          <div className="flex items-center gap-2">
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-slate-800 border border-slate-700 text-slate-300 text-xs rounded-lg px-2.5 py-1.5 outline-none"
            >
              <option value="">All Statuses</option>
              <option value="RUNNING">Running</option>
              <option value="WAITING">Waiting</option>
              <option value="COMPLETED">Completed</option>
              <option value="PAUSED">Paused</option>
              <option value="FAILED">Failed</option>
              <option value="CANCELLED">Cancelled</option>
            </select>
          </div>
        </div>

        {loading ? (
          <div className="p-8 text-center text-slate-500 text-xs">Loading workflow executions...</div>
        ) : runs.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-xs">No workflow executions found.</div>
        ) : (
          <div className="divide-y divide-slate-800">
            {runs.map((run) => (
              <div
                key={run.id}
                onClick={() => onSelectRun && onSelectRun(run)}
                className="p-4 hover:bg-slate-800/40 transition-colors flex items-center justify-between cursor-pointer"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-slate-200">{run.workflow_key}</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                      {run.workflow_version}
                    </span>
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                        run.status === 'COMPLETED'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : run.status === 'RUNNING'
                          ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20'
                          : run.status === 'WAITING'
                          ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                          : run.status === 'PAUSED'
                          ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
                          : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      }`}
                    >
                      {run.status}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400 flex items-center gap-3">
                    <span>Current Step: <strong className="text-slate-300">{run.current_step || 'Completed'}</strong></span>
                    <span>Trigger: <strong className="text-slate-300">{run.trigger_type}</strong></span>
                    <span>Started: {new Date(run.started_at).toLocaleTimeString()}</span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {run.status === 'RUNNING' && (
                    <button
                      onClick={(e) => handlePause(run.id, e)}
                      title="Pause Workflow"
                      className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors"
                    >
                      <Pause className="w-3.5 h-3.5" />
                    </button>
                  )}
                  {run.status === 'PAUSED' && (
                    <button
                      onClick={(e) => handleResume(run.id, e)}
                      title="Resume Workflow"
                      className="p-1.5 bg-slate-800 hover:bg-slate-700 text-cyan-400 rounded-lg transition-colors"
                    >
                      <Play className="w-3.5 h-3.5" />
                    </button>
                  )}
                  {(run.status === 'RUNNING' || run.status === 'WAITING' || run.status === 'PAUSED') && (
                    <button
                      onClick={(e) => handleCancel(run.id, e)}
                      title="Cancel Workflow"
                      className="p-1.5 bg-slate-800 hover:bg-slate-700 text-rose-400 rounded-lg transition-colors"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
