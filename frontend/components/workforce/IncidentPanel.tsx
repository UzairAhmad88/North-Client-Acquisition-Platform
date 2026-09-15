'use client';

import React, { useState } from 'react';
import { AlertOctagon, ShieldAlert, Power, CheckCircle2, Lock } from 'lucide-react';

interface IncidentPanelProps {
  onTriggerKillSwitch?: (targetType: string, targetIdentifier: string, reason: string) => Promise<void>;
}

export const IncidentPanel: React.FC<IncidentPanelProps> = ({ onTriggerKillSwitch }) => {
  const [targetType, setTargetType] = useState('WORKER');
  const [targetId, setTargetId] = useState('');
  const [reason, setReason] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const handleActivate = async () => {
    if (!targetId.trim() || !reason.trim() || !onTriggerKillSwitch) return;
    setIsSubmitting(true);
    setStatusMsg(null);
    try {
      await onTriggerKillSwitch(targetType, targetId, reason);
      setStatusMsg(`Emergency kill switch successfully activated for ${targetType}: ${targetId}`);
      setTargetId('');
      setReason('');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Warning Banner */}
      <div className="p-5 rounded-xl border border-rose-500/30 bg-gradient-to-r from-rose-950/40 via-slate-900/80 to-rose-950/20">
        <div className="flex items-center gap-2">
          <AlertOctagon className="h-5 w-5 text-rose-400" />
          <h2 className="text-lg font-bold text-white tracking-tight">Authoritative Workforce Emergency Controls</h2>
        </div>
        <p className="text-xs text-slate-300 mt-1">
          Instant execution trip gates. Authoritative security operators can immediately suspend global, departmental, or worker-level execution during threat incidents.
        </p>
      </div>

      {statusMsg && (
        <div className="p-4 rounded-xl border border-emerald-500/30 bg-emerald-950/20 text-xs text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="h-4 w-4 text-emerald-400" />
          <span>{statusMsg}</span>
        </div>
      )}

      {/* Kill Switch Form */}
      <div className="p-5 rounded-xl border border-slate-700/60 bg-slate-900/60 backdrop-blur-sm space-y-4">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <Lock className="h-4 w-4 text-rose-400" />
          Activate Emergency Kill Switch
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-slate-400 block mb-1">Target Boundary</label>
            <select
              value={targetType}
              onChange={(e) => setTargetType(e.target.value)}
              className="w-full rounded-lg bg-slate-950/80 border border-slate-700/80 p-2.5 text-xs text-white focus:outline-none focus:border-rose-500"
            >
              <option value="WORKER">Specific Worker (e.g. WRK-RESEARCH-01)</option>
              <option value="TEAM">Specific Squad (e.g. TEAM-DISCOVERY-01)</option>
              <option value="DEPARTMENT">Department (e.g. DEPT-SALES)</option>
              <option value="GLOBAL_WORKFORCE">Global AI Workforce</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-400 block mb-1">Target Identifier</label>
            <input
              type="text"
              value={targetId}
              onChange={(e) => setTargetId(e.target.value)}
              placeholder="e.g. WRK-RESEARCH-01 or GLOBAL"
              className="w-full rounded-lg bg-slate-950/80 border border-slate-700/80 p-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-rose-500"
            />
          </div>
        </div>

        <div>
          <label className="text-xs font-semibold text-slate-400 block mb-1">Audit Justification & Incident Reason</label>
          <textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Document security or policy violation requiring immediate workforce suspension..."
            className="w-full h-18 rounded-lg bg-slate-950/80 border border-slate-700/80 p-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-rose-500"
          />
        </div>

        <div className="flex justify-end">
          <button
            disabled={isSubmitting || !targetId.trim() || !reason.trim()}
            onClick={handleActivate}
            className="px-4 py-2.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold flex items-center gap-2 shadow-lg shadow-rose-600/20 disabled:opacity-50 transition-all cursor-pointer"
          >
            <Power className="h-4 w-4" />
            Trigger Authoritative Kill Switch
          </button>
        </div>
      </div>
    </div>
  );
};
