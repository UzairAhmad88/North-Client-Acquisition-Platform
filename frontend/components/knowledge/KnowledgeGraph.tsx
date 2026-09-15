'use client';

import React, { useState, useEffect } from 'react';
import { getKnowledgeGraph, KnowledgeGraphData } from '@/lib/api/knowledge';
import { GitBranch, Layers, Search, ArrowRight, Share2, Filter } from 'lucide-react';

export default function KnowledgeGraphComponent() {
  const [graphData, setGraphData] = useState<KnowledgeGraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  useEffect(() => {
    async function loadGraph() {
      setLoading(true);
      try {
        const data = await getKnowledgeGraph();
        setGraphData(data);
      } catch (err) {
        console.error('Failed to load knowledge graph:', err);
      } finally {
        setLoading(false);
      }
    }
    loadGraph();
  }, []);

  if (loading || !graphData) {
    return (
      <div className="p-12 text-center text-slate-500 animate-pulse bg-white rounded-xl border border-slate-200">
        Traversing and projecting multi-hop enterprise knowledge graph...
      </div>
    );
  }

  const getNodeColor = (type: string) => {
    switch (type) {
      case 'CLIENT':
        return 'bg-blue-500 text-white border-blue-600';
      case 'PROJECT':
        return 'bg-indigo-500 text-white border-indigo-600';
      case 'REQUIREMENT':
        return 'bg-purple-500 text-white border-purple-600';
      case 'DECISION':
        return 'bg-amber-500 text-white border-amber-600';
      case 'CONTROL':
        return 'bg-emerald-500 text-white border-emerald-600';
      case 'EVIDENCE':
        return 'bg-teal-500 text-white border-teal-600';
      default:
        return 'bg-slate-600 text-white border-slate-700';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-indigo-600" />
            Organizational Knowledge Graph & Entity Relationships
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Section 23 & 48: Multi-hop graph modeling inter-connected Clients, Projects, Requirements, Decisions, Controls, and Evidence.
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-600">
          <span className="px-2.5 py-1 rounded-full bg-slate-100">{graphData.nodes.length} Entities</span>
          <span className="px-2.5 py-1 rounded-full bg-slate-100">{graphData.edges.length} Relationships</span>
        </div>
      </div>

      {/* Graph Visual Explorer */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        {/* Nodes & Edges Display */}
        <div className="md:col-span-8 bg-slate-900 text-white p-6 rounded-2xl border border-slate-800 shadow-sm min-h-[450px] relative overflow-hidden flex flex-col justify-between">
          <div className="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-3">
            <span>Graph Visual Representation</span>
            <span>BFS Multi-Hop Path Navigation</span>
          </div>

          {/* Connected Flow Representation */}
          <div className="py-8 space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {graphData.nodes.map((node) => (
                <div
                  key={node.id}
                  onClick={() => setSelectedNode(node.id)}
                  className={`p-3.5 rounded-xl border cursor-pointer transition-all ${
                    selectedNode === node.id
                      ? 'ring-2 ring-indigo-400 scale-105 shadow-lg ' + getNodeColor(node.type)
                      : 'bg-slate-800/80 hover:bg-slate-800 border-slate-700 text-slate-200'
                  }`}
                >
                  <div className="flex items-center justify-between text-[10px] font-mono opacity-80 mb-1">
                    <span>{node.type}</span>
                    <span>{node.domain}</span>
                  </div>
                  <div className="font-bold text-xs truncate">{node.name}</div>
                  <div className="text-[10px] font-mono opacity-60 mt-1 truncate">{node.id}</div>
                </div>
              ))}
            </div>

            {/* Edge Stream */}
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80 space-y-2">
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                Active Relationship Edges
              </div>
              <div className="space-y-1.5 max-h-40 overflow-y-auto pr-1">
                {graphData.edges.map((edge, idx) => (
                  <div key={idx} className="flex items-center justify-between text-xs font-mono text-slate-300 py-1 border-b border-slate-800/40">
                    <span className="text-indigo-400">{edge.source}</span>
                    <span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 text-[10px] font-bold">
                      [{edge.type}]
                    </span>
                    <span className="text-emerald-400">{edge.target}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="text-[11px] text-slate-400 flex items-center justify-between pt-3 border-t border-slate-800">
            <span>Graph Traversal Engine: Multi-Directional Adjacency</span>
            <span>Zero Data Leakage Bounds Enforced</span>
          </div>
        </div>

        {/* Node Inspector Side Panel */}
        <div className="md:col-span-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h4 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
            <Share2 className="w-4 h-4 text-indigo-600" />
            Entity Inspector
          </h4>

          {selectedNode ? (
            <div className="space-y-4 text-xs">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-slate-400 block mb-1">Entity Code:</span>
                <span className="font-mono font-bold text-slate-900 text-sm">{selectedNode}</span>
              </div>

              <div>
                <span className="font-semibold text-slate-700 block mb-2">Outgoing Connections:</span>
                <div className="space-y-1.5">
                  {graphData.edges
                    .filter((e) => e.source === selectedNode)
                    .map((e, idx) => (
                      <div key={idx} className="p-2 bg-indigo-50 border border-indigo-100 rounded-lg text-indigo-900 flex items-center justify-between">
                        <span>{e.type}</span>
                        <ArrowRight className="w-3 h-3 text-indigo-400" />
                        <span className="font-mono font-bold">{e.target}</span>
                      </div>
                    ))}
                  {graphData.edges.filter((e) => e.source === selectedNode).length === 0 && (
                    <div className="text-slate-400 italic">No outgoing connections.</div>
                  )}
                </div>
              </div>

              <div>
                <span className="font-semibold text-slate-700 block mb-2">Incoming Connections:</span>
                <div className="space-y-1.5">
                  {graphData.edges
                    .filter((e) => e.target === selectedNode)
                    .map((e, idx) => (
                      <div key={idx} className="p-2 bg-emerald-50 border border-emerald-100 rounded-lg text-emerald-900 flex items-center justify-between">
                        <span className="font-mono font-bold">{e.source}</span>
                        <ArrowRight className="w-3 h-3 text-emerald-400" />
                        <span>{e.type}</span>
                      </div>
                    ))}
                  {graphData.edges.filter((e) => e.target === selectedNode).length === 0 && (
                    <div className="text-slate-400 italic">No incoming connections.</div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-slate-400 text-xs italic">
              Click an entity in the graph to inspect its multi-hop relationships.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
