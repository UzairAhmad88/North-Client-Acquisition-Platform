'use client';

import React, { useState } from 'react';
import {
  Users,
  Building2,
  GitBranch,
  Layers,
  UserCheck,
  CheckCircle2,
  ShieldAlert,
  Bot,
  Activity,
  DollarSign,
} from 'lucide-react';
import { WorkforceOverview } from './WorkforceOverview';
import { WorkerCard } from './WorkerCard';
import { TaskGraph } from './TaskGraph';
import { HandoffPanel } from './HandoffPanel';
import { ReviewQueue } from './ReviewQueue';
import { ConsensusView } from './ConsensusView';
import { IncidentPanel } from './IncidentPanel';
import { WorkforceCopilot } from './WorkforceCopilot';
import {
  WorkforceOverview as WorkforceOverviewData,
  AIWorker,
  AIDepartment,
  AITeam,
  AIWorkTask,
  AIHandoff,
  AIConsensusResult,
  WorkforceCopilotResponse,
} from '../../lib/api/workforce';

interface WorkforceDashboardProps {
  overview: WorkforceOverviewData | null;
  workers: AIWorker[];
  departments: AIDepartment[];
  teams: AITeam[];
  tasks: AIWorkTask[];
  handoffs: AIHandoff[];
  pendingReviews: any[];
  consensusResult: AIConsensusResult | null;
  onDecomposeObjective?: (objective: string) => Promise<void>;
  onResolveReview?: (reviewId: string, approved: boolean, rationale: string) => Promise<void>;
  onTriggerKillSwitch?: (targetType: string, targetIdentifier: string, reason: string) => Promise<void>;
  onQueryCopilot?: (query: string) => Promise<WorkforceCopilotResponse>;
}

export const WorkforceDashboard: React.FC<WorkforceDashboardProps> = ({
  overview,
  workers,
  departments,
  teams,
  tasks,
  handoffs,
  pendingReviews,
  consensusResult,
  onDecomposeObjective,
  onResolveReview,
  onTriggerKillSwitch,
  onQueryCopilot,
}) => {
  const [activeTab, setActiveTab] = useState<
    'overview' | 'workers' | 'teams' | 'tasks' | 'handoffs' | 'reviews' | 'consensus' | 'emergency' | 'copilot'
  >('overview');

  const tabs = [
    { id: 'overview', label: 'Workforce Overview', icon: <Activity className="h-4 w-4" /> },
    { id: 'workers', label: 'AI Workers', icon: <Users className="h-4 w-4" />, count: workers.length },
    { id: 'teams', label: 'Departments & Squads', icon: <Building2 className="h-4 w-4" />, count: teams.length },
    { id: 'tasks', label: 'Task Graph', icon: <GitBranch className="h-4 w-4" />, count: tasks.length },
    { id: 'handoffs', label: 'Handoffs', icon: <Layers className="h-4 w-4" />, count: handoffs.length },
    { id: 'reviews', label: 'Review Queue', icon: <UserCheck className="h-4 w-4" />, badge: pendingReviews.length },
    { id: 'consensus', label: 'Consensus', icon: <CheckCircle2 className="h-4 w-4" /> },
    { id: 'emergency', label: 'Kill Switches', icon: <ShieldAlert className="h-4 w-4" /> },
    { id: 'copilot', label: 'Workforce Copilot', icon: <Bot className="h-4 w-4" /> },
  ];

  return (
    <div className="space-y-6">
      {/* Top Navigation Tabs */}
      <div className="flex items-center gap-1.5 p-1.5 rounded-xl bg-slate-900/80 border border-slate-800 overflow-x-auto">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-medium transition-all whitespace-nowrap cursor-pointer ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-sm shadow-indigo-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              {tab.icon}
              <span>{tab.label}</span>
              {tab.count !== undefined && (
                <span
                  className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                    isActive ? 'bg-indigo-700 text-white' : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {tab.count}
                </span>
              )}
              {tab.badge !== undefined && tab.badge > 0 && (
                <span className="text-[10px] px-1.5 py-0.2 rounded-full bg-amber-500/20 text-amber-300 font-bold border border-amber-500/40 animate-pulse">
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Main Tab Content */}
      <div>
        {activeTab === 'overview' && (
          <WorkforceOverview overview={overview} onSelectTab={(t) => setActiveTab(t as any)} />
        )}

        {activeTab === 'workers' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {workers.map((w) => (
              <WorkerCard key={w.worker_code} worker={w} />
            ))}
          </div>
        )}

        {activeTab === 'teams' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {teams.map((t) => (
                <div key={t.team_code} className="p-5 rounded-xl border border-slate-700/60 bg-slate-900/50 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                      {t.team_code}
                    </span>
                    <span className="text-xs font-semibold text-slate-400">${t.budget_limit_usd}/mo limit</span>
                  </div>
                  <h3 className="text-sm font-bold text-white">{t.name}</h3>
                  <p className="text-xs text-slate-400">{t.purpose}</p>
                  <div className="pt-2 border-t border-slate-800 flex flex-wrap gap-1.5">
                    {t.members.map((m, idx) => (
                      <span key={idx} className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">
                        {m}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'tasks' && (
          <TaskGraph tasks={tasks} onDecomposeObjective={onDecomposeObjective} />
        )}

        {activeTab === 'handoffs' && (
          <HandoffPanel handoffs={handoffs} />
        )}

        {activeTab === 'reviews' && (
          <ReviewQueue pendingReviews={pendingReviews} onResolveReview={onResolveReview} />
        )}

        {activeTab === 'consensus' && (
          <ConsensusView consensusResult={consensusResult} />
        )}

        {activeTab === 'emergency' && (
          <IncidentPanel onTriggerKillSwitch={onTriggerKillSwitch} />
        )}

        {activeTab === 'copilot' && (
          <WorkforceCopilot onQuery={onQueryCopilot} />
        )}
      </div>
    </div>
  );
};
