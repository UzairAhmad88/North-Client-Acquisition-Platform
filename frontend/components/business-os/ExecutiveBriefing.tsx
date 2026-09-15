'use client';

import React, { useState } from 'react';
import { ExecutiveBriefing, businessOSApi } from '@/lib/api/business_os';

interface ExecutiveBriefingProps {
  initialBriefing: ExecutiveBriefing;
}

export const ExecutiveBriefingComponent: React.FC<ExecutiveBriefingProps> = ({ initialBriefing }) => {
  const [briefing, setBriefing] = useState<ExecutiveBriefing>(initialBriefing);
  const [frequency, setFrequency] = useState<string>('DAILY');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const fetchBriefing = async (freq: string) => {
    try {
      setIsLoading(true);
      setFrequency(freq);
      const res = await businessOSApi.getBriefing(freq);
      setBriefing(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span>📰</span> Executive Briefing Synthesizer
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Automated intelligence digest synthesizing operational domains into actionable highlights.
          </p>
        </div>
        <div className="flex bg-slate-950 border border-slate-800 rounded-lg p-1 text-xs">
          {['DAILY', 'WEEKLY', 'MONTHLY'].map((freq) => (
            <button
              key={freq}
              onClick={() => fetchBriefing(freq)}
              className={`px-3 py-1 rounded font-semibold transition-all ${
                frequency === freq
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {freq}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        {/* Title & Summary */}
        <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-4">
          <h3 className="text-base font-bold text-slate-100">{briefing.title}</h3>
          <p className="text-xs text-slate-300 mt-2 leading-relaxed">{briefing.summary_paragraph}</p>
        </div>

        {/* What Changed & Recommended Attention */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-4">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">What Changed</h4>
            <ul className="space-y-1.5 text-xs text-slate-400">
              {briefing.what_changed_summary.map((item, i) => (
                <li key={i} className="flex items-start gap-1.5">
                  <span className="text-indigo-400 font-bold">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-4">
            <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">Recommended Attention Areas</h4>
            <ul className="space-y-1.5 text-xs text-slate-400">
              {briefing.recommended_attention_areas.map((item, i) => (
                <li key={i} className="flex items-start gap-1.5">
                  <span className="text-amber-400 font-bold">→</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
