'use client';

import React, { useState, useEffect } from 'react';
import { HumanTask, orchestrationApi } from '@/lib/api/orchestration';
import { CheckCircle, XCircle, AlertCircle, Clock, Check, RefreshCw } from 'lucide-react';

export const HumanTaskQueue: React.FC = () => {
  const [tasks, setTasks] = useState<HumanTask[]>([]);
  const [selectedTask, setSelectedTask] = useState<HumanTask | null>(null);
  const [loading, setLoading] = useState(true);
  const [decisionReason, setDecisionReason] = useState<string>('');
  const [submitting, setSubmitting] = useState(false);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const data = await orchestrationApi.listTasks();
      setTasks(data);
    } catch (err) {
      console.error('Failed to load tasks', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleDecision = async (decision: 'APPROVED' | 'REJECTED' | 'REVISION_REQUIRED') => {
    if (!selectedTask) return;
    try {
      setSubmitting(true);
      await orchestrationApi.completeTask(selectedTask.id, {
        decision,
        decision_reason: decisionReason || `Task ${decision} by operator`,
      });
      setSelectedTask(null);
      setDecisionReason('');
      loadTasks();
    } catch (err) {
      console.error('Failed to submit decision', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Human Task List */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col h-[520px]">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <Clock className="w-4 h-4 text-amber-400" /> Human Approval Queue
          </h3>
          <button onClick={loadTasks} className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg">
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto divide-y divide-slate-800">
          {loading ? (
            <div className="p-8 text-center text-slate-500 text-xs">Loading pending review tasks...</div>
          ) : tasks.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs">No pending review tasks found.</div>
          ) : (
            tasks.map((task) => (
              <div
                key={task.id}
                onClick={() => setSelectedTask(task)}
                className={`p-4 hover:bg-slate-800/40 transition-colors cursor-pointer flex items-center justify-between ${
                  selectedTask?.id === task.id ? 'bg-slate-800/60 border-l-2 border-amber-500' : ''
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-slate-200">{task.title}</span>
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                        task.status === 'PENDING'
                          ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                          : task.status === 'APPROVED'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      }`}
                    >
                      {task.status}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400">
                    Type: <strong className="text-slate-300">{task.task_type}</strong> • Step: <span className="font-mono">{task.step_key}</span>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Review Decision Workspace */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 overflow-y-auto h-[520px]">
        {selectedTask ? (
          <div className="space-y-4">
            <div className="border-b border-slate-800 pb-3">
              <h4 className="text-sm font-semibold text-slate-100">{selectedTask.title}</h4>
              <p className="text-xs text-slate-400 mt-1">{selectedTask.description}</p>
            </div>

            <div>
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                Context Payload
              </div>
              <pre className="text-xs font-mono bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-300 overflow-x-auto max-h-48">
                {JSON.stringify(selectedTask.input_data, null, 2)}
              </pre>
            </div>

            {selectedTask.status === 'PENDING' ? (
              <div className="space-y-3 pt-2">
                <div>
                  <label className="text-xs font-semibold text-slate-300 block mb-1">Decision Rationale</label>
                  <textarea
                    rows={2}
                    value={decisionReason}
                    onChange={(e) => setDecisionReason(e.target.value)}
                    placeholder="Enter approval or rejection justification..."
                    className="w-full bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg p-2.5 outline-none focus:border-cyan-500"
                  />
                </div>

                <div className="flex items-center gap-2 pt-1">
                  <button
                    onClick={() => handleDecision('APPROVED')}
                    disabled={submitting}
                    className="flex-1 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-xs font-semibold py-2 rounded-lg transition-colors flex items-center justify-center gap-1.5"
                  >
                    <CheckCircle className="w-3.5 h-3.5" /> Approve Action
                  </button>
                  <button
                    onClick={() => handleDecision('REJECTED')}
                    disabled={submitting}
                    className="flex-1 bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white text-xs font-semibold py-2 rounded-lg transition-colors flex items-center justify-center gap-1.5"
                  >
                    <XCircle className="w-3.5 h-3.5" /> Reject
                  </button>
                </div>
              </div>
            ) : (
              <div className="p-3 bg-slate-800/60 rounded-lg border border-slate-700 text-xs space-y-1">
                <div>Decision: <strong className="text-slate-200">{selectedTask.decision}</strong></div>
                <div>Rationale: <span className="text-slate-400">{selectedTask.decision_reason}</span></div>
                <div>Completed: <span className="text-slate-400">{selectedTask.completed_at ? new Date(selectedTask.completed_at).toLocaleString() : 'N/A'}</span></div>
              </div>
            )}
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-xs text-slate-500">
            Select a task from the review queue to inspect input data and record human approval.
          </div>
        )}
      </div>
    </div>
  );
};
