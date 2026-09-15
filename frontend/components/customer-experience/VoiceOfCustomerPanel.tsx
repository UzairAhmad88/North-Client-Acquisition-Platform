'use client';

import React from 'react';
import { MessageSquareQuote, TrendingUp, Sparkles, Tag } from 'lucide-react';
import { VoiceThemeItem } from '../../lib/api/customerExperience';

interface VoiceOfCustomerPanelProps {
  themes: VoiceThemeItem[];
  records: any[];
}

export const VoiceOfCustomerPanel: React.FC<VoiceOfCustomerPanelProps> = ({ themes, records }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <MessageSquareQuote className="h-4 w-4 text-pink-400" />
          Voice of Customer & Feedback Themes
        </h3>
        <span className="text-xs text-slate-400 font-mono">Themes: {themes.length}</span>
      </div>

      <div className="space-y-3">
        {themes.map((thm) => (
          <div key={thm.id} className="p-3 rounded-lg border border-slate-800/80 bg-slate-800/30 space-y-2">
            <div className="flex items-center justify-between">
              <div className="text-xs font-bold text-slate-100">{thm.theme_name}</div>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-pink-500/10 text-pink-400 border border-pink-500/20 uppercase font-semibold">
                Freq: {thm.frequency}
              </span>
            </div>
            <p className="text-xs text-slate-400">{thm.description}</p>
            {thm.sample_quotes && thm.sample_quotes.length > 0 && (
              <div className="p-2 rounded bg-slate-900/60 border border-slate-800 text-[11px] italic text-slate-300">
                "{thm.sample_quotes[0]}"
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
