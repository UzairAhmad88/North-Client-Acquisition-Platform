'use client';

import React, { useState } from 'react';
import { ModelGovernance, predictiveApi } from '@/lib/api/predictive';

interface ModelGovernancePanelProps {
  models: ModelGovernance[];
  onRefresh: () => void;
}

export const ModelGovernancePanel: React.FC<ModelGovernancePanelProps> = ({ models, onRefresh }) => {
  const [approvingId, setApprovingId] = useState<string | null>(null);

  const handleApprove = async (modelId: string) => {
    setApprovingId(modelId);
    try {
      await predictiveApi.approveModel(modelId);
      onRefresh();
    } finally {
      setApprovingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-lg font-bold text-zinc-100">Production Model Registry & Lifecycle Governance</h3>
            <p className="text-xs text-zinc-400 mt-1">
              Zero autonomous deployment: all production models require explicit human review and approval.
            </p>
          </div>
          <span className="text-xs px-2.5 py-1 bg-purple-500/10 text-purple-300 font-semibold rounded border border-purple-500/20">
            Governance Rule v1.0
          </span>
        </div>

        <div className="space-y-4">
          {models.map((m) => (
            <div
              key={m.id}
              className="p-5 bg-zinc-950/70 border border-zinc-800 rounded-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4"
            >
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-indigo-400">{m.model_key}</span>
                  <span className="text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-medium">
                    Version: {m.current_version}
                  </span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-semibold ${
                      m.status === 'PRODUCTION'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : m.status === 'APPROVED'
                        ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20'
                        : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                    }`}
                  >
                    {m.status}
                  </span>
                </div>
                <h4 className="text-base font-bold text-zinc-100 mt-2">{m.name}</h4>
                <div className="flex items-center gap-4 text-xs text-zinc-400 mt-1">
                  <span>Algorithm: <strong className="text-zinc-200">{m.algorithm}</strong></span>
                  <span>Type: <strong className="text-zinc-200">{m.prediction_type}</strong></span>
                  {m.approved_by && <span>Approved by: <strong className="text-zinc-200">{m.approved_by}</strong></span>}
                </div>
              </div>

              {m.status === 'EXPERIMENTAL' && (
                <button
                  onClick={() => handleApprove(m.id)}
                  disabled={approvingId === m.id}
                  className="px-4 py-2 text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
                >
                  {approvingId === m.id ? 'Approving...' : 'Approve for Production'}
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
