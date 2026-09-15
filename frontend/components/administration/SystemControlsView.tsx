'use client';

import React, { useState } from 'react';
import { KillSwitchItem, administrationApi } from '@/lib/api/administration';

interface SystemControlsViewProps {
  switches: KillSwitchItem[];
  onRefresh: () => void;
}

export function SystemControlsView({ switches, onRefresh }: SystemControlsViewProps) {
  const [selectedSwitch, setSelectedSwitch] = useState<KillSwitchItem | null>(null);
  const [actionType, setActionType] = useState<'ACTIVATE' | 'RELEASE'>('ACTIVATE');
  const [reason, setReason] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleConfirmAction = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSwitch) return;
    setIsProcessing(true);
    try {
      if (actionType === 'ACTIVATE') {
        await administrationApi.activateKillSwitch(
          selectedSwitch.switch_id,
          reason || 'Manual activation via Administration Control Center'
        );
      } else {
        await administrationApi.releaseKillSwitch(selectedSwitch.switch_id);
      }
      setSelectedSwitch(null);
      setReason('');
      onRefresh();
    } catch (err: any) {
      alert(`Operation failed: ${err.message || err}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Critical Warning Alert */}
      <div className="bg-rose-950/40 border border-rose-800/80 rounded-2xl p-5 backdrop-blur flex items-start gap-4">
        <span className="text-2xl mt-0.5">⚠️</span>
        <div className="space-y-1">
          <h3 className="text-sm font-bold text-rose-200 uppercase tracking-wide">
            Emergency Platform Control & Circuit Interruption
          </h3>
          <p className="text-xs text-rose-300/80 leading-relaxed">
            Emergency kill switches immediately suspend subsystems, disarm background workers, or block outbound communication.
            Activating a kill switch takes effect globally in sub-millisecond time. Every state transition is permanently logged.
          </p>
        </div>
      </div>

      {/* Switches Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {switches.map((item) => {
          const isActive = item.state === 'ACTIVE';
          return (
            <div
              key={item.switch_id}
              className={`border rounded-2xl p-5 transition flex flex-col justify-between ${
                isActive
                  ? 'bg-rose-950/20 border-rose-700/80 shadow-lg shadow-rose-950/30'
                  : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h4 className="text-sm font-bold text-white">{item.name}</h4>
                    <code className="text-[11px] font-mono text-slate-400 block mt-0.5">
                      {item.switch_id}
                    </code>
                  </div>
                  <span
                    className={`text-[10px] font-bold uppercase px-2.5 py-1 rounded-full border ${
                      isActive
                        ? 'bg-rose-600 text-white border-rose-500 animate-pulse'
                        : 'bg-emerald-950 text-emerald-300 border-emerald-800'
                    }`}
                  >
                    {isActive ? 'ENGAGED / ACTIVE' : 'DISARMED'}
                  </span>
                </div>

                <div className="mt-4 space-y-1 text-xs text-slate-400">
                  <div className="flex justify-between">
                    <span>Scope Level:</span>
                    <strong className="text-slate-200">{item.level}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Target Target:</span>
                    <strong className="text-slate-200">{item.target_identifier}</strong>
                  </div>
                  {item.activated_at && (
                    <div className="flex justify-between text-rose-300">
                      <span>Activated At:</span>
                      <span>{new Date(item.activated_at).toLocaleTimeString()}</span>
                    </div>
                  )}
                  {item.reason && (
                    <p className="text-[11px] bg-black/40 p-2 rounded text-slate-300 mt-2 font-mono">
                      Reason: {item.reason}
                    </p>
                  )}
                </div>
              </div>

              <div className="mt-5 pt-3 border-t border-slate-800 flex justify-end gap-2">
                {isActive ? (
                  <button
                    onClick={() => {
                      setSelectedSwitch(item);
                      setActionType('RELEASE');
                    }}
                    className="w-full bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold py-2 px-4 rounded-xl transition"
                  >
                    Disarm / Restore Operations
                  </button>
                ) : (
                  <button
                    onClick={() => {
                      setSelectedSwitch(item);
                      setActionType('ACTIVATE');
                    }}
                    className="w-full bg-rose-700 hover:bg-rose-600 text-white text-xs font-semibold py-2 px-4 rounded-xl transition"
                  >
                    Engage Emergency Kill Switch
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Confirmation Modal */}
      {selectedSwitch && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center gap-3">
              <span className="text-3xl">{actionType === 'ACTIVATE' ? '🛑' : '🟢'}</span>
              <div>
                <h4 className="text-base font-bold text-white">
                  {actionType === 'ACTIVATE' ? 'Engage Emergency Kill Switch' : 'Disarm Kill Switch'}
                </h4>
                <p className="text-xs text-slate-400">{selectedSwitch.name}</p>
              </div>
            </div>

            <form onSubmit={handleConfirmAction} className="space-y-4 pt-2">
              {actionType === 'ACTIVATE' && (
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Mandatory Incident Reason</label>
                  <input
                    type="text"
                    placeholder="e.g., Contain security anomaly or critical defect"
                    value={reason}
                    onChange={(e) => setReason(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-200"
                    required
                  />
                </div>
              )}

              <p className="text-xs text-slate-400 bg-slate-950 p-3 rounded-lg border border-slate-800">
                {actionType === 'ACTIVATE'
                  ? 'All matching outbound and internal execution requests will be blocked immediately.'
                  : 'Normal execution and traffic flow will resume immediately across target subsystems.'}
              </p>

              <div className="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setSelectedSwitch(null)}
                  className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isProcessing}
                  className={`px-4 py-2 text-white rounded-lg text-xs font-bold transition ${
                    actionType === 'ACTIVATE'
                      ? 'bg-rose-600 hover:bg-rose-500'
                      : 'bg-emerald-600 hover:bg-emerald-500'
                  }`}
                >
                  {isProcessing ? 'Processing...' : 'Confirm Action'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
