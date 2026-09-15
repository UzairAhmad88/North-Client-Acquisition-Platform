'use client';

import React from 'react';
import { ComponentHealth, CircuitBreakerState } from '@/lib/api/reliability';

interface Props {
  components: Record<string, ComponentHealth>;
  circuits: CircuitBreakerState[];
  onResetCircuit: (serviceName: string) => void;
}

export function DependencyHealthMatrix({ components, circuits, onResetCircuit }: Props) {
  const componentList = Object.values(components || {});

  return (
    <div className="space-y-6">
      {/* Component Probes Matrix */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center justify-between">
          <span>Subsystem & Dependency Health Checks</span>
          <span className="text-xs text-slate-400 font-normal">Real-time latency and fallback status</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {componentList.map((comp) => {
            const isHealthy = comp.status === 'HEALTHY';
            return (
              <div
                key={comp.component_name}
                className="bg-slate-950/60 border border-slate-800/80 p-4 rounded-xl flex flex-col justify-between hover:border-slate-700 transition"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-semibold text-slate-300 capitalize">{comp.component_name}</span>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        isHealthy
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                          : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      }`}
                    >
                      {comp.status}
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-400 mb-1">{comp.component_type}</div>
                  <div className="text-[11px] text-slate-500 truncate">{comp.message || 'Operational'}</div>
                </div>

                <div className="mt-4 pt-2 border-t border-slate-800/50 flex items-center justify-between text-[11px]">
                  <span className="text-slate-400">Latency:</span>
                  <span className={`font-mono font-medium ${comp.latency_ms > 200 ? 'text-amber-400' : 'text-emerald-400'}`}>
                    {comp.latency_ms.toFixed(1)} ms
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Circuit Breakers State Machine */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center justify-between">
          <span>Circuit Breakers & Fault Isolation</span>
          <span className="text-xs text-slate-400 font-normal">CLOSED $\rightarrow$ OPEN $\rightarrow$ HALF_OPEN</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {circuits.map((c) => {
            const isClosed = c.state === 'CLOSED';
            const isOpen = c.state === 'OPEN';
            return (
              <div key={c.service_name} className="bg-slate-950/60 border border-slate-800/80 p-4 rounded-xl">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-white uppercase">{c.service_name}</span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      isClosed
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : isOpen
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                    }`}
                  >
                    {c.state}
                  </span>
                </div>

                <div className="space-y-1 my-3 text-[11px] text-slate-400">
                  <div className="flex justify-between">
                    <span>Consecutive Failures:</span>
                    <span className="font-mono text-slate-200">{c.failure_count} / {c.failure_threshold}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Success Count:</span>
                    <span className="font-mono text-slate-200">{c.success_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Recovery Timeout:</span>
                    <span className="font-mono text-slate-200">{c.recovery_timeout}s</span>
                  </div>
                </div>

                {!isClosed && (
                  <button
                    onClick={() => onResetCircuit(c.service_name)}
                    className="w-full mt-2 py-1.5 bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 border border-cyan-500/30 rounded-lg text-xs font-medium transition"
                  >
                    Reset Circuit to CLOSED
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
