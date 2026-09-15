'use client';

import React, { useState } from 'react';
import { SecurityEventItem } from '@/lib/api/securityOps';
import { Search, Filter, Shield, Lock, Eye, AlertCircle } from 'lucide-react';

interface SecurityEventTableProps {
  events: SecurityEventItem[];
  loading: boolean;
  onRefresh: () => void;
}

export default function SecurityEventTable({ events, loading, onRefresh }: SecurityEventTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');

  const categories = ['ALL', 'AUTHENTICATION', 'AUTHORIZATION', 'AI_SECURITY', 'API', 'DATA_ACCESS', 'ADMINISTRATION'];

  const filteredEvents = events.filter((evt) => {
    const matchesSearch =
      evt.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
      evt.principal_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (evt.resource_id || '').toLowerCase().includes(searchTerm.toLowerCase());

    const matchesCategory = selectedCategory === 'ALL' || evt.event_category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const getSeverityBadge = (severity: string) => {
    const s = severity.toLowerCase();
    if (s === 'critical') return 'bg-rose-100 text-rose-800 border-rose-300';
    if (s === 'high') return 'bg-orange-100 text-orange-800 border-orange-300';
    if (s === 'medium') return 'bg-amber-100 text-amber-800 border-amber-300';
    return 'bg-slate-100 text-slate-700 border-slate-300';
  };

  const getResultBadge = (result: string) => {
    const r = result.toUpperCase();
    if (r === 'DENY' || r === 'BLOCK' || r === 'FAILURE') {
      return 'bg-rose-50 text-rose-700 border-rose-200';
    }
    return 'bg-emerald-50 text-emerald-700 border-emerald-200';
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      {/* Header and Controls */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Shield className="w-5 h-5 text-indigo-600" />
            Canonical Security Telemetry Stream
          </h3>
          <p className="text-xs text-slate-500">
            Immutable normalized event ledger with strict zero-secret redaction (Section 6 & 48)
          </p>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search action, principal, resource..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-1.5 text-xs rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>

          <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-lg">
            <Filter className="w-3.5 h-3.5 text-slate-500 ml-1" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-transparent text-xs text-slate-700 focus:outline-none font-medium pr-2"
            >
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Secret Redaction Notice */}
      <div className="flex items-center gap-2 text-xs text-slate-500 bg-slate-50 px-3 py-2 rounded-lg border border-slate-100">
        <Lock className="w-3.5 h-3.5 text-emerald-600" />
        <span>Data Minimization Active: Passwords, tokens, and authorization secrets are masked before ledger entry.</span>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-700">
          <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-y border-slate-200">
            <tr>
              <th className="py-2.5 px-3">Timestamp</th>
              <th className="py-2.5 px-3">Category</th>
              <th className="py-2.5 px-3">Action</th>
              <th className="py-2.5 px-3">Principal</th>
              <th className="py-2.5 px-3">Target Resource</th>
              <th className="py-2.5 px-3">Result</th>
              <th className="py-2.5 px-3">Severity</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  Streaming events...
                </td>
              </tr>
            ) : filteredEvents.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-400">
                  No security events matching filter criteria.
                </td>
              </tr>
            ) : (
              filteredEvents.map((evt) => (
                <tr key={evt.security_event_id} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-2.5 px-3 text-slate-500 whitespace-nowrap">
                    {new Date(evt.timestamp).toLocaleTimeString()}
                  </td>
                  <td className="py-2.5 px-3 font-medium text-slate-900 whitespace-nowrap">
                    {evt.event_category}
                  </td>
                  <td className="py-2.5 px-3 font-mono text-[11px] text-indigo-700">
                    {evt.action}
                  </td>
                  <td className="py-2.5 px-3 text-slate-600">
                    <span className="font-medium text-slate-800">{evt.principal_id}</span>
                    <span className="text-[10px] text-slate-400 ml-1">({evt.principal_type})</span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-600 font-mono text-[11px] truncate max-w-xs">
                    {evt.resource_id || evt.resource_type || '-'}
                  </td>
                  <td className="py-2.5 px-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${getResultBadge(evt.result)}`}>
                      {evt.result}
                    </span>
                  </td>
                  <td className="py-2.5 px-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${getSeverityBadge(evt.risk_level)}`}>
                      {evt.risk_level.toUpperCase()}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
