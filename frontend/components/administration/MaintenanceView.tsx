'use client';

import React, { useState } from 'react';
import { MaintenanceState, administrationApi } from '@/lib/api/administration';

interface MaintenanceViewProps {
  maintenance: MaintenanceState | null;
  onRefresh: () => void;
}

export function MaintenanceView({ maintenance, onRefresh }: MaintenanceViewProps) {
  const [showModal, setShowModal] = useState(false);
  const [mode, setMode] = useState<string>('PLANNED_MAINTENANCE');
  const [title, setTitle] = useState<string>('Scheduled Database & Core Infrastructure Upgrade');
  const [description, setDescription] = useState<string>(
    'Executing zero-downtime schema migrations and caching tier updates.'
  );
  const [internalBanner, setInternalBanner] = useState<string>(
    'PLATFORM MAINTENANCE: Background asynchronous tasks paused. Mutations are restricted.'
  );
  const [clientBanner, setClientBanner] = useState<string>(
    'Scheduled maintenance in progress. The platform remains operational in read-only mode.'
  );
  const [isProcessing, setIsProcessing] = useState(false);

  const isUnderMaintenance = maintenance?.current_mode !== 'NORMAL' && maintenance?.active_window?.is_active;

  const handleStartMaintenance = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsProcessing(true);
    try {
      await administrationApi.startMaintenance({
        mode,
        title,
        description,
        internal_banner: internalBanner,
        client_banner: clientBanner,
        affected_services: ['database', 'workflow_engine', 'billing'],
      });
      setShowModal(false);
      onRefresh();
    } catch (err: any) {
      alert(`Failed to enter maintenance mode: ${err.message || err}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleEndMaintenance = async () => {
    if (!confirm('Are you sure you want to end maintenance mode and restore full platform operations?')) return;
    setIsProcessing(true);
    try {
      await administrationApi.endMaintenance();
      onRefresh();
    } catch (err: any) {
      alert(`Failed to end maintenance mode: ${err.message || err}`);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Platform Status Banner */}
      <div
        className={`border rounded-2xl p-6 backdrop-blur flex flex-col md:flex-row justify-between items-start md:items-center gap-6 ${
          isUnderMaintenance
            ? 'bg-amber-950/30 border-amber-700/80 shadow-xl shadow-amber-950/20'
            : 'bg-emerald-950/20 border-emerald-800/60'
        }`}
      >
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <span className="text-3xl">{isUnderMaintenance ? '🚧' : '🛡️'}</span>
            <div>
              <div className="flex items-center gap-2.5">
                <h3 className="text-base font-bold text-white">Platform Operating State:</h3>
                <span
                  className={`text-xs font-extrabold uppercase px-3 py-1 rounded-full border ${
                    isUnderMaintenance
                      ? 'bg-amber-500 text-black border-amber-400 animate-pulse'
                      : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                  }`}
                >
                  {maintenance?.current_mode || 'NORMAL'}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1">
                State mutation capability:{' '}
                <strong className={maintenance?.is_mutation_allowed ? 'text-emerald-400' : 'text-rose-400'}>
                  {maintenance?.is_mutation_allowed ? 'UNRESTRICTED (Read-Write)' : 'LOCKED (Read-Only)'}
                </strong>
              </p>
            </div>
          </div>
        </div>

        <div>
          {isUnderMaintenance ? (
            <button
              onClick={handleEndMaintenance}
              disabled={isProcessing}
              className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2.5 px-6 rounded-xl text-xs shadow-lg transition"
            >
              {isProcessing ? 'Restoring...' : 'End Maintenance & Restore Normal Operations'}
            </button>
          ) : (
            <button
              onClick={() => setShowModal(true)}
              className="bg-amber-600 hover:bg-amber-500 text-black font-bold py-2.5 px-6 rounded-xl text-xs shadow-lg transition"
            >
              Initiate Maintenance Window
            </button>
          )}
        </div>
      </div>

      {/* Active Maintenance Details Card */}
      {isUnderMaintenance && maintenance?.active_window && (
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 backdrop-blur space-y-4">
          <h4 className="text-sm font-bold text-white flex items-center gap-2">
            <span>📢</span>
            <span>Active Maintenance Window Broadcasts</span>
          </h4>

          <div className="space-y-3 text-xs">
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-[10px] text-indigo-400 uppercase font-bold block mb-1">
                Internal Console Banner
              </span>
              <p className="text-slate-200 font-mono">{maintenance.active_window.internal_banner}</p>
            </div>

            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-[10px] text-cyan-400 uppercase font-bold block mb-1">
                Client Portal Banner
              </span>
              <p className="text-slate-200 font-mono">{maintenance.active_window.client_portal_banner}</p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-slate-400 pt-2 text-[11px]">
              <div>
                <span>Title:</span> <strong className="text-white block">{maintenance.active_window.title}</strong>
              </div>
              <div>
                <span>Initiated By:</span>{' '}
                <strong className="text-white block">{maintenance.active_window.initiated_by}</strong>
              </div>
              <div>
                <span>Started:</span>{' '}
                <strong className="text-white block">
                  {new Date(maintenance.active_window.start_time).toLocaleTimeString()}
                </strong>
              </div>
              <div>
                <span>Affected Services:</span>{' '}
                <strong className="text-white block">
                  {maintenance.active_window.affected_services?.join(', ') || 'All'}
                </strong>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Start Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <h4 className="text-base font-bold text-white">Initiate Platform Maintenance Mode</h4>
            <p className="text-xs text-slate-400">
              Entering maintenance mode protects database integrity by transitioning subsystems to read-only mode and broadcasting system notices.
            </p>

            <form onSubmit={handleStartMaintenance} className="space-y-3 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Maintenance Mode</label>
                <select
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                >
                  <option value="PLANNED_MAINTENANCE">PLANNED_MAINTENANCE</option>
                  <option value="EMERGENCY_READ_ONLY">EMERGENCY_READ_ONLY</option>
                  <option value="DEGRADED_SERVICE">DEGRADED_SERVICE</option>
                  <option value="OUTAGE">OUTAGE</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Internal Notice Banner</label>
                <input
                  type="text"
                  value={internalBanner}
                  onChange={(e) => setInternalBanner(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Client Portal Banner</label>
                <input
                  type="text"
                  value={clientBanner}
                  onChange={(e) => setClientBanner(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                />
              </div>

              <div className="flex justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isProcessing}
                  className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-black rounded-lg text-xs font-bold"
                >
                  {isProcessing ? 'Initiating...' : 'Activate Maintenance Mode'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
