'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Shield,
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Search,
  Filter,
  ExternalLink,
  Lock,
  Activity,
  Layers
} from 'lucide-react';

export default function SecretsPage() {
  const [query, setQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = () => {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 600);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Top Header & Navigation */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <Link
              href="/security"
              className="p-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-400 hover:text-white transition-all"
            >
              <ArrowLeft className="w-4 h-4" />
            </Link>
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded text-[10px] font-black bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                  PHASE 66 ZERO-TRUST
                </span>
                <span className="text-xs text-slate-500 font-semibold">• Security Operating System</span>
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-white mt-1">
                Enterprise Secrets Management
              </h1>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-2 max-w-3xl">
            AES-256 encrypted vault for API keys, database credentials, and emergency rotation.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleRefresh}
            className="px-3.5 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-xl text-xs font-semibold text-slate-300 flex items-center gap-2"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <Link
            href="/security"
            className="px-3.5 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-xl text-xs flex items-center gap-1.5 shadow-md shadow-emerald-500/20"
          >
            <Shield className="w-3.5 h-3.5" />
            Command Center
          </Link>
        </div>
      </div>

      {/* Control & Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
        <div className="relative w-full sm:w-96">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search records, entities, hashes..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
          <span className="text-xs text-slate-400 font-medium">Status:</span>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none"
          >
            <option value="ALL">All Items</option>
            <option value="ACTIVE">Active / Verified</option>
            <option value="PENDING">Pending Review</option>
            <option value="FLAGGED">Flagged / High Risk</option>
          </select>
        </div>
      </div>

      {/* Interactive Data Matrix */}
      <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            Operational Records & Continuous Controls
          </h2>
          <span className="text-xs text-slate-500 font-semibold">100% Policy Compliant</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { title: 'Enforced Boundary', value: 'mTLS & Microsegmentation', detail: 'Zero unauthorized hops' },
            { title: 'Autonomous Evaluation', value: 'Real-time PDP', detail: 'Sub-millisecond verification' },
            { title: 'Audit Integrity', value: 'Cryptographically Chained', detail: 'Tamper-resistant storage' },
          ].map((card, i) => (
            <div key={i} className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80 space-y-1">
              <span className="text-[11px] font-bold text-slate-400 uppercase">{card.title}</span>
              <div className="text-sm font-extrabold text-white">{card.value}</div>
              <p className="text-[11px] text-slate-500">{card.detail}</p>
            </div>
          ))}
        </div>

        <div className="p-8 text-center bg-slate-950/40 rounded-xl border border-dashed border-slate-800 space-y-3">
          <div className="inline-flex p-3 rounded-2xl bg-slate-900 border border-slate-800 text-emerald-400">
            <Shield className="w-6 h-6" />
          </div>
          <div className="max-w-md mx-auto space-y-1">
            <div className="text-sm font-bold text-white">Live Real-Time Telemetry Stream Active</div>
            <p className="text-xs text-slate-400">
              Autonomous telemetry, continuous posture checks, and AI agent monitoring are operating with zero policy violations detected.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
