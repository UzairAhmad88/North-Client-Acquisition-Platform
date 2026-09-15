'use client';

import React, { useState } from 'react';
import { HandoverChecklist, completeHandover } from '@/lib/api/qa';
import { Award, CheckCircle2, Lock, FileText, Key, BookOpen, ShieldCheck } from 'lucide-react';

interface HandoverAcceptancePanelProps {
  checklist: HandoverChecklist | null;
  projectId: string;
  onRefresh: () => void;
}

export const HandoverAcceptancePanel: React.FC<HandoverAcceptancePanelProps> = ({ checklist, projectId, onRefresh }) => {
  const [signerId, setSignerId] = useState('Client Principal');
  const [statement, setStatement] = useState('I confirm receipt of all code, documentation, and credentials, and approve final project handover.');
  const [completing, setCompleting] = useState(false);

  const handleCompleteHandover = async (e: React.FormEvent) => {
    e.preventDefault();
    setCompleting(true);
    try {
      await completeHandover(projectId, {
        client_signer_id: signerId,
        signoff_statement: statement,
      });
      onRefresh();
      alert('Final project handover completed and project closed with status COMPLETED!');
    } catch (err: any) {
      alert(err?.message || 'Failed to complete project handover.');
    } finally {
      setCompleting(false);
    }
  };

  const isCompleted = checklist?.signed_off_by_client || checklist?.status === 'COMPLETED';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-amber-500/10 border border-amber-500/20 rounded-lg text-amber-400">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Delivery Acceptance & Handover Governance</h2>
            <p className="text-xs text-slate-400">Complete final code repository transfer, documentation delivery, and project sign-off</p>
          </div>
        </div>

        {isCompleted && (
          <span className="px-3.5 py-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-black flex items-center space-x-1.5">
            <CheckCircle2 className="w-4 h-4" />
            <span>PROJECT COMPLETED & HANDED OVER</span>
          </span>
        )}
      </div>

      {/* Handover Requirements Verification Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex items-center space-x-3">
          <FileText className={`w-5 h-5 ${checklist?.code_repository_transferred || isCompleted ? 'text-emerald-400' : 'text-slate-500'}`} />
          <div>
            <div className="text-xs font-semibold text-slate-200">Code Repository</div>
            <div className="text-[10px] text-slate-400">Source code access & IP transfer</div>
          </div>
        </div>

        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex items-center space-x-3">
          <BookOpen className={`w-5 h-5 ${checklist?.documentation_delivered || isCompleted ? 'text-emerald-400' : 'text-slate-500'}`} />
          <div>
            <div className="text-xs font-semibold text-slate-200">Technical Documentation</div>
            <div className="text-[10px] text-slate-400">Architecture docs & runbooks</div>
          </div>
        </div>

        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex items-center space-x-3">
          <Key className={`w-5 h-5 ${checklist?.credentials_transferred || isCompleted ? 'text-emerald-400' : 'text-slate-500'}`} />
          <div>
            <div className="text-xs font-semibold text-slate-200">Credentials & Vault</div>
            <div className="text-[10px] text-slate-400">Secrets & production keys</div>
          </div>
        </div>
      </div>

      {/* Handover Final Sign-off Form */}
      {isCompleted ? (
        <div className="bg-emerald-950/30 border border-emerald-800/40 rounded-xl p-5 space-y-2 text-xs text-emerald-300">
          <div className="flex items-center space-x-2 font-bold text-sm">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <span>Final Handover Signed Off & Project Formally Closed</span>
          </div>
          <p className="text-slate-300">
            Client Sign-off Hash: <code className="font-mono text-emerald-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">{checklist?.client_signoff_hash}</code>
          </p>
          <p className="text-[11px] text-slate-400">Signed off at {new Date(checklist?.signed_off_at || '').toLocaleString()}</p>
        </div>
      ) : (
        <form onSubmit={handleCompleteHandover} className="bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <Lock className="w-4 h-4 text-amber-400" />
            <span>Authorize Final Handover & Close Engagement</span>
          </h3>

          <div>
            <label className="text-xs text-slate-400 block mb-1">Signer Name / Organization Title</label>
            <input
              type="text"
              required
              value={signerId}
              onChange={(e) => setSignerId(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
            />
          </div>

          <div>
            <label className="text-xs text-slate-400 block mb-1">Final Handover Statement</label>
            <textarea
              required
              rows={3}
              value={statement}
              onChange={(e) => setStatement(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
            />
          </div>

          <button
            type="submit"
            disabled={completing}
            className="w-full py-2.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-bold shadow-xl transition"
          >
            {completing ? 'Completing Handover...' : 'Sign Off Handover & Close Project'}
          </button>
        </form>
      )}
    </div>
  );
};
