'use client';

import React, { useState, useEffect } from 'react';
import {
  GitBranch,
  ArrowRight,
  ArrowLeft,
  Search,
  Layers,
  Database,
  Cpu,
  UserCheck,
  FileCheck2,
  Share2,
} from 'lucide-react';
import { dataApi, LineageGraphResponse } from '@/lib/api/data';

export default function DataLineageGraph() {
  const [entityType, setEntityType] = useState('PROPOSAL');
  const [entityId, setEntityId] = useState('PROP-7721');
  const [graph, setGraph] = useState<LineageGraphResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchLineage = async () => {
    try {
      setLoading(true);
      const res = await dataApi.getLineageGraph(entityType, entityId);
      if (res) {
        setGraph(res);
      }
    } catch (err) {
      console.error('Failed to trace lineage', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLineage();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-cyan-400" />
            End-to-End Data Lineage & Provenance Graph
          </h2>
          <p className="text-sm text-slate-400">
            Trace upstream origins, derivation pipelines, AI transformations, and downstream dependents.
          </p>
        </div>
      </div>

      {/* Query Bar */}
      <div className="flex flex-col sm:flex-row gap-3 bg-slate-900 border border-slate-800 p-4 rounded-xl">
        <div className="w-full sm:w-48">
          <label className="block text-xs font-medium text-slate-400 mb-1">Entity Type</label>
          <select
            value={entityType}
            onChange={(e) => setEntityType(e.target.value)}
            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-cyan-500"
          >
            <option value="PROPOSAL">PROPOSAL</option>
            <option value="ESTIMATE">ESTIMATE</option>
            <option value="REQUIREMENT">REQUIREMENT</option>
            <option value="AUDIT">AUDIT</option>
            <option value="LEAD">LEAD</option>
            <option value="CONTRACT">CONTRACT</option>
          </select>
        </div>

        <div className="flex-1">
          <label className="block text-xs font-medium text-slate-400 mb-1">Entity Identifier</label>
          <input
            type="text"
            value={entityId}
            onChange={(e) => setEntityId(e.target.value)}
            placeholder="e.g. PROP-7721"
            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex items-end">
          <button
            onClick={fetchLineage}
            disabled={loading}
            className="w-full sm:w-auto px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-semibold rounded-lg shadow-md transition-all flex items-center justify-center gap-2"
          >
            <Search className="w-4 h-4" />
            Trace Lineage
          </button>
        </div>
      </div>

      {/* Lineage Visual Flow */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Share2 className="w-4 h-4 text-cyan-400" />
          Trace Graph: {entityType} ({entityId})
        </h3>

        {loading ? (
          <div className="p-12 text-center text-slate-400">Tracing upstream and downstream edges...</div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Upstream Sources Column */}
            <div className="space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                  <ArrowLeft className="w-3.5 h-3.5 text-cyan-400" />
                  Upstream Origins ({graph?.upstream_nodes?.length || 0})
                </span>
                <span className="text-[10px] text-slate-500">Sources / Inputs</span>
              </div>

              {graph?.upstream_nodes && graph.upstream_nodes.length > 0 ? (
                graph.upstream_nodes.map((node, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1.5 hover:border-cyan-500/40 transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-cyan-300">{node.type}</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                        {node.relationship}
                      </span>
                    </div>
                    <p className="text-xs text-white font-mono">{node.id}</p>
                    {node.transformation && (
                      <p className="text-[11px] text-slate-400">
                        Transformation: <span className="text-slate-300 font-medium">{node.transformation}</span>
                      </p>
                    )}
                  </div>
                ))
              ) : (
                <div className="p-4 bg-slate-950/40 border border-slate-800 rounded-xl text-center text-slate-500 text-xs">
                  No upstream sources linked directly.
                </div>
              )}
            </div>

            {/* Target Central Node */}
            <div className="flex flex-col items-center justify-center p-6 bg-cyan-500/5 border-2 border-cyan-500/30 rounded-2xl text-center space-y-3 shadow-inner">
              <div className="p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-full text-cyan-400">
                <Database className="w-8 h-8" />
              </div>
              <div>
                <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                  Inspected Node
                </span>
                <h4 className="text-lg font-extrabold text-white mt-0.5">{entityId}</h4>
                <p className="text-xs text-slate-400 font-mono mt-0.5">{entityType}</p>
              </div>
              <div className="pt-2 border-t border-cyan-500/20 w-full text-xs text-slate-400 space-y-1">
                <p>Authority: <span className="text-cyan-300 font-medium">VERIFIED_DATA</span></p>
                <p>Status: <span className="text-emerald-400 font-medium">HEALTHY</span></p>
              </div>
            </div>

            {/* Downstream Dependents Column */}
            <div className="space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                  Downstream Dependents ({graph?.downstream_nodes?.length || 0})
                  <ArrowRight className="w-3.5 h-3.5 text-emerald-400" />
                </span>
                <span className="text-[10px] text-slate-500">Derivations</span>
              </div>

              {graph?.downstream_nodes && graph.downstream_nodes.length > 0 ? (
                graph.downstream_nodes.map((node, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1.5 hover:border-emerald-500/40 transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-emerald-300">{node.type}</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {node.relationship}
                      </span>
                    </div>
                    <p className="text-xs text-white font-mono">{node.id}</p>
                  </div>
                ))
              ) : (
                <div className="p-4 bg-slate-950/40 border border-slate-800 rounded-xl text-center text-slate-500 text-xs">
                  No downstream dependents registered yet.
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
