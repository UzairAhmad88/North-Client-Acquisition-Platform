'use client';

import React from 'react';
import { FlaskConical, CheckCircle2, AlertOctagon, TrendingUp, BookOpen } from 'lucide-react';
import { InnovationExperiment, InnovationLearning } from '../../lib/api/innovation';

interface ExperimentRunnerProps {
  experiments: InnovationExperiment[];
  learnings: InnovationLearning[];
}

export const ExperimentRunner: React.FC<ExperimentRunnerProps> = ({ experiments, learnings }) => {
  return (
    <div className="space-y-6">
      {/* Experiments Section */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <FlaskConical className="h-4 w-4 text-cyan-400" />
              Empirical Experiments & Validation Tests
            </h3>
            <p className="text-xs text-slate-400">
              A/B tests, prototypes, surveys, and pricing experiments with statistical significance checks.
            </p>
          </div>
          <span className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 text-slate-300 border border-slate-700">
            {experiments.length} Active Experiments
          </span>
        </div>

        <div className="space-y-3">
          {experiments.length === 0 ? (
            <div className="text-center py-8 text-xs text-slate-500">
              No validation experiments designed for this workspace yet.
            </div>
          ) : (
            experiments.map((exp) => (
              <div
                key={exp.id}
                className="p-4 rounded-lg border border-slate-800 bg-slate-950/40 hover:border-slate-700 transition-colors"
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-semibold mr-2">
                      {exp.experiment_type}
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-semibold">
                      {exp.status}
                    </span>
                    <h4 className="text-xs font-bold text-white mt-1.5">{exp.title}</h4>
                  </div>
                  <div className="text-right text-[10px] text-slate-500 font-mono">
                    <div>N = {exp.sample_size} sample</div>
                    <div>{exp.duration_days} days</div>
                  </div>
                </div>

                <div className="flex items-center justify-between text-[10px] text-slate-400 pt-2 border-t border-slate-900">
                  <span>Method: <span className="text-slate-300 font-mono">{exp.statistical_method}</span></span>
                  <span className="text-indigo-400">Governance Approved</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Structured Learnings Section */}
      {learnings.length > 0 && (
        <div className="rounded-xl border border-indigo-900/40 bg-indigo-950/10 p-5 backdrop-blur-sm">
          <h3 className="text-sm font-bold text-indigo-300 flex items-center gap-2 mb-3">
            <BookOpen className="h-4 w-4 text-indigo-400" />
            Structured Organizational Learnings ({learnings.length})
          </h3>

          <div className="space-y-2.5">
            {learnings.map((lrn) => (
              <div key={lrn.id} className="p-3 rounded-lg border border-indigo-800/40 bg-slate-950/60">
                <div className="flex items-start gap-2 text-xs text-white font-medium mb-1">
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 mt-0.5 shrink-0" />
                  <span>{lrn.insight_statement}</span>
                </div>
                <p className="text-[11px] text-slate-400 pl-5.5 mb-1">
                  <span className="text-slate-300 font-medium">Evidence:</span> {lrn.evidence_summary}
                </p>
                {lrn.strategic_implication && (
                  <p className="text-[10px] text-indigo-300 pl-5.5 italic">
                    Strategic Implication: {lrn.strategic_implication}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
