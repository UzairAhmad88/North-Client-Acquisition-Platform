'use client';

import React, { useState, useEffect } from 'react';
import { listConflicts, resolveConflict, KnowledgeConflict } from '@/lib/api/knowledge';
import { AlertOctagon, CheckCircle2, ShieldAlert, User, Check, X } from 'lucide-react';

export default function ConflictPanelComponent() {
  const [conflicts, setConflicts] = useState<KnowledgeConflict[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedConflict, setSelectedConflict] = useState<KnowledgeConflict | null>(null);
  const [signer, setSigner] = useState('lead_architect');
  const [notes, setNotes] = useState('');
  const [resolving, setResolving] = useState(false);

  const fetchConflicts = async () => {
    setLoading(true);
    try {
      const data = await listConflicts();
      setConflicts(data);
    } catch (err) {
      console.error('Failed to load conflicts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConflicts();
  }, []);

  const handleResolve = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedConflict || !notes.trim()) return;

    setResolving(true);
    try {
      await resolveConflict(selectedConflict.conflict_code, {
        resolved_by: signer.trim(),
        resolution_notes: notes.trim(),
      });
      setSelectedConflict(null);
      setNotes('');
      fetchConflicts();
    } catch (err) {
      console.error('Failed to resolve conflict:', err);
    } finally {
      setResolving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <AlertOctagon className="w-5 h-5 text-amber-500" />
            Contradiction Detection & Human Conflict Governance
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Section 12 & 42: Enforces Rule 9 - Contradictions across client messages, requirements, and policies must NEVER be silently auto-resolved.
          </p>
        </div>
        <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
          {conflicts.length} Open Contradictions
        </span>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-500 animate-pulse bg-white rounded-xl border border-slate-200">
          Scanning facts and claims for active contradictions...
        </div>
      ) : conflicts.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-2xl border border-slate-200 space-y-2">
          <CheckCircle2 className="w-10 h-10 text-emerald-500 mx-auto" />
          <h4 className="text-base font-bold text-slate-900">Zero Contradictions Detected</h4>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            All canonical facts and requirements across the knowledge base are consistent and mutually aligned.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {conflicts.map((c) => (
            <div
              key={c.conflict_code}
              className="bg-white p-6 rounded-2xl border border-amber-200 shadow-sm space-y-4"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded">
                      {c.conflict_code}
                    </span>
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-100 text-amber-800">
                      {c.status}
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-slate-900">{c.description}</h4>
                </div>

                <button
                  onClick={() => setSelectedConflict(c)}
                  className="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold rounded-lg shadow-sm transition-colors whitespace-nowrap"
                >
                  Review & Sign-off
                </button>
              </div>

              <div className="grid grid-cols-2 gap-4 text-xs bg-slate-50 p-3 rounded-xl border border-slate-100">
                <div>
                  <span className="text-slate-400 block">Claim Source A:</span>
                  <span className="font-mono font-bold text-slate-800">{c.source_a_code}</span>
                </div>
                <div>
                  <span className="text-slate-400 block">Claim Source B:</span>
                  <span className="font-mono font-bold text-slate-800">{c.source_b_code}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Resolution Modal */}
      {selectedConflict && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-base font-bold text-slate-900">Sign-off Conflict Resolution</h3>
              <button onClick={() => setSelectedConflict(null)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900">
              <span className="font-bold block mb-1">Non-Negotiable Rule 9 & 42:</span>
              Semantic similarity cannot resolve factual conflicts. Requires human authority sign-off.
            </div>

            <form onSubmit={handleResolve} className="space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Approving Authority Principal</label>
                <input
                  type="text"
                  required
                  value={signer}
                  onChange={(e) => setSigner(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:ring-1 focus:ring-amber-500"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Resolution Rationale & Action</label>
                <textarea
                  required
                  rows={3}
                  placeholder="Explain why Source A is confirmed over Source B and what action was taken..."
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:ring-1 focus:ring-amber-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setSelectedConflict(null)}
                  className="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={resolving}
                  className="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white font-semibold rounded-lg shadow-sm"
                >
                  {resolving ? 'Signing off...' : 'Confirm Resolution'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
