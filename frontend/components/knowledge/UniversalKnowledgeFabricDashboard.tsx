'use client';

import React, { useState } from 'react';

export default function UniversalKnowledgeFabricDashboard() {
  const [searchQuery, setSearchQuery] = useState('Show delayed projects involving our largest customers this quarter');
  const [selectedDomain, setSelectedDomain] = useState('ALL');
  const [activeTab, setActiveTab] = useState<'search' | 'entity360' | 'graph' | 'conflicts'>('search');

  const stats = [
    { label: 'Canonical Entities', value: '4,850', change: '+124 this week', status: 'optimal' },
    { label: 'Graph Relationships', value: '24,900', change: 'Avg degree 5.1', status: 'optimal' },
    { label: 'Verified Claims', value: '12,400', change: '99.4% precision', status: 'optimal' },
    { label: 'Ingested Documents', value: '1,820', change: 'PDF, DOCX, XLSX', status: 'optimal' },
    { label: 'Knowledge Quality', value: '96.4%', change: 'Freshness 93.2%', status: 'optimal' },
    { label: 'Active Conflicts', value: '3', change: '2 in reconciliation', status: 'warning' },
    { label: 'Open Gaps', value: '5', change: 'Remediating', status: 'warning' },
    { label: 'Searches Today', value: '342', change: 'Avg latency 8.4ms', status: 'optimal' },
  ];

  const searchResults = [
    {
      id: 'ENT-CUST-101',
      title: 'Acme Global Corporation (Canonical Entity)',
      type: 'CUSTOMER',
      domain: 'SALES_CRM',
      clearance: 'INTERNAL',
      snippet: 'Primary Tier-1 enterprise account with 3 active MSA contracts and 12 ongoing project workstreams.',
      confidence: '99.0%',
      explanation: 'Exact normalized entity token match; verified through Salesforce and NetSuite Tax ID.'
    },
    {
      id: 'DOC-MSA-2026',
      title: 'Master Services Agreement 2026 (Acme Corp)',
      type: 'CONTRACT',
      domain: 'LEGAL_CONTRACTS',
      clearance: 'CONFIDENTIAL',
      snippet: 'Governing enterprise contract specifying $2.4M ARR commitment with mutual indemnification.',
      confidence: '97.2%',
      explanation: 'Graph traversal edge: Acme Corporation owns Contract.'
    },
    {
      id: 'PRJ-APOLLO',
      title: 'Project Apollo Migration (Delayed Milestone)',
      type: 'PROJECT',
      domain: 'OPERATIONS',
      clearance: 'INTERNAL',
      snippet: 'Core infrastructure migration currently flagged amber due to supplier hardware lead times.',
      confidence: '95.4%',
      explanation: 'Filtered by condition: Milestone delay flagged in Jira Enterprise telemetry.'
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Enterprise Knowledge Fabric & Universal Search
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800">
              FABRIC LIVE
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Universal, permission-aware representation of enterprise knowledge, temporal graphs, and semantic intelligence.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700">
            Rebuild Vector Index
          </button>
          <button className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-indigo-600 hover:bg-indigo-500 text-white shadow-sm">
            Trigger Ingestion Job
          </button>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s, idx) => (
          <div key={idx} className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="text-xs font-medium text-slate-400">{s.label}</div>
            <div className="text-2xl font-bold text-white mt-1">{s.value}</div>
            <div className={`text-xs mt-1 ${s.status === 'optimal' ? 'text-emerald-400' : 'text-amber-400'}`}>
              {s.change}
            </div>
          </div>
        ))}
      </div>

      {/* Universal Search Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Ask anything across CRM, ERP, Finance, HR, Contracts, Projects, and AI Memory..."
              className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
            />
          </div>
          <button className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg text-sm transition">
            Universal Search
          </button>
        </div>

        {/* Domain Filter Chips */}
        <div className="flex flex-wrap items-center gap-2 pt-1 text-xs text-slate-400">
          <span>Domains:</span>
          {['ALL', 'FINANCE', 'LEGAL_CONTRACTS', 'OPERATIONS', 'SALES_CRM', 'AI_MEMORY'].map((d) => (
            <button
              key={d}
              onClick={() => setSelectedDomain(d)}
              className={`px-2.5 py-1 rounded-md transition ${
                selectedDomain === d
                  ? 'bg-indigo-900/60 text-indigo-300 border border-indigo-700 font-semibold'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              {d}
            </button>
          ))}
          <span className="ml-auto text-emerald-400 font-mono text-[11px]">
            Security Trimming: RBAC Active (Least Privilege Enforced)
          </span>
        </div>
      </div>

      {/* Main Tabs */}
      <div className="flex gap-2 border-b border-slate-800 text-sm">
        {[
          { key: 'search', label: 'Search Results & Explanations' },
          { key: 'entity360', label: 'Entity 360 Explorer' },
          { key: 'graph', label: 'Graph Topology & Lineage' },
          { key: 'conflicts', label: 'Conflicts & Quality Remediations' }
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as any)}
            className={`pb-2.5 px-3 font-medium transition border-b-2 ${
              activeTab === tab.key
                ? 'border-indigo-500 text-white'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'search' && (
        <div className="space-y-3">
          <div className="text-xs text-slate-400 flex justify-between">
            <span>Showing 3 ranked results (8.4ms latency)</span>
            <span>0 restricted items suppressed by security trimming</span>
          </div>

          {searchResults.map((item) => (
            <div key={item.id} className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-slate-700 transition space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <span className="font-semibold text-white hover:text-indigo-400 cursor-pointer">
                    {item.title}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300 border border-slate-700">
                    {item.type}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-950 text-indigo-400 border border-indigo-800">
                    {item.domain}
                  </span>
                </div>
                <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                  item.clearance === 'CONFIDENTIAL'
                    ? 'bg-amber-950 text-amber-300 border border-amber-800'
                    : 'bg-slate-800 text-slate-400'
                }`}>
                  {item.clearance}
                </span>
              </div>
              <p className="text-sm text-slate-300">{item.snippet}</p>
              <div className="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-800/80">
                <span className="text-slate-400"><strong>Explainability:</strong> {item.explanation}</span>
                <span className="text-emerald-400 font-mono">Confidence: {item.confidence}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'entity360' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-xl font-bold text-white">Acme Global Corporation (ENT-CUST-101)</h2>
              <p className="text-xs text-slate-400 mt-0.5">Canonical Master Entity • Resolved from 4 disparate system records</p>
            </div>
            <span className="px-2.5 py-1 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-xs font-semibold">
              ACTIVE MASTER
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 font-semibold mb-2">Canonical Attributes</div>
              <ul className="text-xs space-y-1.5 text-slate-300">
                <li><strong className="text-slate-400">Industry:</strong> Enterprise SaaS</li>
                <li><strong className="text-slate-400">ARR:</strong> $45,000,000</li>
                <li><strong className="text-slate-400">Credit Rating:</strong> AAA</li>
                <li><strong className="text-slate-400">Risk Tier:</strong> Low</li>
              </ul>
            </div>

            <div className="bg-slate-950 border border-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 font-semibold mb-2">Resolved Aliases</div>
              <div className="flex flex-wrap gap-1.5">
                {['Acme Ltd', 'ACME Limited', 'Acme Inc.', 'Acme Holdings'].map((a) => (
                  <span key={a} className="px-2 py-0.5 bg-slate-900 text-slate-300 rounded text-[11px] border border-slate-800">
                    {a}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-slate-950 border border-slate-800 rounded-lg p-3">
              <div className="text-xs text-slate-400 font-semibold mb-2">AI Insights & Provenance</div>
              <p className="text-xs text-indigo-300 leading-relaxed">
                Contract renewal window opens in 90 days. High expansion potential based on 30% API throughput increase.
              </p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'graph' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center space-y-3">
          <div className="text-base font-semibold text-white">Enterprise Knowledge Graph Topology</div>
          <p className="text-xs text-slate-400 max-w-lg mx-auto">
            Interactive multi-hop network traversal demonstrating shortest path [Acme Corp → Apollo Migration → ChipSet Tech].
          </p>
          <div className="h-64 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-center text-slate-500 font-mono text-xs">
            [GRAPH VISUALIZATION CANVAS: 4 Nodes, 3 Edges, Centrality 0.87]
          </div>
        </div>
      )}

      {activeTab === 'conflicts' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-bold text-white">Knowledge Conflicts & Gap Remediations</h2>
          <div className="bg-slate-950 border border-amber-900/40 rounded-lg p-4 text-xs space-y-2">
            <div className="flex justify-between font-semibold text-amber-300">
              <span>CONFLICT-2026-01: Payment Terms Discrepancy on Acme SOW #4</span>
              <span>RESOLVING</span>
            </div>
            <p className="text-slate-400">
              Source A (NetSuite ERP): NET-30 vs Source B (Email Note): NET-60. Recommended resolution: NET-30 based on Authority Tier 1.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
