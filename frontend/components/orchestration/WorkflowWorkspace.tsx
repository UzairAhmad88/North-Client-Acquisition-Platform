'use client';

import React, { useState } from 'react';
import { WorkflowRun } from '@/lib/api/orchestration';
import { WorkflowDashboard } from './WorkflowDashboard';
import { WorkflowTimeline } from './WorkflowTimeline';
import { EventExplorer } from './EventExplorer';
import { HumanTaskQueue } from './HumanTaskQueue';
import { AutomationRuleBuilder } from './AutomationRuleBuilder';
import { DeadLetterQueueViewer } from './DeadLetterQueueViewer';
import { Activity, Radio, Clock, Sliders, AlertOctagon, GitBranch } from 'lucide-react';

export const WorkflowWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'workflows' | 'events' | 'tasks' | 'automation' | 'dlq'>('workflows');
  const [selectedRun, setSelectedRun] = useState<WorkflowRun | null>(null);

  return (
    <div className="space-y-6">
      {/* Workspace Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2.5">
            <GitBranch className="w-5 h-5 text-cyan-400" /> Workflow Orchestration & Event Control Plane
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Phase 34: Central orchestration, transactional outbox/inbox event bus, human approval gates, and automation rules.
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 p-1 rounded-xl">
          <button
            onClick={() => { setActiveTab('workflows'); setSelectedRun(null); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
              activeTab === 'workflows' ? 'bg-cyan-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Activity className="w-3.5 h-3.5" /> Workflows
          </button>
          <button
            onClick={() => { setActiveTab('events'); setSelectedRun(null); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
              activeTab === 'events' ? 'bg-cyan-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Radio className="w-3.5 h-3.5" /> Event Bus
          </button>
          <button
            onClick={() => { setActiveTab('tasks'); setSelectedRun(null); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
              activeTab === 'tasks' ? 'bg-cyan-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Clock className="w-3.5 h-3.5" /> Human Tasks
          </button>
          <button
            onClick={() => { setActiveTab('automation'); setSelectedRun(null); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
              activeTab === 'automation' ? 'bg-cyan-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sliders className="w-3.5 h-3.5" /> Automation
          </button>
          <button
            onClick={() => { setActiveTab('dlq'); setSelectedRun(null); }}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
              activeTab === 'dlq' ? 'bg-cyan-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <AlertOctagon className="w-3.5 h-3.5" /> DLQ
          </button>
        </div>
      </div>

      {/* Main Workspace Body */}
      {activeTab === 'workflows' && (
        selectedRun ? (
          <div className="space-y-4">
            <button
              onClick={() => setSelectedRun(null)}
              className="text-xs text-cyan-400 hover:text-cyan-300 font-medium flex items-center gap-1"
            >
              ← Back to Workflow Executions
            </button>
            <WorkflowTimeline workflowRun={selectedRun} />
          </div>
        ) : (
          <WorkflowDashboard onSelectRun={(run) => setSelectedRun(run)} />
        )
      )}

      {activeTab === 'events' && <EventExplorer />}
      {activeTab === 'tasks' && <HumanTaskQueue />}
      {activeTab === 'automation' && <AutomationRuleBuilder />}
      {activeTab === 'dlq' && <DeadLetterQueueViewer />}
    </div>
  );
};
