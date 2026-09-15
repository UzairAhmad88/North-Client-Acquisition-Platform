'use client';

import React from 'react';
import { ProcessMap } from '@/lib/api/processIntelligence';
import { GitBranch, ArrowRight, Clock, Activity } from 'lucide-react';

interface Props {
  processMap: ProcessMap | null;
  loading: boolean;
}

export default function ProcessMapComponent({ processMap, loading }: Props) {
  if (loading) {
    return <div className="p-12 text-center text-slate-400">Reconstructing directly-follows graph...</div>;
  }

  if (!processMap || processMap.nodes.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-12 text-center text-slate-400">
        <GitBranch className="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p className="text-lg font-medium text-white">No Process Graph Available</p>
        <p className="text-sm text-slate-500 mt-1">Ingest event logs to automatically discover process topology.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-indigo-400" /> Process Flow Map ({processMap.map_type})
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            {processMap.nodes.length} Activities &bull; {processMap.edges.length} Transitions
          </p>
        </div>
      </div>

      {/* Nodes Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {processMap.nodes.map((node) => (
          <div key={node.id} className="bg-slate-950 border border-slate-800 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-white truncate">{node.label}</span>
              <Activity className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="mt-2 flex justify-between text-xs text-slate-400">
              <span>Freq: {node.frequency}</span>
              <span>Avg: {node.average_duration_ms}ms</span>
            </div>
          </div>
        ))}
      </div>

      {/* Transition Edges Table */}
      <div className="mt-6">
        <h4 className="text-sm font-semibold text-slate-300 mb-3">Directly-Follows Transitions</h4>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-400">
            <thead className="bg-slate-950 text-slate-300 text-xs font-semibold uppercase">
              <tr>
                <th className="px-4 py-3">Source Activity</th>
                <th className="px-4 py-3"></th>
                <th className="px-4 py-3">Target Activity</th>
                <th className="px-4 py-3">Frequency</th>
                <th className="px-4 py-3">Avg Latency</th>
                <th className="px-4 py-3">Median Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {processMap.edges.map((edge, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="px-4 py-3 font-medium text-white">{edge.source_activity}</td>
                  <td className="px-4 py-3"><ArrowRight className="w-4 h-4 text-slate-500" /></td>
                  <td className="px-4 py-3 font-medium text-white">{edge.target_activity}</td>
                  <td className="px-4 py-3 font-mono">{edge.transition_frequency}</td>
                  <td className="px-4 py-3 text-amber-400 font-mono">{edge.average_latency_seconds}s</td>
                  <td className="px-4 py-3 font-mono">{edge.median_latency_seconds}s</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
