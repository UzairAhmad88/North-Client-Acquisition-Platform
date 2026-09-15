'use client';

import React, { useState } from 'react';
import { AssistantPanel } from '../assistant/AssistantPanel';
import { GlobalSearch } from '../search/GlobalSearch';
import { CommandPalette } from './CommandPalette';

export const CommandCenterWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'SEARCH' | 'ASSISTANT' | 'COMMANDS'>('SEARCH');

  return (
    <div className="flex flex-col space-y-6 max-w-7xl mx-auto w-full p-4">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center bg-slate-900/90 border border-slate-800 p-6 rounded-2xl backdrop-blur-md">
        <div>
          <div className="flex items-center space-x-3">
            <span className="text-2xl">⚡</span>
            <h1 className="text-2xl font-black tracking-tight text-slate-100">
              Global Command Center & Unified Search
            </h1>
          </div>
          <p className="text-sm text-slate-400 mt-1 max-w-2xl">
            Phase 38 Unified Platform Interface: Global cross-entity search, natural-language assistant,
            and keyboard-driven Command Palette (<kbd className="bg-slate-800 px-1.5 py-0.5 rounded text-xs font-mono">Ctrl + K</kbd>).
          </p>
        </div>

        {/* Tab Controls */}
        <div className="flex items-center space-x-1 bg-slate-950/80 p-1.5 rounded-xl border border-slate-800 mt-4 md:mt-0">
          <button
            onClick={() => setActiveTab('SEARCH')}
            className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${
              activeTab === 'SEARCH'
                ? 'bg-cyan-600 text-white shadow-lg'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            🔍 Global Search
          </button>
          <button
            onClick={() => setActiveTab('ASSISTANT')}
            className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${
              activeTab === 'ASSISTANT'
                ? 'bg-indigo-600 text-white shadow-lg'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            🤖 AI Assistant
          </button>
        </div>
      </div>

      {/* Main Tab Content */}
      <div>
        {activeTab === 'SEARCH' && <GlobalSearch />}
        {activeTab === 'ASSISTANT' && <AssistantPanel />}
      </div>

      {/* Global Command Palette ( हमेशा active for Ctrl+K ) */}
      <CommandPalette />
    </div>
  );
};
