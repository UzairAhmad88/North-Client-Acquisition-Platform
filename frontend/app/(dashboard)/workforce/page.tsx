'use client';

import React, { useState, useEffect } from 'react';
import { WorkforceDashboard } from '../../../components/workforce';
import {
  workforceApi,
  WorkforceOverview,
  AIWorker,
  AIDepartment,
  AITeam,
  AIWorkTask,
  AIHandoff,
  AIConsensusResult,
} from '../../../lib/api/workforce';
import { RefreshCw, AlertCircle } from 'lucide-react';

export default function WorkforcePage() {
  const [overview, setOverview] = useState<WorkforceOverview | null>(null);
  const [workers, setWorkers] = useState<AIWorker[]>([]);
  const [departments, setDepartments] = useState<AIDepartment[]>([]);
  const [teams, setTeams] = useState<AITeam[]>([]);
  const [tasks, setTasks] = useState<AIWorkTask[]>([]);
  const [handoffs, setHandoffs] = useState<AIHandoff[]>([]);
  const [pendingReviews, setPendingReviews] = useState<any[]>([]);
  const [consensusResult, setConsensusResult] = useState<AIConsensusResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [
        overviewRes,
        workersRes,
        deptsRes,
        teamsRes,
        tasksRes,
        reviewsRes,
      ] = await Promise.all([
        workforceApi.getOverview().catch(() => null),
        workforceApi.getWorkers().catch(() => []),
        workforceApi.getDepartments().catch(() => []),
        workforceApi.getTeams().catch(() => []),
        workforceApi.getTasks().catch(() => []),
        workforceApi.getPendingReviews().catch(() => []),
      ]);

      if (overviewRes) setOverview(overviewRes);
      setWorkers(workersRes || []);
      setDepartments(deptsRes || []);
      setTeams(teamsRes || []);
      setTasks(tasksRes || []);
      setPendingReviews(reviewsRes || []);

      // Mocked sample handoff and consensus result for demonstration
      setHandoffs([
        {
          handoff_code: 'HND-DISC-001',
          from_worker_code: 'WRK-RESEARCH-01',
          to_worker_code: 'WRK-LEAD_QUALIFICATION-01',
          task_code: 'TSK-OUTREACH-01',
          context_summary: 'Target enterprise digital audit completed. 8 high-impact automation findings identified.',
          artifacts: [{ type: 'AUDIT_REPORT', findings_count: 8 }],
          expected_next_action: 'Evaluate lead opportunity fit score and calculate recommended service tiers.',
          confidence_score: 0.96,
          status: 'DELIVERED',
        },
      ]);

      setConsensusResult({
        consensus_code: 'CNS-STRAT-01',
        topic: 'Expansion into Multi-Location Dental Software Modernization',
        participating_workers: ['WRK-RESEARCH-01', 'WRK-SALES_INTELLIGENCE-01', 'WRK-FINANCE-01'],
        consensus_score: 0.94,
        has_conflicts: false,
        synthesized_conclusion: 'Unanimous alignment across research, sales, and finance specialists. Projected ROI multiple 5.2x with low downside risk.',
        dissenting_views: [],
      });
    } catch (err: any) {
      console.error('Failed to load workforce data:', err);
      setError(err.message || 'Failed to connect to Workforce Platform Service');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDecomposeObjective = async (objective: string) => {
    const newTasks = await workforceApi.decomposeObjective(objective);
    setTasks((prev) => [...newTasks, ...prev]);
  };

  const handleResolveReview = async (reviewId: string, approved: boolean, rationale: string) => {
    await workforceApi.resolveReview(reviewId, approved, 'Executive Reviewer', rationale);
    setPendingReviews((prev) => prev.filter((r) => r.review_id !== reviewId));
    await loadData();
  };

  const handleTriggerKillSwitch = async (targetType: string, targetIdentifier: string, reason: string) => {
    await workforceApi.triggerKillSwitch(targetType, targetIdentifier, reason);
    await loadData();
  };

  const handleQueryCopilot = async (query: string) => {
    return await workforceApi.queryCopilot(query);
  };

  return (
    <div className="p-6 md:p-8 space-y-6 max-w-7xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-black tracking-tight text-white">
              Autonomous Knowledge Worker & Multi-Agent Platform
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
              Phase 52
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Governed AI workforce coordination across 20 specialized knowledge workers, departmental squads, DAG task graphs, and Level 0-5 human supervision.
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

      {/* Main Tabbed Workforce Dashboard */}
      <WorkforceDashboard
        overview={overview}
        workers={workers}
        departments={departments}
        teams={teams}
        tasks={tasks}
        handoffs={handoffs}
        pendingReviews={pendingReviews}
        consensusResult={consensusResult}
        onDecomposeObjective={handleDecomposeObjective}
        onResolveReview={handleResolveReview}
        onTriggerKillSwitch={handleTriggerKillSwitch}
        onQueryCopilot={handleQueryCopilot}
      />
    </div>
  );
}
