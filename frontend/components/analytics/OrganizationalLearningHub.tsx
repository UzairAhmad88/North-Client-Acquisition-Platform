'use client';

import React, { useState } from 'react';
import { BusinessInsight, BusinessRecommendation, Experiment, analyticsApi } from '@/lib/api/analytics';

interface OrganizationalLearningHubProps {
  insights: BusinessInsight[];
  recommendations: BusinessRecommendation[];
  experiments: Experiment[];
  onRefresh: () => void;
}

export const OrganizationalLearningHub: React.FC<OrganizationalLearningHubProps> = ({
  insights,
  recommendations,
  experiments,
  onRefresh,
}) => {
  const [activeTab, setActiveTab] = useState<'insights' | 'recommendations' | 'experiments'>('insights');
  const [evaluatingExpId, setEvaluatingExpId] = useState<string | null>(null);
  const [evalResult, setEvalResult] = useState<any | null>(null);

  const handleReviewInsight = async (id: string, action: string) => {
    await analyticsApi.reviewInsight(id, action);
    onRefresh();
  };

  const handleReviewRecommendation = async (id: string, action: string) => {
    await analyticsApi.reviewRecommendation(id, action);
    onRefresh();
  };

  const handleEvaluateExperiment = async (expId: string) => {
    setEvaluatingExpId(expId);
    try {
      const res = await analyticsApi.evaluateExperiment(expId);
      setEvalResult(res);
      onRefresh();
    } finally {
      setEvaluatingExpId(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Sub-Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-zinc-800 pb-3">
        <button
          onClick={() => setActiveTab('insights')}
          className={`px-4 py-2 text-sm font-semibold rounded-lg transition-colors ${
            activeTab === 'insights'
              ? 'bg-indigo-600 text-white'
              : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60'
          }`}
        >
          Discovered Insights ({insights.length})
        </button>
        <button
          onClick={() => setActiveTab('recommendations')}
          className={`px-4 py-2 text-sm font-semibold rounded-lg transition-colors ${
            activeTab === 'recommendations'
              ? 'bg-indigo-600 text-white'
              : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60'
          }`}
        >
          Human Recommendations ({recommendations.length})
        </button>
        <button
          onClick={() => setActiveTab('experiments')}
          className={`px-4 py-2 text-sm font-semibold rounded-lg transition-colors ${
            activeTab === 'experiments'
              ? 'bg-indigo-600 text-white'
              : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/60'
          }`}
        >
          Continuous Experiments ({experiments.length})
        </button>
      </div>

      {/* Tab 1: Insights with Evidence */}
      {activeTab === 'insights' && (
        <div className="space-y-4">
          {insights.length === 0 ? (
            <div className="p-8 text-center text-zinc-500 bg-zinc-900/40 border border-zinc-800 rounded-xl">
              No organizational insights recorded yet.
            </div>
          ) : (
            insights.map((ins) => (
              <div key={ins.id} className="p-6 bg-zinc-900/80 border border-zinc-800 rounded-xl space-y-4">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded">
                        {ins.category}
                      </span>
                      <span className="text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-medium">
                        Confidence: {ins.confidence}
                      </span>
                      <span className="text-xs text-zinc-400">Sample: {ins.sample_size}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-zinc-800/80 text-zinc-400">
                        Status: {ins.status}
                      </span>
                    </div>
                    <h4 className="text-base font-bold text-zinc-100 mt-2">{ins.title}</h4>
                    <p className="text-sm text-zinc-300 mt-1">{ins.description}</p>
                  </div>
                  {ins.status === 'PENDING_REVIEW' && (
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleReviewInsight(ins.id, 'ACCEPT')}
                        className="px-3 py-1.5 text-xs bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded"
                      >
                        Accept
                      </button>
                      <button
                        onClick={() => handleReviewInsight(ins.id, 'REJECT')}
                        className="px-3 py-1.5 text-xs bg-rose-600 hover:bg-rose-500 text-white font-semibold rounded"
                      >
                        Reject
                      </button>
                    </div>
                  )}
                </div>

                {/* Evidence Items */}
                {ins.evidence_items && ins.evidence_items.length > 0 && (
                  <div className="mt-3 p-4 bg-zinc-950/80 border border-zinc-800/60 rounded-lg text-xs space-y-2">
                    <p className="font-semibold text-zinc-300">Empirical Evidence Grounding:</p>
                    {ins.evidence_items.map((ev) => (
                      <div key={ev.id} className="text-zinc-400 flex items-center justify-between">
                        <span>Source: {ev.source_type} (n={ev.sample_count})</span>
                        {ev.variance_pct !== undefined && ev.variance_pct !== null && (
                          <span className="font-semibold text-amber-400">Variance: {ev.variance_pct}%</span>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* Tab 2: Recommendations with Decisions */}
      {activeTab === 'recommendations' && (
        <div className="space-y-4">
          {recommendations.length === 0 ? (
            <div className="p-8 text-center text-zinc-500 bg-zinc-900/40 border border-zinc-800 rounded-xl">
              No recommendations currently pending decision.
            </div>
          ) : (
            recommendations.map((rec) => (
              <div key={rec.id} className="p-6 bg-zinc-900/80 border border-zinc-800 rounded-xl space-y-4">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded">
                        Target Workflow: {rec.affected_workflow}
                      </span>
                      <span className="text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-medium">
                        Status: {rec.status}
                      </span>
                    </div>
                    <h4 className="text-base font-bold text-zinc-100 mt-2">{rec.title}</h4>
                    <p className="text-sm text-zinc-300 mt-1 font-medium">Recommendation: {rec.recommendation}</p>
                    <p className="text-xs text-zinc-400 mt-1">Reason: {rec.reason}</p>
                  </div>
                  {rec.status === 'PENDING_APPROVAL' && (
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleReviewRecommendation(rec.id, 'APPROVE')}
                        className="px-3 py-1.5 text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded"
                      >
                        Approve
                      </button>
                      <button
                        onClick={() => handleReviewRecommendation(rec.id, 'REJECT')}
                        className="px-3 py-1.5 text-xs bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-semibold rounded"
                      >
                        Reject
                      </button>
                    </div>
                  )}
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-2 text-xs">
                  <div className="p-3 bg-emerald-950/20 border border-emerald-500/20 rounded-lg text-emerald-300">
                    <span className="font-semibold block mb-1">Expected Benefit:</span>
                    {rec.expected_benefit}
                  </div>
                  <div className="p-3 bg-amber-950/20 border border-amber-500/20 rounded-lg text-amber-300">
                    <span className="font-semibold block mb-1">Potential Downside / Tradeoff:</span>
                    {rec.potential_downside}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Tab 3: Experiments */}
      {activeTab === 'experiments' && (
        <div className="space-y-4">
          {evalResult && (
            <div className="p-4 bg-indigo-950/40 border border-indigo-500/40 rounded-xl text-sm text-indigo-200">
              <p className="font-bold mb-1">Statistical Hypothesis Evaluation:</p>
              <p>{evalResult.conclusion}</p>
            </div>
          )}

          {experiments.length === 0 ? (
            <div className="p-8 text-center text-zinc-500 bg-zinc-900/40 border border-zinc-800 rounded-xl">
              No continuous improvement experiments active.
            </div>
          ) : (
            experiments.map((exp) => (
              <div key={exp.id} className="p-6 bg-zinc-900/80 border border-zinc-800 rounded-xl space-y-3">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded">
                        {exp.target_workflow}
                      </span>
                      <span className="text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-medium">
                        Status: {exp.status}
                      </span>
                      <span className="text-xs text-zinc-400">
                        Trials: {exp.current_sample_count}/{exp.sample_target}
                      </span>
                    </div>
                    <h4 className="text-base font-bold text-zinc-100 mt-2">{exp.title}</h4>
                    <p className="text-sm text-zinc-300 mt-1 italic">"{exp.hypothesis}"</p>
                  </div>
                  <button
                    onClick={() => handleEvaluateExperiment(exp.id)}
                    disabled={evaluatingExpId === exp.id}
                    className="px-3.5 py-1.5 text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded disabled:opacity-50"
                  >
                    {evaluatingExpId === exp.id ? 'Evaluating...' : 'Evaluate Hypothesis'}
                  </button>
                </div>

                <div className="flex items-center gap-6 text-xs text-zinc-400 pt-2 border-t border-zinc-800/60">
                  <span>Target Metric: <strong className="text-zinc-200">{exp.target_metric}</strong></span>
                  <span>Baseline: <strong className="text-zinc-200">{exp.baseline_value}</strong></span>
                  <span>Target: <strong className="text-emerald-400">{exp.target_value}</strong></span>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};
