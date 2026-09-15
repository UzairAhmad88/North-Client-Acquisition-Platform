'use client';

import React from 'react';
import { TaskItem } from '@/lib/api/projects';

interface TaskBoardProps {
  tasks: TaskItem[];
  onStatusChange?: (taskId: string, newStatus: string) => void;
}

const COLUMNS = [
  { key: 'TODO', label: 'To Do', badgeBg: 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300' },
  { key: 'IN_PROGRESS', label: 'In Progress', badgeBg: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300' },
  { key: 'BLOCKED', label: 'Blocked', badgeBg: 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300' },
  { key: 'IN_REVIEW', label: 'In Review', badgeBg: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300' },
  { key: 'COMPLETED', label: 'Completed', badgeBg: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300' },
];

export const TaskBoard: React.FC<TaskBoardProps> = ({ tasks, onStatusChange }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-4 overflow-x-auto pb-4">
      {COLUMNS.map((col) => {
        const columnTasks = tasks.filter((t) => t.status === col.key);
        return (
          <div key={col.key} className="bg-slate-50 dark:bg-slate-900/50 rounded-xl p-3 border border-slate-200 dark:border-slate-800 flex flex-col min-w-[220px]">
            <div className="flex items-center justify-between mb-3 px-1">
              <span className={`text-xs font-bold px-2 py-1 rounded-full ${col.badgeBg}`}>
                {col.label} ({columnTasks.length})
              </span>
            </div>

            <div className="space-y-3 flex-1 overflow-y-auto max-h-[600px] pr-1">
              {columnTasks.length === 0 ? (
                <div className="text-center py-6 text-xs text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-lg">
                  No tasks
                </div>
              ) : (
                columnTasks.map((task) => (
                  <div
                    key={task.id}
                    className="bg-white dark:bg-slate-800 p-3 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 hover:border-indigo-400 transition-all"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] font-mono text-slate-400">{task.task_number}</span>
                      <span
                        className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${
                          task.priority === 'CRITICAL'
                            ? 'bg-red-500 text-white'
                            : task.priority === 'HIGH'
                            ? 'bg-amber-500 text-white'
                            : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                        }`}
                      >
                        {task.priority}
                      </span>
                    </div>

                    <h4 className="text-xs font-semibold text-slate-900 dark:text-slate-100 mb-1">{task.name}</h4>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-2 mb-2">{task.description}</p>

                    {task.status === 'BLOCKED' && task.blocked_reason && (
                      <div className="text-[10px] bg-red-50 text-red-600 dark:bg-red-950/40 dark:text-red-300 p-1.5 rounded mb-2">
                        <strong>Blocked:</strong> {task.blocked_reason}
                      </div>
                    )}

                    <div className="flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-slate-100 dark:border-slate-700/50">
                      <span>Est: {task.estimated_hours}h</span>
                      <span>Act: {task.actual_hours}h</span>
                      <span className="font-semibold text-indigo-600 dark:text-indigo-400">{task.progress_percent}%</span>
                    </div>

                    {onStatusChange && (
                      <div className="mt-2 pt-2 border-t border-slate-100 dark:border-slate-700/50 flex gap-1 justify-end">
                        {col.key !== 'COMPLETED' && (
                          <button
                            onClick={() => onStatusChange(task.id, 'COMPLETED')}
                            className="text-[10px] bg-emerald-50 text-emerald-600 hover:bg-emerald-100 px-2 py-0.5 rounded"
                          >
                            Done
                          </button>
                        )}
                        {col.key === 'TODO' && (
                          <button
                            onClick={() => onStatusChange(task.id, 'IN_PROGRESS')}
                            className="text-[10px] bg-blue-50 text-blue-600 hover:bg-blue-100 px-2 py-0.5 rounded"
                          >
                            Start
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
