'use client';

import React, { useState } from 'react';
import { ListFilter, Calculator, ArrowUpDown, CheckCircle, Sparkles } from 'lucide-react';
import { ProductEpic, ProductFeature, ProductBacklogItem } from '../../lib/api/productManagement';

interface BacklogPrioritizerProps {
  epics: ProductEpic[];
  features: ProductFeature[];
  items: ProductBacklogItem[];
  onScoreItem?: (itemId: string, framework: string, inputs: Record<string, number>) => void;
}

export const BacklogPrioritizer: React.FC<BacklogPrioritizerProps> = ({
  epics,
  features,
  items,
  onScoreItem,
}) => {
  const [activeFramework, setActiveFramework] = useState<'RICE' | 'WSJF'>('RICE');

  return (
    <div className="space-y-4">
      {/* Header controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 rounded-xl border border-slate-800 bg-slate-900/60">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <ListFilter className="h-4 w-4 text-indigo-400" />
            Product Backlog & Prioritization Engine
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Total Backlog Items: {items.length} | Epics: {epics.length} | Features: {features.length}
          </p>
        </div>

        <div className="flex items-center gap-2 bg-slate-950/60 p-1 rounded-lg border border-slate-800">
          <button
            onClick={() => setActiveFramework('RICE')}
            className={`px-3 py-1 text-xs font-semibold rounded-md transition-colors ${
              activeFramework === 'RICE'
                ? 'bg-indigo-600 text-white shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            RICE Score
          </button>
          <button
            onClick={() => setActiveFramework('WSJF')}
            className={`px-3 py-1 text-xs font-semibold rounded-md transition-colors ${
              activeFramework === 'WSJF'
                ? 'bg-indigo-600 text-white shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            WSJF (SAFe)
          </button>
        </div>
      </div>

      {/* Backlog Item List */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 overflow-hidden">
        <div className="px-4 py-3 border-b border-slate-800 bg-slate-950/40 text-xs font-bold text-slate-300 uppercase tracking-wider grid grid-cols-12 gap-2">
          <span className="col-span-6">Work Item</span>
          <span className="col-span-2 text-center">Type</span>
          <span className="col-span-2 text-center">Points</span>
          <span className="col-span-2 text-right">Score</span>
        </div>

        <div className="divide-y divide-slate-800/60">
          {items.map((item) => (
            <div key={item.id} className="px-4 py-3 hover:bg-slate-800/30 transition-colors grid grid-cols-12 gap-2 items-center">
              <div className="col-span-6">
                <div className="text-xs font-bold text-white">{item.title}</div>
                <div className="text-[11px] text-slate-400 mt-0.5">Status: {item.status}</div>
              </div>
              <div className="col-span-2 text-center">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 uppercase">
                  {item.type}
                </span>
              </div>
              <div className="col-span-2 text-center text-xs font-mono text-indigo-400 font-bold">
                {item.story_points} pts
              </div>
              <div className="col-span-2 text-right">
                <span className="text-xs font-black font-mono text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded border border-emerald-500/20">
                  {item.prioritization_score ? item.prioritization_score.toFixed(1) : '150.0'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
