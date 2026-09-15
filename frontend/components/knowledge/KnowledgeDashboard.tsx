'use client';

import React, { useState, useEffect } from 'react';
import { getKnowledgeOverview, KnowledgeOverview } from '@/lib/api/knowledge';
import KnowledgeOverviewComponent from './KnowledgeOverview';
import KnowledgeSearchComponent from './KnowledgeSearch';
import KnowledgeExplorerComponent from './KnowledgeExplorer';
import KnowledgeGraphComponent from './KnowledgeGraph';
import DecisionMemoryComponent from './DecisionMemory';
import LessonLibraryComponent from './LessonLibrary';
import ContextInspectorComponent from './ContextInspector';
import ConflictPanelComponent from './ConflictPanel';
import KnowledgeQualityComponent from './KnowledgeQuality';
import {
  Brain,
  Search,
  BookOpen,
  GitBranch,
  Layers,
  Sparkles,
  Cpu,
  AlertOctagon,
  CheckCircle2,
  RefreshCw,
} from 'lucide-react';

export default function KnowledgeDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [overview, setOverview] = useState<KnowledgeOverview | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchOverview = async () => {
    setLoading(true);
    try {
      const data = await getKnowledgeOverview();
      setOverview(data);
    } catch (err) {
      console.error('Failed to load knowledge overview:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Brain },
    { id: 'search', label: 'Enterprise Search', icon: Search },
    { id: 'explorer', label: 'Repository', icon: BookOpen },
    { id: 'graph', label: 'Knowledge Graph', icon: GitBranch },
    { id: 'decisions', label: 'Decisions', icon: Layers },
    { id: 'lessons', label: 'Lessons Learned', icon: Sparkles },
    { id: 'context', label: 'AI Context Engine', icon: Cpu },
    { id: 'conflicts', label: 'Conflicts', icon: AlertOctagon },
    { id: 'quality', label: 'Quality & Integrity', icon: CheckCircle2 },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4 md:p-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2.5">
            <Brain className="w-7 h-7 text-indigo-600" />
            Knowledge & Organizational Memory Platform
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Phase 48 Unified Knowledge, Enterprise Search, Semantic Intelligence & Grounded AI Context
          </p>
        </div>

        <button
          onClick={fetchOverview}
          disabled={loading}
          className="px-3.5 py-2 bg-white border border-slate-200 hover:border-slate-300 text-slate-700 text-xs font-semibold rounded-xl flex items-center gap-2 transition-all shadow-sm self-start sm:self-auto"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Memory
        </button>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 border-b border-slate-100">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200/60'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-500'}`} />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab Panels */}
      <div>
        {activeTab === 'overview' && (
          <KnowledgeOverviewComponent
            overview={overview}
            loading={loading}
            onRefresh={fetchOverview}
            onNavigateTab={setActiveTab}
          />
        )}
        {activeTab === 'search' && <KnowledgeSearchComponent />}
        {activeTab === 'explorer' && <KnowledgeExplorerComponent />}
        {activeTab === 'graph' && <KnowledgeGraphComponent />}
        {activeTab === 'decisions' && <DecisionMemoryComponent />}
        {activeTab === 'lessons' && <LessonLibraryComponent />}
        {activeTab === 'context' && <ContextInspectorComponent />}
        {activeTab === 'conflicts' && <ConflictPanelComponent />}
        {activeTab === 'quality' && <KnowledgeQualityComponent />}
      </div>
    </div>
  );
}
