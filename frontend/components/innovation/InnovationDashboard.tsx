'use client';

import React, { useState, useEffect } from 'react';
import {
  innovationApi,
  InnovationOverview,
  InnovationWorkspace,
  InnovationProblem,
  InnovationOpportunity,
  InnovationIdea,
  InnovationHypothesis,
  InnovationAssumption,
  InnovationExperiment,
  InnovationLearning,
  InnovationProductConcept,
  InnovationBusinessCase,
  InnovationEconomics,
  InnovationPrototype,
  InnovationPRD,
  InnovationGateReview,
  InnovationPortfolio,
  IdeaSource,
  HorizonLevel,
  GateStage,
  PivotAction
} from '../../lib/api/innovation';

import { ProblemBoard } from './ProblemBoard';
import { IdeaCard } from './IdeaCard';
import { AssumptionMatrix } from './AssumptionMatrix';
import { ExperimentRunner } from './ExperimentRunner';
import { ProductConceptViewer } from './ProductConceptViewer';
import { GateReviewPanel } from './GateReviewPanel';
import { PortfolioHorizonChart } from './PortfolioHorizonChart';
import { InnovationCopilot } from './InnovationCopilot';

type TabKey =
  | 'problems'
  | 'ideas'
  | 'assumptions'
  | 'experiments'
  | 'concepts'
  | 'gates'
  | 'portfolio'
  | 'copilot';

