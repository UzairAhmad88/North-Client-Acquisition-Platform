'use client';

import React, { useState } from 'react';
import { DiscoverySessionDetail } from '@/lib/api/requirements';
import { ReadinessIndicator } from './ReadinessIndicator';
import { RequirementsList } from './RequirementsList';
import { DiscoveryQuestions } from './DiscoveryQuestions';
import { ScopePanel } from './ScopePanel';

interface RequirementsWorkspaceProps {
  sessionDetail: DiscoverySessionDetail;
  onAnalyze?: () => void;
  onConfirmRequirement?: (reqId: string) => void;
  onAnswerQuestion?: (qId: string, answerText: string) => void;
  isAnalyzing?: boolean;
}

export function RequirementsWorkspace({
  sessionDetail,
  onAnalyze,
  onConfirmRequirement,
  onAnswerQuestion,
  isAnalyzing,
}: RequirementsWorkspaceProps) {
  const [activeTab, setActiveTab] = useState<'REQUIREMENTS' | 'QUESTIONS' | 'SCOPE'>('REQUIREMENTS');

  return (
    <div className="space-y-6">
      {/* Top Header Card */}
      <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-xl font-bold text-slate-100">Discovery Workspace</h2>
            <span className="rounded-full bg-indigo-500/20 px-3 py-1 text-xs font-semibold text-indigo-300 border border-indigo-500/30">
              v{sessionDetail.version}
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-400">
            Session ID: {sessionDetail.id} | Business ID: {sessionDetail.business_id}
          </p>
        </div>

        {onAnalyze && (
          <button
            onClick={onAnalyze}
            disabled={isAnalyzing}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-lg hover:bg-indigo-500 disabled:opacity-50 transition-all"
          >
            {isAnalyzing ? 'Analyzing Discovery Session...' : 'Analyze Discovery Session'}
          </button>
        )}
      </div>

      {/* Readiness Gauge */}
      <ReadinessIndicator
        readinessStage={sessionDetail.readiness_stage}
        readinessScore={sessionDetail.readiness_score}
        completenessScore={sessionDetail.completeness_score}
        scopeComplexity={sessionDetail.scope_complexity}
      />

      {/* Workspace Tabs */}
      <div className="border-b border-slate-800">
        <div className="flex gap-6 text-sm font-semibold">
          <button
            onClick={() => setActiveTab('REQUIREMENTS')}
            className={`pb-3 border-b-2 transition-colors ${
              activeTab === 'REQUIREMENTS'
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Requirements ({sessionDetail.requirements?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab('QUESTIONS')}
            className={`pb-3 border-b-2 transition-colors ${
              activeTab === 'QUESTIONS'
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Discovery Questions ({sessionDetail.questions?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab('SCOPE')}
            className={`pb-3 border-b-2 transition-colors ${
              activeTab === 'SCOPE'
                ? 'border-indigo-500 text-indigo-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Scope Matrix ({sessionDetail.scope_items?.length || 0})
          </button>
        </div>
      </div>

      {/* Tab Panels */}
      {activeTab === 'REQUIREMENTS' && (
        <RequirementsList
          requirements={sessionDetail.requirements}
          onConfirmRequirement={onConfirmRequirement}
        />
      )}

      {activeTab === 'QUESTIONS' && (
        <DiscoveryQuestions
          questions={sessionDetail.questions}
          onAnswerQuestion={onAnswerQuestion}
        />
      )}

      {activeTab === 'SCOPE' && <ScopePanel scopeItems={sessionDetail.scope_items} />}
    </div>
  );
}
