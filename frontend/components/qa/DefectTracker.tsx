'use client';

import React, { useState } from 'react';
import { Defect, createDefect, updateDefectStatus } from '@/lib/api/qa';
import { AlertTriangle, Plus, CheckCircle2, Filter, ShieldAlert, Tag } from 'lucide-react';

interface DefectTrackerProps {
  defects: Defect[];
  projectId: string;
  onRefresh: () => void;
}

export const DefectTracker: React.FC<DefectTrackerProps> = ({ defects, projectId, onRefresh }) => {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleCreateDefect = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !description) return;
    setSubmitting(true);
    try {
      await createDefect(projectId, {
        title,
        description,
        reported_by: 'QA Specialist',
      });
      setTitle('');
      setDescription('');
      setShowCreateModal(false);
      onRefresh();
    } catch (err: any) {
      alert(err?.message || 'Failed to submit defect report.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleStatusChange = async (defectId: string, newStatus: string) => {
    try {
      await updateDefectStatus(defectId, {
        status: newStatus,
        resolution_summary: `Status updated to ${newStatus} by QA Lead`,
      });
      onRefresh();
    } catch (err: any) {
      alert(err?.message || 'Failed to update defect status.');
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400">
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Defect Tracking & Triage Engine</h2>
            <p className="text-xs text-slate-400">Classify issue severity, track resolutions, and enforce release gates</p>
          </div>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="px-3.5 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg text-xs font-semibold shadow-lg transition flex items-center space-x-1.5"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Report Defect</span>
        </button>
      </div>

      {/* Modal for reporting defect */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 max-w-lg w-full shadow-2xl space-y-4">
            <h3 className="text-base font-bold text-white">Report New Defect</h3>
            <form onSubmit={handleCreateDefect} className="space-y-4">
              <div>
                <label className="text-xs text-slate-400 font-medium block mb-1">Defect Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g., Payment calculation fails on discounted checkout"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-red-500"
                />
              </div>

              <div>
                <label className="text-xs text-slate-400 font-medium block mb-1">Detailed Description & Steps to Reproduce</label>
                <textarea
                  required
                  rows={4}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Steps to reproduce, expected result vs actual result..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-red-500"
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-xs font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg text-xs font-semibold shadow-lg"
                >
                  {submitting ? 'Submitting...' : 'Submit Report'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Defects List */}
      <div className="space-y-3">
        {defects.length > 0 ? (
          defects.map((def) => (
            <div key={def.id} className="bg-slate-950 border border-slate-800/80 rounded-lg p-4 space-y-2">
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-xs font-bold text-red-400 bg-red-500/10 px-2 py-0.5 rounded border border-red-500/20">
                    {def.defect_number}
                  </span>
                  <h4 className="text-sm font-semibold text-white">{def.title}</h4>
                </div>

                <div className="flex items-center space-x-2">
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      def.severity === 'CRITICAL'
                        ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                        : def.severity === 'HIGH'
                        ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                        : 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    }`}
                  >
                    {def.severity}
                  </span>

                  <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300 border border-slate-700">
                    {def.classification}
                  </span>
                </div>
              </div>

              <p className="text-xs text-slate-300">{def.description}</p>

              <div className="flex items-center justify-between pt-2 border-t border-slate-800/50 text-[11px]">
                <span className="text-slate-400">Reported by {def.reported_by}</span>

                <div className="flex items-center space-x-1.5">
                  <span className="text-slate-500 mr-1">Status: <strong className="text-slate-200">{def.status}</strong></span>
                  {def.status !== 'RESOLVED' && (
                    <button
                      onClick={() => handleStatusChange(def.id, 'RESOLVED')}
                      className="px-2.5 py-1 bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 rounded border border-amber-500/30 text-[10px] font-semibold"
                    >
                      Mark Resolved
                    </button>
                  )}
                  {def.status !== 'CLOSED' && (
                    <button
                      onClick={() => handleStatusChange(def.id, 'CLOSED')}
                      className="px-2.5 py-1 bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 rounded border border-emerald-500/30 text-[10px] font-semibold"
                    >
                      Close Defect
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="py-8 text-center text-xs text-slate-500">
            No defects currently reported for this project.
          </div>
        )}
      </div>
    </div>
  );
};
