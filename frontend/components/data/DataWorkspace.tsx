'use client';

import React, { useState } from 'react';
import {
  Database,
  Layers,
  Activity,
  GitBranch,
  BookOpen,
  FileText,
  Lock,
  Sparkles,
  ShieldCheck,
  Search,
} from 'lucide-react';
import DataCatalogViewer from './DataCatalogViewer';
import DataQualityDashboard from './DataQualityDashboard';
import DataLineageGraph from './DataLineageGraph';
import KnowledgeBaseManager from './KnowledgeBaseManager';
import DocumentManager from './DocumentManager';
import DataRetentionControl from './DataRetentionControl';

type DataTab = 'overview' | 'catalog' | 'quality' | 'lineage' | 'knowledge' | 'documents' | 'retention';

export default function DataWorkspace() {
  const [activeTab, setActiveTab] = useState<DataTab>('overview');

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-400">
            <Database className="w-8 h-8" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">
              Unified Data Platform & Governance Control Plane
            </h1>
            <p className="text-sm text-slate-400">
              Authority Hierarchy, Semantic Catalog, Multi-Dimensional Quality, Provenance Lineage & Knowledge Architecture
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <ShieldCheck className="w-3.5 h-3.5 mr-1 text-indigo-400" />
            Phase 36 Active
          </span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-800 pb-2 overflow-x-auto">
        {[
          { id: 'overview', label: 'Overview', icon: Layers },
          { id: 'catalog', label: 'Data Catalog', icon: Database },
          { id: 'quality', label: 'Quality & Conflicts', icon: Activity },
          { id: 'lineage', label: 'Lineage & Provenance', icon: GitBranch },
          { id: 'knowledge', label: 'Knowledge Base', icon: BookOpen },
          { id: 'documents', label: 'Documents & Hash Archive', icon: FileText },
          { id: 'retention', label: 'Retention & Legal Holds', icon: Lock },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as DataTab)}
              className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl font-medium text-xs sm:text-sm transition-all whitespace-nowrap ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-lg'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Key Metrics / Highlights */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-md">
              <span className="text-xs text-slate-400 font-medium block">Authoritative Catalog Items</span>
              <span className="text-2xl font-bold text-white mt-1 block">42</span>
              <span className="text-xs text-indigo-400 mt-2 block">100% SLA freshness compliant</span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-md">
              <span className="text-xs text-slate-400 font-medium block">Data Quality Index</span>
              <span className="text-2xl font-bold text-emerald-400 mt-1 block">96.8%</span>
              <span className="text-xs text-slate-400 mt-2 block">Across 7 quality dimensions</span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-md">
              <span className="text-xs text-slate-400 font-medium block">Curated Knowledge Items</span>
              <span className="text-2xl font-bold text-amber-400 mt-1 block">128</span>
              <span className="text-xs text-slate-400 mt-2 block">Canonical lifecycle verified</span>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-md">
              <span className="text-xs text-slate-400 font-medium block">Active Legal Holds</span>
              <span className="text-2xl font-bold text-rose-400 mt-1 block">1</span>
              <span className="text-xs text-slate-400 mt-2 block">Deletion locking enforced</span>
            </div>
          </div>

          {/* Data Hierarchy Architecture Summary */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-400" />
              Enterprise Data Hierarchy & Guardrails
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                <span className="font-bold text-indigo-400 text-sm block">1. Semantic Authority</span>
                <p className="text-slate-300 leading-relaxed">
                  Strict classification tiers ensure raw crawler and webhook data are never conflated with contractual commitments or verified records.
                </p>
              </div>

              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                <span className="font-bold text-cyan-400 text-sm block">2. Lineage & Provenance</span>
                <p className="text-slate-300 leading-relaxed">
                  Every data transformation, proposal generation, and AI inference links upstream sources, actors, and confidence scores.
                </p>
              </div>

              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                <span className="font-bold text-amber-400 text-sm block">3. Authorized AI Retrieval</span>
                <p className="text-slate-300 leading-relaxed">
                  Embeddings serve solely as retrieval indexes. AI context injection strictly filters by tenant boundaries and classification clearance.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'catalog' && <DataCatalogViewer />}
      {activeTab === 'quality' && <DataQualityDashboard />}
      {activeTab === 'lineage' && <DataLineageGraph />}
      {activeTab === 'knowledge' && <KnowledgeBaseManager />}
      {activeTab === 'documents' && <DocumentManager />}
      {activeTab === 'retention' && <DataRetentionControl />}
    </div>
  );
}
