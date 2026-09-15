'use client';

import React, { useState, useEffect } from 'react';
import { StrategyDashboard } from '../../../components/strategy';
import { strategyApi, StrategicPlanOverview, StrategicObjective, StrategicInitiative, OptimizationRun, ParetoFrontier, StrategicDecisionRecord } from '../../../lib/api/strategy';
import { Sparkles, RefreshCw, AlertCircle, PlusCircle } from 'lucide-react';

export default function StrategyPage() {
  const [overview, setOverview] = useState<StrategicPlanOverview | null>(null);
  const [objectives, setObjectives] = useState<StrategicObjective[]>([]);
  const [initiatives, setInitiatives] = useState<StrategicInitiative[]>([]);
  const [optimizationRuns, setOptimizationRuns] = useState<OptimizationRun[]>([]);
  const [paretoFrontier, setParetoFrontier] = useState<ParetoFrontier | null>(null);
  const [decisions, setDecisions] = useState<StrategicDecisionRecord[]>([]);
  const [feasibilityData, setFeasibilityData] = useState<any[]>([]);
  const [pendingDecisions, setPendingDecisions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [
        overviewRes,
        objectivesRes,
        initiativesRes,
        paretoRes,
        decisionsRes,
      ] = await Promise.all([
        strategyApi.getOverview().catch(() => null),
        strategyApi.getObjectives().catch(() => []),
        strategyApi.getInitiatives().catch(() => []),
        strategyApi.getParetoAnalysis().catch(() => null),
        strategyApi.getDecisions().catch(() => []),
      ]);

      if (overviewRes) setOverview(overviewRes);
      setObjectives(objectivesRes || []);
      setInitiatives(initiativesRes || []);
      if (paretoRes) setParetoFrontier(paretoRes);
      setDecisions(decisionsRes || []);

      // Mocked pending decision for interactive demonstration
      setPendingDecisions([
        {
          option_id: 'opt-2026-q3-01',
          question: 'Ratify Q3 Strategic Resource Reallocation: Enterprise AI Expansion',
          description: 'Reallocate 80h engineering capacity and $35,000 budget from outbound email marketing to Autonomous Discovery Engine scaling.',
          trade_off_summary: 'Increases qualified high-ticket leads by modeled +28%, but delays secondary website audit revamp by 2 weeks.',
          required_approval_role: 'CHIEF_STRATEGY_OFFICER',
          plan_id: overviewRes?.active_plans?.[0]?.plan_id || 'plan-master-2026',
        },
      ]);

      // Mocked feasibility items derived from objectives
      if (objectivesRes && objectivesRes.length > 0) {
        setFeasibilityData(
          objectivesRes.map((obj: StrategicObjective) => ({
            objective_id: obj.objective_id,
            name: obj.name,
            feasibility_score: 0.82,
            feasibility_level: 'LIKELY',
            confidence_score: obj.confidence || 0.85,
            strategic_gap: Math.max(0, (obj.target_value || 100) - (obj.current_value || 0)),
            gap_percentage: 18,
            limiting_factors: ['Engineering FTE capacity constrained at 82%'],
            mitigation_recommendations: ['Prioritize high-impact automated outreach scripts in Sprint 4'],
            unit: obj.unit,
            target_value: obj.target_value,
            current_value: obj.current_value,
          }))
        );
      } else {
        setFeasibilityData([
          {
            objective_id: 'obj-default-01',
            name: 'Scale Qualified Enterprise Opportunities to 500/mo',
            feasibility_score: 0.88,
            feasibility_level: 'FEASIBLE',
            confidence_score: 0.91,
            strategic_gap: 160,
            gap_percentage: 32,
            limiting_factors: ['Outreach email deliverability domain warm-up duration'],
            mitigation_recommendations: ['Activate dedicated pool of secondary outreach domains via Phase 37'],
            unit: 'opportunities',
            target_value: 500,
            current_value: 340,
          },
        ]);
      }
    } catch (err: any) {
      console.error('Failed to load strategy data:', err);
      setError(err.message || 'Failed to connect to Strategy Service');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleTriggerOptimization = async (
    planId: string,
    weights: any,
    budgetCeiling: number,
    fteCeiling: number
  ) => {
    const res = await strategyApi.runOptimization({
      plan_id: planId,
      budget_ceiling: budgetCeiling,
      fte_capacity_ceiling: fteCeiling,
      objective_weights: weights,
      solver_type: 'BRANCH_AND_BOUND_KNAPSACK',
    });
    setOptimizationRuns((prev) => [res, ...prev]);
    return res;
  };

  const handleApproveDecision = async (optionId: string, rationale: string) => {
    await strategyApi.approveDecision(optionId, rationale);
    setPendingDecisions((prev) => prev.filter((d) => d.option_id !== optionId));
    await loadData();
  };

  const handleRejectDecision = async (optionId: string, reason: string) => {
    await strategyApi.rejectDecision(optionId, reason);
    setPendingDecisions((prev) => prev.filter((d) => d.option_id !== optionId));
    await loadData();
  };

  const handleQueryCopilot = async (query: string) => {
    return await strategyApi.queryCopilot(query);
  };

  return (
    <div className="p-6 md:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black tracking-tight text-white">
              Strategy & Goal Optimization Engine
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
              Phase 51
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            End-to-end strategic planning, multi-objective portfolio optimization, Pareto frontier trade-offs, and human-in-the-loop governance.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={loadData}
            disabled={isLoading}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700/80 text-xs font-semibold text-slate-300 transition-all cursor-pointer"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl border border-rose-500/30 bg-rose-950/20 text-xs text-rose-300 flex items-center gap-2">
          <AlertCircle className="h-4 w-4 text-rose-400 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Tabbed Strategy Dashboard */}
      <StrategyDashboard
        overview={overview}
        objectives={objectives}
        initiatives={initiatives}
        optimizationRuns={optimizationRuns}
        paretoFrontier={paretoFrontier}
        decisions={decisions}
        feasibilityData={feasibilityData}
        pendingDecisions={pendingDecisions}
        onTriggerOptimization={handleTriggerOptimization}
        onApproveDecision={handleApproveDecision}
        onRejectDecision={handleRejectDecision}
        onQueryCopilot={handleQueryCopilot}
      />
    </div>
  );
}
