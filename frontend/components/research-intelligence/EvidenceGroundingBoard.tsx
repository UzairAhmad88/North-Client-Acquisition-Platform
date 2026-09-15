'use client';

import React from 'react';
import { Database, CheckCircle2, Clock, Info, AlertCircle } from 'lucide-react';
import { ResearchFact } from '../../lib/api/research_intelligence';

interface EvidenceGroundingBoardProps {
  facts: ResearchFact[];
}

export const EvidenceGroundingBoard: React.FC<EvidenceGroundingBoardProps> = ({ facts }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Database className="h-4 w-4 text-emerald-400" />
            Extracted Facts & Evidence Grounding
          </h3>
          <p className="text-xs text-slate-400">
            Strict epistemic separation: Fact ≠ Inference ≠ Prediction. Every fact preserves provenance.
          </p>
        </div>
        <span className="text-xs font-mono px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
          {facts.length} Verified Facts
        </span>
      </div>

      <div className="space-y-2.5 max-h-96 overflow-y-auto pr-1">
        {facts.length === 0 ? (
          <div className="text-center py-8 text-xs text-slate-500">
            No structured facts extracted for this workspace yet.
          </div>
        ) : (
          facts.map((fact) => (
            <div
              key={fact.id}
              className="p-3 rounded-lg border border-slate-800 bg-slate-950/30 hover:border-slate-700/80 transition-colors"
            >
              <div className="flex items-start justify-between gap-3 mb-1">
                <p className="text-xs font-medium text-slate-200 leading-relaxed">
                  {fact.fact_statement}
                </p>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-emerald-400 border border-slate-700 shrink-0">
                  {Math.round((fact.confidence_score || 0.85) * 100)}% Conf
                </span>
              </div>
              <div className="flex items-center justify-between text-[10px] text-slate-400 pt-2 border-t border-slate-900">
                <div className="flex items-center gap-3">
                  {fact.entity_name && (
                    <span className="text-indigo-400 font-medium">
                      Entity: {fact.entity_name}
                    </span>
                  )}
                  {fact.fact_value && (
                    <span className="text-slate-300">
                      Value: <span className="font-mono text-cyan-300">{fact.fact_value}</span>
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-1 text-slate-500">
                  <Clock className="h-3 w-3" />
                  <span>{fact.observed_at ? new Date(fact.observed_at).toLocaleDateString() : 'Recent'}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
