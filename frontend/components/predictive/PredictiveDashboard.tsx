'use client';

import React from 'react';
import { PredictionRecord } from '@/lib/api/predictive';

interface PredictiveDashboardProps {
  predictions: PredictionRecord[];
  loading: boolean;
  onRefresh: () => void;
  onTriggerInference: () => void;
}

export const PredictiveDashboard: React.FC<PredictiveDashboardProps> = ({
  predictions,
  loading,
  onRefresh,
  onTriggerInference,
}) => {
  if (loading && predictions.length === 0) {
    return (
      <div className="p-8 text-center text-zinc-400">
        <div className="inline-block animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mb-3"></div>
        <p>Loading Predictive Operations Intelligence...</p>
      </div>
    );
  }

  const highRiskCount = predictions.filter((p) => p.risk_band === 'HIGH' || p.risk_band === 'CRITICAL').length;
  const leadConversions = predictions.filter((p) => p.prediction_type === 'LEAD_CONVERSION');
  const projectDelays = predictions.filter((p) => p.prediction_type === 'PROJECT_DELAY');
  const effortVariances = predictions.filter((p) => p.prediction_type === 'PROJECT_EFFORT_VARIANCE');

  return (
    <div className="space-y-6">
      {/* Top Banner & Control Actions */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-zinc-100">Predictive Operations Command Radar</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20">
              Probabilistic Decision Support
            </span>
          </div>
          <p className="text-sm text-zinc-400 mt-1">
            Real-time inference without autonomous policy change: Prediction $\neq$ Recommendation $\neq$ Decision $\neq$ Action.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={onRefresh}
            className="px-3.5 py-2 text-sm bg-zinc-800 hover:bg-zinc-700 text-zinc-200 rounded-lg transition-colors border border-zinc-700/60 font-medium"
          >
            Refresh
          </button>
          <button
            onClick={onTriggerInference}
            className="px-4 py-2 text-sm bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white rounded-lg transition-all font-semibold shadow-md shadow-purple-500/20"
          >
            Run Predictive Inference
          </button>
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Total Active Predictions</p>
          <p className="text-3xl font-extrabold text-zinc-100 mt-2">{predictions.length}</p>
          <p className="text-xs text-zinc-500 mt-1">Point-in-time point models</p>
        </div>

        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">High Risk Signals</p>
          <p className="text-3xl font-extrabold text-rose-400 mt-2">{highRiskCount}</p>
          <p className="text-xs text-zinc-500 mt-1">Requires human review</p>
        </div>

        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Lead Conversion Models</p>
          <p className="text-3xl font-extrabold text-emerald-400 mt-2">{leadConversions.length}</p>
          <p className="text-xs text-zinc-500 mt-1">Calibrated probability bands</p>
        </div>

        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-5">
          <p className="text-xs font-semibold uppercase tracking-wider text-zinc-400">Project Delay Models</p>
          <p className="text-3xl font-extrabold text-amber-400 mt-2">{projectDelays.length}</p>
          <p className="text-xs text-zinc-500 mt-1">Blocker & dependency analysis</p>
        </div>
      </div>

      {/* Predictions Stream */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-zinc-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-purple-500 animate-pulse"></span>
            Recent Predictive Signals & Calibrated Explanations
          </h3>
          <span className="text-xs text-zinc-400">Evidence Grounded • Non-Deterministic</span>
        </div>

        {predictions.length === 0 ? (
          <p className="text-sm text-zinc-500 italic">No predictions generated yet. Click "Run Predictive Inference".</p>
        ) : (
          <div className="space-y-4">
            {predictions.map((p) => (
              <div
                key={p.id}
                className="p-5 bg-zinc-950/70 border border-zinc-800/80 rounded-lg hover:border-zinc-700 transition-colors space-y-3"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="px-2 py-0.5 text-xs font-bold bg-purple-500/10 text-purple-400 border border-purple-500/20 rounded">
                        {p.prediction_type}
                      </span>
                      <span
                        className={`px-2 py-0.5 text-xs font-bold rounded ${
                          p.risk_band === 'CRITICAL' || p.risk_band === 'HIGH'
                            ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                            : p.risk_band === 'MEDIUM'
                            ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                            : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        }`}
                      >
                        {p.risk_band} RISK
                      </span>
                      <span className="text-xs text-zinc-400">Entity: {p.entity_id}</span>
                      <span className="text-xs text-zinc-500">Model: {p.model_version}</span>
                    </div>
                    <div className="mt-2 flex items-baseline gap-3">
                      <span className="text-2xl font-extrabold text-zinc-100">
                        {Math.round(p.probability * 100)}% Estimated Likelihood
                      </span>
                      {p.confidence_interval && (
                        <span className="text-xs text-zinc-400">
                          (Confidence Interval: {Math.round((p.confidence_interval.lower || 0) * 100)}% –{' '}
                          {Math.round((p.confidence_interval.upper || 0) * 100)}%)
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Explanation and Key Drivers */}
                {p.explanation && (
                  <div className="p-3 bg-zinc-900/60 border border-zinc-800/60 rounded-md text-xs space-y-2">
                    <p className="text-zinc-300 font-medium">{p.explanation.summary_text}</p>
                    {p.explanation.key_drivers && p.explanation.key_drivers.length > 0 && (
                      <div className="flex flex-wrap gap-2 pt-1 border-t border-zinc-800/60">
                        {p.explanation.key_drivers.map((drv, i) => (
                          <span key={i} className="px-2 py-0.5 bg-zinc-800 text-zinc-300 rounded font-mono text-xs">
                            {drv.feature}: {String(drv.value)} ({drv.impact})
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
