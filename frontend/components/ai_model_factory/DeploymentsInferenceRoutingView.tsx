import React from 'react';
import { AiDeploymentItem } from '@/lib/api/aiModelFactory';

interface Props {
  deployments: AiDeploymentItem[];
}

export const DeploymentsInferenceRoutingView: React.FC<Props> = ({ deployments }) => {
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-100">Live Deployments & Policy Inference Routing</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Canary rollouts, traffic weighting, latency-driven routing gateways, and instant rollback controls.
          </p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono">
          {deployments.length} Active Endpoints
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {deployments.map((d) => (
          <div key={d.id} className="p-4 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="text-sm font-bold text-white font-mono">{d.environment} Endpoint</h4>
                <p className="text-xs text-slate-400 mt-0.5">Strategy: {d.strategy}</p>
              </div>
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">
                {d.traffic_weight_pct}% Traffic
              </span>
            </div>

            <div className="bg-slate-900/70 p-2.5 rounded border border-slate-800 text-xs font-mono text-slate-300 space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>Endpoint URL:</span>
                <span className="text-slate-200 truncate max-w-[200px]">{d.endpoint_url}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Autoscaling Replicas:</span>
                <span className="text-indigo-300">{d.current_replicas} / {d.max_replicas} pods</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>P95 Latency:</span>
                <span className="text-emerald-400">24.5 ms</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-slate-700/40 text-xs">
              <span className="text-slate-500 text-[10px] font-mono">Rollback Target: {d.rollback_target_version_id || 'Pinned Stable'}</span>
              <button
                disabled
                className="px-2.5 py-1 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-mono cursor-not-allowed opacity-80"
              >
                Instant Rollback
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
