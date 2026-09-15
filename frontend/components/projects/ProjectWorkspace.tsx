'use client';

import React, { useState } from 'react';
import { ProjectDetail } from '@/lib/api/projects';
import { TaskBoard } from './TaskBoard';
import { ProjectHealthPanel } from './ProjectHealthPanel';
import { ScopeMonitorPanel } from './ScopeMonitorPanel';
import { EffortPanel } from './EffortPanel';

interface ProjectWorkspaceProps {
  project: ProjectDetail;
  onStatusChange?: (status: string) => void;
  onTaskStatusChange?: (taskId: string, newStatus: string) => void;
}

export const ProjectWorkspace: React.FC<ProjectWorkspaceProps> = ({
  project,
  onStatusChange,
  onTaskStatusChange,
}) => {
  const [activeTab, setActiveTab] = useState<'OVERVIEW' | 'BOARD' | 'EFFORT' | 'SCOPE' | 'DELIVERABLES'>('OVERVIEW');

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300">
                {project.project_number}
              </span>
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
                {project.status}
              </span>
            </div>
            <h1 className="text-xl font-bold text-slate-900 dark:text-slate-100">{project.name}</h1>
            <p className="text-xs text-slate-500 mt-1 max-w-2xl">{project.description}</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right">
              <span className="text-[11px] text-slate-400 block font-medium">Overall Progress</span>
              <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400">{project.progress_percent}%</span>
            </div>
            {onStatusChange && project.status === 'INITIATED' && (
              <button
                onClick={() => onStatusChange('PLANNING')}
                className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-all"
              >
                Start Planning
              </button>
            )}
            {onStatusChange && project.status === 'READY' && (
              <button
                onClick={() => onStatusChange('IN_PROGRESS')}
                className="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-all"
              >
                Start Execution
              </button>
            )}
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex gap-2 mt-6 pt-4 border-t border-slate-100 dark:border-slate-700/50">
          {(['OVERVIEW', 'BOARD', 'EFFORT', 'SCOPE', 'DELIVERABLES'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`text-xs font-semibold px-3 py-1.5 rounded-lg transition-all ${
                activeTab === tab
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Contents */}
      {activeTab === 'OVERVIEW' && (
        <div className="space-y-6">
          <ProjectHealthPanel
            health={project.health}
            reasons={['All milestones and tasks are progressing on baseline schedule.']}
            effortVariance={project.total_actual_hours - project.total_estimated_hours}
            overdueCount={0}
            blockedCount={project.tasks.filter((t) => t.status === 'BLOCKED').length}
          />
          <TaskBoard tasks={project.tasks} onStatusChange={onTaskStatusChange} />
        </div>
      )}

      {activeTab === 'BOARD' && <TaskBoard tasks={project.tasks} onStatusChange={onTaskStatusChange} />}

      {activeTab === 'EFFORT' && (
        <EffortPanel
          tasks={project.tasks}
          totalEstimated={project.total_estimated_hours}
          totalActual={project.total_actual_hours}
        />
      )}

      {activeTab === 'SCOPE' && <ScopeMonitorPanel signals={[]} />}

      {activeTab === 'DELIVERABLES' && (
        <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm">
          <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100 mb-4">Committed Project Deliverables</h3>
          <div className="space-y-3">
            {project.deliverables.map((d) => (
              <div key={d.id} className="p-4 bg-slate-50 dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-700">
                <div className="flex items-center justify-between mb-1">
                  <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">{d.name}</h4>
                  <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
                    {d.status}
                  </span>
                </div>
                <p className="text-xs text-slate-500 mb-2">{d.description}</p>
                <div className="text-[11px] text-slate-400">
                  <strong>Baseline Item:</strong> {d.source_baseline_item}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
