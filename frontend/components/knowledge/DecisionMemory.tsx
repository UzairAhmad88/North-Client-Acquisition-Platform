'use client';

import React, { useState, useEffect } from 'react';
import { listDecisions, DecisionRecord } from '@/lib/api/knowledge';
import { Layers, CheckCircle2, User, FileText, Calendar, Search } from 'lucide-react';

export default function DecisionMemoryComponent() {
  const [decisions, setDecisions] = useState<DecisionRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    async function loadDecisions() {
      setLoading(true);
      try {
        const data = await listDecisions();
        setDecisions(data);
      } catch (err) {
        console.error('Failed to load decisions:', err);
      } finally {
        setLoading(false);
      }
    }
    loadDecisions();
  }, []);

  const filtered = decisions.filter(
    (d) =>
      d.title.toLowerCase().includes(filter.toLowerCase()) ||
      d.rationale.toLowerCase().includes(filter.toLowerCase()) ||
      d.decision_code.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Layers className="w-5 h-5 text-indigo-600" />
            Decision Memory & Architectural Records
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Section 26: Searchable organizational decision history with full context background, trade-off options, rationale, approvers, and evidence links.
          </p>
        </div>

        <div className="relative w-full md:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Filter decisions..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-500 animate-pulse bg-white rounded-xl border border-slate-200">
          Loading decision memory records...
        </div>
      ) : filtered.length === 0 ? (
        <div className="p-8 text-center bg-white rounded-xl border border-slate-200 text-slate-500 text-sm">
          No matching decisions found.
        </div>
      ) : (
        <div className="space-y-4">
          {filtered.map((d) => (
            <div key={d.decision_code} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
                      {d.decision_code}
                    </span>
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">
                      {d.status}
                    </span>
                  </div>
                  <h4 className="text-base font-bold text-slate-900">{d.title}</h4>
                </div>
                <span className="text-xs text-slate-400 flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5" />
                  {new Date(d.decided_at).toLocaleDateString()}
                </span>
              </div>

              <div className="space-y-2 text-xs">
                <div>
                  <span className="font-semibold text-slate-500 block mb-0.5">Core Question:</span>
                  <p className="text-slate-800 bg-slate-50 p-2.5 rounded-lg border border-slate-100">{d.question}</p>
                </div>

                <div>
                  <span className="font-semibold text-slate-500 block mb-0.5">Rationale:</span>
                  <p className="text-slate-800 bg-indigo-50/50 p-2.5 rounded-lg border border-indigo-100/60 leading-relaxed">
                    {d.rationale}
                  </p>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between pt-3 border-t border-slate-100 text-xs text-slate-500 gap-2">
                <div className="flex items-center gap-3">
                  <span>Owner: <strong>{d.owner_id}</strong></span>
                  <span>Approvers: <strong>{d.approver_ids?.join(', ') || 'Lead'}</strong></span>
                </div>
                <div>
                  Evidence: <span className="font-mono">{d.evidence_references?.join(', ') || 'N/A'}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
