'use client';

import React, { useState } from 'react';
import GovernanceDashboard from '@/components/governance/GovernanceDashboard';
import AIGovernanceWorkspace from '@/components/governance/AIGovernanceWorkspace';
import { Scale, Bot } from 'lucide-react';

export default function GovernancePage() {
  const [activeWorkspace, setActiveWorkspace] = useState<'grc' | 'ai'>('grc');

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Workspace Switcher */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">Governance Command Center</h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Phase 47 Unified GRC, Compliance, Risk & Privacy Platform paired with Phase 33 AI Governance
          </p>
        </div>

        <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl border border-slate-200">
          <button
            onClick={() => setActiveWorkspace('grc')}
            className={`px-3 py-1.5 text-xs font-bold rounded-lg flex items-center gap-1.5 transition-all ${
              activeWorkspace === 'grc'
                ? 'bg-indigo-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
            }`}
          >
            <Scale className="w-4 h-4" />
            <span>Unified GRC & Compliance</span>
          </button>
          <button
            onClick={() => setActiveWorkspace('ai')}
            className={`px-3 py-1.5 text-xs font-bold rounded-lg flex items-center gap-1.5 transition-all ${
              activeWorkspace === 'ai'
                ? 'bg-indigo-600 text-white shadow-xs'
                : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
            }`}
          >
            <Bot className="w-4 h-4" />
            <span>AI Governance & Prompts</span>
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      {activeWorkspace === 'grc' ? (
        <GovernanceDashboard />
      ) : (
        <AIGovernanceWorkspace />
      )}
    </div>
  );
}
