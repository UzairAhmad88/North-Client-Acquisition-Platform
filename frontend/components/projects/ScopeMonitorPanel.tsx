'use client';

import React from 'react';

interface ScopeSignal {
  signal_type: string;
  description: string;
  source: string;
  severity: string;
  recommended_action: string;
}


interface ScopeMonitorPanelProps {
  signals: ScopeSignal[];
}

export const ScopeMonitorPanel: React.FC<ScopeMonitorPanelProps> = ({ signals }) => {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 shadow-sm mb-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">Baseline Scope Monitor</h3>
          <p className="text-xs text-slate-500">Detects potential scope expansion signals against committed baseline</p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 rounded bg-indigo-50 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300">
          {signals.length} Signals Detected
        </span>
      </div>

      {signals.length === 0 ? (
        <div className="text-center py-6 text-xs text-slate-400 border border-dashed border-slate-200 dark:border-slate-700 rounded-lg">
          No scope expansion signals detected. Execution matches baseline commitments.
        </div>
      ) : (
        <div className="space-y-3">
          {signals.map((sig, i) => (
            <div key={i} className="p-3 bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40 rounded-lg text-xs">
              <div className="flex items-center justify-between mb-1">
                <span className="font-semibold text-amber-800 dark:text-amber-300">{sig.signal_type}</span>
                <span className="text-[10px] font-mono text-slate-400">Source: {sig.source}</span>
              </div>
              <p className="text-slate-700 dark:text-slate-300 mb-2">{sig.description}</p>
              <div className="text-[11px] text-slate-500 bg-white dark:bg-slate-900 p-2 rounded border border-slate-200 dark:border-slate-800">
                <strong>Recommended Action:</strong> {sig.recommended_action}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
