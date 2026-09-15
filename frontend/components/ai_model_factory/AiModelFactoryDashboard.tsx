'use client';

import React, { useState, useEffect } from 'react';
import {
  aiModelFactoryApi,
  AiFactoryOverviewMetrics,
  AiProjectItem,
  AiModelItem,
  AiExperimentItem,
  AiDeploymentItem,
  AiPromptItem,
  AiDriftEventItem,
} from '@/lib/api/aiModelFactory';
import { AiFactoryOverviewMetricsView } from './AiFactoryOverviewMetrics';
import { ProjectsExperimentsTrainingView } from './ProjectsExperimentsTrainingView';
import { ModelRegistryArtifactsView } from './ModelRegistryArtifactsView';
import { EvaluationBenchmarksJudgeView } from './EvaluationBenchmarksJudgeView';
import { PromptsRagopsAgentopsView } from './PromptsRagopsAgentopsView';
import { DeploymentsInferenceRoutingView } from './DeploymentsInferenceRoutingView';
import { MonitoringDriftRetrainingView } from './MonitoringDriftRetrainingView';
import { GovernanceModelCardsSafetyView } from './GovernanceModelCardsSafetyView';
import { GpuFinopsDigitalTwinView } from './GpuFinopsDigitalTwinView';
import { AiFactoryCopilot } from './AiFactoryCopilot';

type TabType =
  | 'overview'
  | 'projects_experiments'
  | 'model_registry'
  | 'evaluation_benchmarks'
  | 'prompts_ragops'
  | 'deployments_inference'
  | 'drift_monitoring'
  | 'governance_safety'
  | 'gpu_finops_twin'
  | 'copilot';

export const AiModelFactoryDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState<AiFactoryOverviewMetrics | null>(null);
  const [projects, setProjects] = useState<AiProjectItem[]>([]);
  const [models, setModels] = useState<AiModelItem[]>([]);
  const [experiments, setExperiments] = useState<AiExperimentItem[]>([]);
  const [deployments, setDeployments] = useState<AiDeploymentItem[]>([]);
  const [prompts, setPrompts] = useState<AiPromptItem[]>([]);
  const [driftEvents, setDriftEvents] = useState<AiDriftEventItem[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [m, proj, mdl, exp, dep, prm, drf] = await Promise.all([
          aiModelFactoryApi.getOverview(),
          aiModelFactoryApi.getProjects(),
          aiModelFactoryApi.getModels(),
          aiModelFactoryApi.getExperiments(),
          aiModelFactoryApi.getDeployments(),
          aiModelFactoryApi.getPrompts(),
          aiModelFactoryApi.getDriftEvents(),
        ]);
        setMetrics(m);
        setProjects(proj);
        setModels(mdl);
        setExperiments(exp);
        setDeployments(dep);
        setPrompts(prm);
        setDriftEvents(drf);
      } catch (err) {
        console.error('Error loading AI Model Factory dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const navTabs: { id: TabType; label: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'projects_experiments', label: 'Projects & Sweeps' },
    { id: 'model_registry', label: 'Model Registry' },
    { id: 'evaluation_benchmarks', label: 'Evaluation & Benchmarks' },
    { id: 'prompts_ragops', label: 'Prompts & RAGOps' },
    { id: 'deployments_inference', label: 'Deployments & Routes' },
    { id: 'drift_monitoring', label: 'Drift & Retraining' },
    { id: 'governance_safety', label: 'Governance & Safety' },
    { id: 'gpu_finops_twin', label: 'GPU & FinOps Twin' },
    { id: 'copilot', label: 'AI Copilot' },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 font-mono text-xs font-bold">
              PHASE 63
            </span>
            <h1 className="text-2xl font-bold text-white tracking-tight">AI Model Factory & MLOps OS</h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Centralized Model Factory, MLOps, LLMOps, Benchmarking, Policy-Routed Inference, Drift Detection, and AI FinOps.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            MLOps Active
          </span>
        </div>
      </div>

      {/* Top Level Metric KPIs */}
      <AiFactoryOverviewMetricsView metrics={metrics} loading={loading} />

      {/* Navigation Tabs */}
      <div className="flex overflow-x-auto gap-1 border-b border-slate-800 pb-1 scrollbar-none">
        {navTabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3.5 py-2 rounded-t-lg text-xs font-medium whitespace-nowrap transition-colors ${
              activeTab === tab.id
                ? 'bg-slate-800 text-white border-b-2 border-indigo-500 font-bold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Panels */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <ProjectsExperimentsTrainingView projects={projects} experiments={experiments} />
          <ModelRegistryArtifactsView models={models} />
          <EvaluationBenchmarksJudgeView />
        </div>
      )}

      {activeTab === 'projects_experiments' && (
        <ProjectsExperimentsTrainingView projects={projects} experiments={experiments} />
      )}

      {activeTab === 'model_registry' && <ModelRegistryArtifactsView models={models} />}

      {activeTab === 'evaluation_benchmarks' && <EvaluationBenchmarksJudgeView />}

      {activeTab === 'prompts_ragops' && <PromptsRagopsAgentopsView prompts={prompts} />}

      {activeTab === 'deployments_inference' && (
        <DeploymentsInferenceRoutingView deployments={deployments} />
      )}

      {activeTab === 'drift_monitoring' && (
        <MonitoringDriftRetrainingView driftEvents={driftEvents} />
      )}

      {activeTab === 'governance_safety' && <GovernanceModelCardsSafetyView />}

      {activeTab === 'gpu_finops_twin' && <GpuFinopsDigitalTwinView />}

      {activeTab === 'copilot' && <AiFactoryCopilot />}
    </div>
  );
};
