'use client';

import React from 'react';
import { Package, Layers, DollarSign, CheckCircle2, ShieldCheck, ArrowRight } from 'lucide-react';
import { InnovationProductConcept } from '../../lib/api/innovation';

interface ProductConceptViewerProps {
  concept: InnovationProductConcept;
}

export const ProductConceptViewer: React.FC<ProductConceptViewerProps> = ({ concept }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 backdrop-blur-sm">
      <div className="flex items-start justify-between gap-4 pb-4 border-b border-slate-800 mb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-semibold">
              {concept.business_model_type}
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-semibold">
              {concept.status}
            </span>
          </div>
          <h2 className="text-lg font-bold text-white">{concept.name}</h2>
          <p className="text-xs text-slate-400 mt-1">
            Target Persona: <span className="text-slate-200 font-medium">{concept.target_customer_persona}</span>
          </p>
        </div>
      </div>

      {/* Value Proposition */}
      <div className="mb-4">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-1.5">Value Proposition</h3>
        <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/40 p-3 rounded-lg border border-slate-800">
          {concept.value_proposition}
        </p>
      </div>

      {/* Core Features & Differentiators */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
          <h4 className="text-xs font-bold text-slate-300 mb-2 flex items-center gap-1.5">
            <Layers className="h-3.5 w-3.5 text-indigo-400" />
            Core Features
          </h4>
          <ul className="space-y-1 text-xs text-slate-300">
            {(concept.core_features || ['Multi-channel ingestion', 'Fact validation engine']).map((f, i) => (
              <li key={i} className="flex items-center gap-1.5">
                <CheckCircle2 className="h-3 w-3 text-emerald-400 shrink-0" />
                <span>{f}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
          <h4 className="text-xs font-bold text-slate-300 mb-2 flex items-center gap-1.5">
            <ShieldCheck className="h-3.5 w-3.5 text-cyan-400" />
            Core Differentiators
          </h4>
          <ul className="space-y-1 text-xs text-slate-300">
            {(concept.differentiators || ['Deterministic safety bounds', 'Zero hallucination guarantee']).map((d, i) => (
              <li key={i} className="flex items-center gap-1.5">
                <CheckCircle2 className="h-3 w-3 text-cyan-400 shrink-0" />
                <span>{d}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {concept.technical_architecture_notes && (
        <div className="text-[11px] text-slate-400 bg-slate-950/20 p-2.5 rounded border border-slate-800/80">
          <span className="text-slate-300 font-semibold">Technical Architecture:</span> {concept.technical_architecture_notes}
        </div>
      )}
    </div>
  );
};
