'use client';

import React, { useState } from 'react';
import {
  Compass,
  Target,
  Layers,
  Cpu,
  BarChart3,
  CheckCircle2,
  AlertTriangle,
  Bot,
  UserCheck,
  TrendingUp,
} from 'lucide-react';
import { StrategyOverview } from './StrategyOverview';
import { ObjectiveTree } from './ObjectiveTree';
import { InitiativePortfolio } from './InitiativePortfolio';
import { OptimizationPanel } from './OptimizationPanel';
import { ParetoChart } from './ParetoChart';
import { FeasibilityPanel } from './FeasibilityPanel';
import { DecisionRecord } from './DecisionRecord';
import { StrategyCopilot } from './StrategyCopilot';
import {
  StrategicPlanOverview,
  StrategicObjective,
  StrategicInitiative,
  OptimizationRun,
  ParetoFrontier,
  StrategicDecisionRecord,
  StrategyCopilotQueryResponse,
} from '../../lib/api/strategy';

interface StrategyDashboardProps {
  overview: StrategicPlanOverview | null;
  objectives: StrategicObjective[];
  initiatives: StrategicInitiative[];
  optimizationRuns: OptimizationRun[];
  paretoFrontier: ParetoFrontier | null;
  decisions: StrategicDecisionRecord[];
  feasibilityData: any[];
  pendingDecisions?: any[];
  onTriggerOptimization?: (planId: string, weights: any, budgetCeiling: number, fteCeiling: number) => Promise<any>;
  onApproveDecision?: (optionId: string, rationale: string) => Promise<void>;
  onRejectDecision?: (optionId: string, reason: string) => Promise<void>;
  onQueryCopilot?: (query: string) => Promise<StrategyCopilotQueryResponse>;
}

export const StrategyDashboard: React.FC<StrategyDashboardProps> = ({
  overview,
  objectives,
  initiatives,
  optimizationRuns,
  paretoFrontier,
  decisions,
  feasibilityData,
  pendingDecisions,
  onTriggerOptimization,
  onApproveDecision,
  onRejectDecision,
  onQueryCopilot,
}) => {
  const [activeTab, setActiveTab] = useState<
    'overview' | 'objectives' | 'initiatives' | 'optimization' | 'pareto' | 'feasibility' | 'governance' | 'copilot'
  >('overview');

  const tabs = [
    { id: 'overview', label: 'Overview & Health', icon: <Compass className="h-4 w-4" /> },
    { id: 'objectives', label: 'Objectives & OKRs', icon: <Target className="h-4 w-4" />, count: objectives.length },
    { id: 'initiatives', label: 'Initiatives', icon: <Layers className="h-4 w-4" />, count: initiatives.length },
    { id: 'optimization', label: 'Optimization Solver', icon: <Cpu className="h-4 w-4" /> },
    { id: 'pareto', label: 'Pareto Packages', icon: <BarChart3 className="h-4 w-4" /> },
    { id: 'feasibility', label: 'Feasibility & Gaps', icon: <TrendingUp className="h-4 w-4" /> },
    { id: 'governance', label: 'Decision Ledger', icon: <UserCheck className="h-4 w-4" />, badge: pendingDecisions?.length },
    { id: 'copilot', label: 'Strategy Copilot', icon: <Bot className="h-4 w-4" /> },
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
          <StrategyOverview
            overview={overview}
            onSelectPlan={(id) => setActiveTab('objectives')}
          />
        )}

        {activeTab === 'objectives' && (
          <ObjectiveTree objectives={objectives} />
        )}

        {activeTab === 'initiatives' && (
          <InitiativePortfolio initiatives={initiatives} />
        )}

        {activeTab === 'optimization' && (
          <OptimizationPanel
            activeRun={optimizationRuns[0] || null}
            onRunOptimization={onTriggerOptimization}
          />
        )}

        {activeTab === 'pareto' && (
          <ParetoChart paretoFrontier={paretoFrontier} />
        )}

        {activeTab === 'feasibility' && (
          <FeasibilityPanel feasibilityData={feasibilityData} />
        )}

        {activeTab === 'governance' && (
          <DecisionRecord
            decisions={decisions}
            pendingOptions={pendingDecisions}
            onApproveDecision={onApproveDecision}
            onRejectDecision={onRejectDecision}
          />
        )}

        {activeTab === 'copilot' && (
          <StrategyCopilot onQuery={onQueryCopilot} />
        )}
      </div>
    </div>
  );
};