export const InnovationDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabKey>('problems');
  const [overview, setOverview] = useState<InnovationOverview | null>(null);
  const [workspaces, setWorkspaces] = useState<InnovationWorkspace[]>([]);
  const [activeWorkspaceId, setActiveWorkspaceId] = useState<string>('ws-demo-001');

  // Domain state
  const [problems, setProblems] = useState<InnovationProblem[]>([]);
  const [opportunities, setOpportunities] = useState<InnovationOpportunity[]>([]);
  const [ideas, setIdeas] = useState<InnovationIdea[]>([]);
  const [hypotheses, setHypotheses] = useState<InnovationHypothesis[]>([]);
  const [assumptions, setAssumptions] = useState<InnovationAssumption[]>([]);
  const [experiments, setExperiments] = useState<InnovationExperiment[]>([]);
  const [learnings, setLearnings] = useState<InnovationLearning[]>([]);
  const [concepts, setConcepts] = useState<InnovationProductConcept[]>([]);
  const [businessCases, setBusinessCases] = useState<InnovationBusinessCase[]>([]);
  const [prds, setPrds] = useState<InnovationPRD[]>([]);
  const [gateReviews, setGateReviews] = useState<InnovationGateReview[]>([]);
  const [portfolio, setPortfolio] = useState<InnovationPortfolio | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAllData();
  }, [activeWorkspaceId]);

  const loadAllData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        overviewRes,
        workspacesRes,
        problemsRes,
        oppsRes,
        ideasRes,
        hypoRes,
        asmpRes,
        expRes,
        learnRes,
        conceptsRes,
        bcaseRes,
        prdsRes,
        gatesRes,
        portfolioRes
      ] = await Promise.all([
        innovationApi.getOverview(),
        innovationApi.getWorkspaces(),
        innovationApi.getProblems(activeWorkspaceId),
        innovationApi.getOpportunities(activeWorkspaceId),
        innovationApi.getIdeas(activeWorkspaceId),
        innovationApi.getHypotheses(activeWorkspaceId),
        innovationApi.getAssumptions(activeWorkspaceId),
        innovationApi.getExperiments(activeWorkspaceId),
        innovationApi.getLearnings(activeWorkspaceId),
        innovationApi.getProductConcepts(activeWorkspaceId),
        innovationApi.getBusinessCases(activeWorkspaceId),
        innovationApi.getPRDs(activeWorkspaceId),
        innovationApi.getGateReviews(activeWorkspaceId),
        innovationApi.getPortfolio(activeWorkspaceId)
      ]);

      setOverview(overviewRes);
      setWorkspaces(workspacesRes);
      setProblems(problemsRes);
      setOpportunities(oppsRes);
      setIdeas(ideasRes);
      setHypotheses(hypoRes);
      setAssumptions(asmpRes);
      setExperiments(expRes);
      setLearnings(learnRes);
      setConcepts(conceptsRes);
      setBusinessCases(bcaseRes);
      setPrds(prdsRes);
      setGateReviews(gatesRes);
      setPortfolio(portfolioRes);
    } catch (err: any) {
      setError(err?.message || 'Failed to load innovation platform data');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProblem = async (statement: string, affectedUsers: string, severity: number, wtp: number) => {
    const newProb = await innovationApi.createProblem({
      workspace_id: activeWorkspaceId,
      statement,
      affected_users: affectedUsers,
      severity,
      willingness_to_pay: wtp,
      frequency: 'WEEKLY'
    });
    setProblems(prev => [newProb, ...prev]);
  };

  const handleCreateOpportunity = async (problemId: string, marketSizeUsd: number) => {
    const newOpp = await innovationApi.createOpportunity({
      workspace_id: activeWorkspaceId,
      problem_id: problemId,
      market_size_usd: marketSizeUsd
    });
    setOpportunities(prev => [newOpp, ...prev]);
  };

  const handleEvaluateGate = async (gateStage: GateStage, checklist: Record<string, boolean>) => {
    const review = await innovationApi.evaluateGate({
      workspace_id: activeWorkspaceId,
      gate_stage: gateStage,
      checklist,
      reviewed_by: 'Human Decision Committee'
    });
    setGateReviews(prev => [review, ...prev.filter(r => r.gate_stage !== gateStage)]);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 sm:p-6 lg:p-8 space-y-6">
      {/* Header & Workspace Switcher */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-3">
            <span className="px-2.5 py-1 rounded-md bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
              Phase 55
            </span>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-indigo-300">
              Unified Product & Innovation Intelligence Platform
            </h1>
          </div>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 max-w-3xl">
            Empirical R&D operating loop transforming customer observations into validated problems, transparently scored ideas, rigorous statistical experiments, and stage-gated product launches.
          </p>
        </div>

        {/* Workspace selector */}
        <div className="flex items-center gap-3 bg-slate-900/80 border border-slate-800 p-2 rounded-xl">
          <span className="text-xs text-slate-400 font-medium pl-1">Workspace:</span>
          <select
            value={activeWorkspaceId}
            onChange={e => setActiveWorkspaceId(e.target.value)}
            className="bg-slate-950 border border-slate-700/80 text-xs text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            {workspaces.map(w => (
              <option key={w.id || w.workspace_id} value={w.id || w.workspace_id}>
                {w.title} ({w.stage_gate || w.stage || 'GATE_0'})
              </option>
            ))}
          </select>
          <button
            onClick={loadAllData}
            className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-slate-200 transition-colors"
            title="Refresh Data"
          >
            ↻
          </button>
        </div>
      </div>

      {/* Metrics Banner */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/60">
          <div className="text-[10px] uppercase font-semibold text-slate-400">Total Workspaces</div>
          <div className="text-xl font-bold text-slate-100 mt-1">{overview?.total_workspaces ?? 1}</div>
        </div>
        <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/60">
          <div className="text-[10px] uppercase font-semibold text-slate-400">Validated Problems</div>
          <div className="text-xl font-bold text-amber-400 mt-1">{(overview as any)?.validated_problems ?? overview?.total_problems_cataloged ?? problems.length}</div>
        </div>
        <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/60">
          <div className="text-[10px] uppercase font-semibold text-slate-400">Ideas Scored</div>
          <div className="text-xl font-bold text-indigo-400 mt-1">{(overview as any)?.total_ideas ?? overview?.total_ideas_generated ?? ideas.length}</div>
        </div>
        <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/60">
          <div className="text-[10px] uppercase font-semibold text-slate-400">Running Experiments</div>
          <div className="text-xl font-bold text-cyan-400 mt-1">{overview?.active_experiments_count ?? (overview as any)?.active_experiments ?? experiments.length}</div>
        </div>
        <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/60">
          <div className="text-[10px] uppercase font-semibold text-slate-400">Active PRDs</div>
          <div className="text-xl font-bold text-emerald-400 mt-1">{(overview as any)?.active_prds ?? prds.length}</div>
        </div>
        <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/60">
          <div className="text-[10px] uppercase font-semibold text-slate-400">Avg Portfolio ROI</div>
          <div className="text-xl font-bold text-purple-400 mt-1">3.8x</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800 text-xs">
        {[
          { key: 'problems', label: '1. Problems & Opps', count: problems.length },
          { key: 'ideas', label: '2. Idea Scoring', count: ideas.length },
          { key: 'assumptions', label: '3. Assumption Mapping', count: assumptions.length },
          { key: 'experiments', label: '4. Empirical Experiments', count: experiments.length },
          { key: 'concepts', label: '5. Product Concepts & PRD', count: concepts.length },
          { key: 'gates', label: '6. Stage-Gate Reviews', count: gateReviews.length },
          { key: 'portfolio', label: '7. Horizon Portfolio' },
          { key: 'copilot', label: 'AI Innovation Copilot' }
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as TabKey)}
            className={`px-3.5 py-2 rounded-lg font-medium whitespace-nowrap transition-all flex items-center gap-1.5 ${
              activeTab === tab.key
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                : 'bg-slate-900/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            <span>{tab.label}</span>
            {tab.count !== undefined && (
              <span className="px-1.5 py-0.2 rounded-full text-[10px] bg-slate-950/60 border border-slate-700/50">
                {tab.count}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Main Content Area */}
      {error ? (
        <div className="p-6 rounded-xl bg-rose-950/30 border border-rose-800 text-rose-300 text-xs">
          {error}
        </div>
      ) : (
        <div>
          {activeTab === 'problems' && (
            <ProblemBoard
              problems={problems}
            />
          )}

          {activeTab === 'ideas' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-slate-100">Innovation Ideas & 11-Factor Scoring</h3>
                  <p className="text-xs text-slate-400">
                    Transparent formula exposing customer value, market potential, feasibility, and evidence strength weights.
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {ideas.map(idea => (
                  <IdeaCard
                    key={idea.id || idea.idea_id}
                    idea={idea}
                  />
                ))}
              </div>
            </div>
          )}

          {activeTab === 'assumptions' && (
            <AssumptionMatrix
              assumptions={assumptions}
            />
          )}

          {activeTab === 'experiments' && (
            <ExperimentRunner
              experiments={experiments}
              learnings={learnings}
            />
          )}

          {activeTab === 'concepts' && (
            <div className="space-y-6">
              {concepts.map(concept => (
                <ProductConceptViewer
                  key={concept.id || concept.concept_id}
                  concept={concept}
                />
              ))}
            </div>
          )}

          {activeTab === 'gates' && (
            <GateReviewPanel
              reviews={gateReviews}
              onEvaluateGate={handleEvaluateGate}
            />
          )}

          {activeTab === 'portfolio' && (
            <PortfolioHorizonChart
              portfolio={portfolio ?? undefined}
            />
          )}

          {activeTab === 'copilot' && (
            <InnovationCopilot workspaceId={activeWorkspaceId} />
          )}
        </div>
      )}
    </div>
  );
};
