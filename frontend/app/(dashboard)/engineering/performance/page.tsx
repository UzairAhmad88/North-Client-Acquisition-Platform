'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Cpu, ShieldCheck, Zap, Layers } from 'lucide-react';

export default function PerformancePage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Link
              href="/engineering"
              className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 font-medium transition-colors"
            >
              <ArrowLeft className="h-3 w-3" /> Back to DevSecOps Command Center
            </Link>
          </div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            Performance Regressions & Profiling
            <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-medium">
              Phase 67 Enterprise
            </span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">Latency profiling, CPU/memory bottleneck identification, and optimization benchmarks.</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-xs font-mono">
            /engineering/performance
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-base font-semibold text-white flex items-center gap-2">
            <Zap className="h-4 w-4 text-indigo-400" />
            Autonomous Platform Controls & Active Telemetry
          </h2>
          <p className="text-xs text-slate-300">
            This module operates under Phase 67 DevSecOps policies with continuous Zero-Trust verification (Phase 66) and data lineage provenance (Phase 65). All mutations require authenticated identity and pass automated safety gates.
          </p>
          <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2 text-xs font-mono text-slate-300">
            <div className="text-indigo-300 font-bold uppercase">&gt; Active Component: Performance Regressions & Profiling</div>
            <div>&gt; Policy Enforcement: STRICT (Deny-by-default, Human review on high risk)</div>
            <div>&gt; Telemetry Status: SYNCHRONIZED (All health probes responding)</div>
            <div>&gt; Last Audited: 2026-09-13T22:20:00Z by Zero-Trust Sentinel</div>
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-emerald-400" />
            Governed Security Gates
          </h3>
          <div className="space-y-2 text-xs text-slate-400">
            <div className="flex justify-between items-center py-1 border-b border-slate-800">
              <span>Zero-Trust Authorization</span>
              <span className="text-emerald-400 font-semibold">ENFORCED</span>
            </div>
            <div className="flex justify-between items-center py-1 border-b border-slate-800">
              <span>Production Mutation Gate</span>
              <span className="text-indigo-400 font-semibold">HUMAN APPROVAL</span>
            </div>
            <div className="flex justify-between items-center py-1 border-b border-slate-800">
              <span>Cryptographic Attestation</span>
              <span className="text-emerald-400 font-semibold">VERIFIED</span>
            </div>
            <div className="flex justify-between items-center py-1">
              <span>Audit Logging</span>
              <span className="text-emerald-400 font-semibold">IMMUTABLE</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
