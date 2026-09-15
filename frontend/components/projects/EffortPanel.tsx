'use client';

import React from 'react';
import { TaskItem } from '@/lib/api/projects';

interface EffortPanelProps {
  tasks: TaskItem[];
  totalEstimated: number;
  totalActual: number;
}

export const EffortPanel: React.FC<EffortPanelProps> = ({ tasks, totalEstimated, totalActual }) => {
  const variance = totalActual - totalEstimated;

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm mb-6">
      <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100 mb-4">Estimated vs. Actual Effort Tracking</h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700">
          <span className="text-xs text-slate-400 font-medium">Total Estimated Effort</span>
          <p className="text-xl font-bold text-slate-800 dark:text-slate-100">{totalEstimated.toFixed(1)}h</p>
        </div>
        <div className="bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700">
          <span className="text-xs text-slate-400 font-medium">Total Actual Effort Logged</span>
          <p className="text-xl font-bold text-indigo-600 dark:text-indigo-400">{totalActual.toFixed(1)}h</p>
        </div>
        <div className="bg-slate-50 dark:bg-slate-900/50 p-4 rounded-xl border border-slate-200 dark:border-slate-700">
          <span className="text-xs text-slate-400 font-medium">Effort Variance</span>
          <p className={`text-xl font-bold ${variance > 0 ? 'text-amber-600' : 'text-emerald-600'}`}>
            {variance > 0 ? `+${variance.toFixed(1)}h` : `${variance.toFixed(1)}h`}
          </p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-200 dark:border-slate-700 text-slate-400">
              <th className="py-2 px-3">Task ID</th>
              <th className="py-2 px-3">Task Name</th>
              <th className="py-2 px-3">Status</th>
              <th className="py-2 px-3 text-right">Estimated</th>
              <th className="py-2 px-3 text-right">Actual</th>
              <th className="py-2 px-3 text-right">Variance</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {tasks.map((task) => {
              const diff = task.actual_hours - task.estimated_hours;
              return (
                <tr key={task.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                  <td className="py-2.5 px-3 font-mono text-slate-400">{task.task_number}</td>
                  <td className="py-2.5 px-3 font-medium text-slate-800 dark:text-slate-200">{task.name}</td>
                  <td className="py-2.5 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px] bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
                      {task.status}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-right text-slate-600 dark:text-slate-400">{task.estimated_hours}h</td>
                  <td className="py-2.5 px-3 text-right font-semibold text-slate-800 dark:text-slate-200">{task.actual_hours}h</td>
                  <td className={`py-2.5 px-3 text-right font-bold ${diff > 0 ? 'text-amber-600' : 'text-emerald-600'}`}>
                    {diff > 0 ? `+${diff.toFixed(1)}h` : `${diff.toFixed(1)}h`}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
