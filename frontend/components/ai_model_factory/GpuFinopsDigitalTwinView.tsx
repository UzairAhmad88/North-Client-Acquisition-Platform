'use client';

import React, { useState } from 'react';

export const GpuFinopsDigitalTwinView: React.FC = () => {
  const [simulationResult, setSimulationResult] = useState<any | null>(null);

  const runSimulation = (type: string) => {
    if (type === 'GPU_NODE_FAILURE') {
      setSimulationResult({
        scenario: 'GPU Node Failure Simulation',
        impact: '1 GPU cluster node offline. Automated failover shifted 4 inference workloads to backup availability zone with 0 downtime.',
        costImpact: '+$120.00 compute reallocation',
        projectedLatency: '34 ms (within 50ms SLA)',
      });
    } else {
      setSimulationResult({
        scenario: 'Inference Traffic 3x Surge',
        impact: 'Autoscaling triggers +4 replica pods. Peak P95 latency scales from 24ms to 36ms.',
        costImpact: '+$340.00 / day',
        projectedLatency: '36 ms (within 50ms SLA)',
      });
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* GPU Clusters & AI FinOps */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-100">GPU Cluster & AI FinOps Breakdown</h3>
          <span className="text-xs px-2.5 py-1 rounded-full bg-cyan-500/20 text-cyan-300 font-mono">
            4 H100 Nodes Active
          </span>
        </div>
        <div className="space-y-3 text-xs">
          <div className="p-3.5 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Inference Tokens (Monthly):</span>
              <span className="font-bold text-white">$14,280.00 (62%)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Training & Fine-Tuning GPU:</span>
              <span className="font-bold text-white">$6,450.00 (28%)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Embedding & Vector Search:</span>
              <span className="font-bold text-white">$2,300.00 (10%)</span>
            </div>
          </div>
          <div className="bg-slate-900/60 p-3 rounded border border-slate-800 space-y-1">
            <span className="text-slate-500 text-[10px] uppercase font-mono">GPU Allocation Queue:</span>
            <p className="text-slate-300 font-mono">Node alpha-01: NVIDIA H100 SXM5 80GB (78.4% utilization)</p>
          </div>
        </div>
      </div>

      {/* Digital Twin Failure Simulation */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-100">AI Infrastructure Digital Twin</h3>
          <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 font-mono">
            Phase 50 Simulation
          </span>
        </div>
        <p className="text-xs text-slate-400">
          Run isolated scenario simulations to stress-test GPU outages, provider rate-limiting, and cost surges.
        </p>
        <div className="flex gap-3">
          <button
            onClick={() => runSimulation('GPU_NODE_FAILURE')}
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 transition"
          >
            Simulate GPU Failure
          </button>
          <button
            onClick={() => runSimulation('TRAFFIC_SURGE')}
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 border border-slate-700 transition"
          >
            Simulate 3x Traffic Surge
          </button>
        </div>

        {simulationResult && (
          <div className="p-3.5 rounded-lg bg-indigo-950/40 border border-indigo-500/30 text-xs space-y-2">
            <p className="font-bold text-indigo-300 font-mono text-sm">{simulationResult.scenario}</p>
            <p className="text-slate-300">{simulationResult.impact}</p>
            <div className="grid grid-cols-2 gap-2 pt-2 border-t border-indigo-500/20 text-[11px]">
              <div>
                <span className="text-slate-500">Cost Impact:</span>
                <p className="font-mono text-amber-300">{simulationResult.costImpact}</p>
              </div>
              <div>
                <span className="text-slate-500">Latency Projected:</span>
                <p className="font-mono text-emerald-300">{simulationResult.projectedLatency}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
