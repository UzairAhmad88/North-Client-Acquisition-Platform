'use client';

import React, { useState, useEffect } from 'react';
import { listProjectChanges, getChangeDetail, triageChange, analyzeChangeImpact, ChangeRequest } from '@/lib/api/changes';
import { ChangeList } from './ChangeList';
import { ChangeImpactPanel } from './ChangeImpactPanel';
import { ChangeCommercialImpact } from './ChangeCommercialImpact';
import { ChangeApprovalPanel } from './ChangeApprovalPanel';
import { GitPullRequest, Layers, Sparkles, Filter, ShieldCheck, Plus, ArrowRight } from 'lucide-react';

interface ChangeWorkspaceProps {
  projectId: string;
}

export const ChangeWorkspace: React.FC<ChangeWorkspaceProps> = ({ projectId }) => {
  const [changes, setChanges] = useState<ChangeRequest[]>([]);
  const [selectedChange, setSelectedChange] = useState<ChangeRequest | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadChanges();
  }, [projectId]);

  const loadChanges = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listProjectChanges(projectId);
      setChanges(data);
      if (data.length > 0 && !selectedChange) {
        setSelectedChange(data[0]);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch change requests.');
    } finally {
      setLoading(false);
    }
  };

  const handleRunTriage = async () => {
    if (!selectedChange) return;
    setAnalyzing(true);
    try {
      const triaged = await triageChange(selectedChange.id);
      setSelectedChange(triaged);
      setChanges((prev) => prev.map((c) => (c.id === triaged.id ? triaged : c)));
    } catch (err: any) {
      setError(err?.message || 'Failed to triage request.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleRunImpactAnalysis = async () => {
    if (!selectedChange) return;
    setAnalyzing(true);
    try {
      await analyzeChangeImpact(selectedChange.id);
      const updated = await getChangeDetail(selectedChange.id);
      setSelectedChange(updated);
      setChanges((prev) => prev.map((c) => (c.id === updated.id ? updated : c)));
    } catch (err: any) {
      setError(err?.message || 'Failed to execute impact analysis.');
    } finally {
      setAnalyzing(false);
    }
  };

  const activeVersion = selectedChange?.versions?.[0];

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4 sm:p-6 text-slate-100">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-blue-600/10 border border-blue-500/20 rounded-xl text-blue-400">
            <GitPullRequest className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-black text-white tracking-tight">Change Request & Scope Control</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Phase 28 — Controlled Scope & Commercial Governance Engine • Project ID: <code className="text-slate-300">{projectId}</code>
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3 bg-slate-950 px-4 py-2.5 rounded-xl border border-slate-800">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <div className="text-xs">
            <div className="font-semibold text-slate-200">Baseline Lock Active</div>
            <div className="text-[10px] text-slate-400">Unapproved Requests Cannot Alter Scope</div>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-950/40 border border-red-800/50 rounded-lg text-xs text-red-300">
          {error}
        </div>
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Change List */}
        <div className="md:col-span-1">
          <ChangeList
            changes={changes}
            selectedChangeId={selectedChange?.id}
            onSelectChange={(c) => setSelectedChange(c)}
          />
        </div>

        {/* Right Column: Selected Change Detail & Controls */}
        <div className="md:col-span-2 space-y-6">
          {selectedChange ? (
            <>
              {/* Change Request Detail Header Card */}
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
                <div className="flex items-start justify-between border-b border-slate-800 pb-3">
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="font-mono text-xs font-bold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                        {selectedChange.change_number}
                      </span>
                      <h2 className="text-lg font-bold text-white">{selectedChange.title}</h2>
                    </div>
                    <p className="text-xs text-slate-400 mt-1">Requested by {selectedChange.requested_by} • Source: {selectedChange.source}</p>
                  </div>
                  <span className="px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    {selectedChange.classification}
                  </span>
                </div>

                <div className="space-y-1 text-xs">
                  <span className="text-slate-400 font-medium">Request Description:</span>
                  <p className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-300 whitespace-pre-wrap">
                    {selectedChange.description}
                  </p>
                </div>

                {/* AI Change Agent Quick Actions */}
                <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-800">
                  <button
                    onClick={handleRunTriage}
                    disabled={analyzing}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded text-xs font-semibold text-slate-200 border border-slate-700 flex items-center space-x-1.5"
                  >
                    <Filter className="w-3.5 h-3.5 text-blue-400" />
                    <span>Run AI Triage</span>
                  </button>

                  <button
                    onClick={handleRunImpactAnalysis}
                    disabled={analyzing}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded text-xs font-semibold text-slate-200 border border-slate-700 flex items-center space-x-1.5"
                  >
                    <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                    <span>Execute Impact Analysis</span>
                  </button>
                </div>
              </div>

              {/* Impact Panel */}
              <ChangeImpactPanel version={activeVersion} />

              {/* Commercial Impact Panel */}
              <ChangeCommercialImpact />

              {/* Approval Controls */}
              <ChangeApprovalPanel change={selectedChange} onRefresh={loadChanges} />
            </>
          ) : (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center text-xs text-slate-500">
              Select a change request from the left sidebar to inspect impact and approval controls.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
