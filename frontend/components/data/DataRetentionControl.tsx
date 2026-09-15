'use client';

import React, { useState, useEffect } from 'react';
import {
  Lock,
  Unlock,
  ShieldAlert,
  Clock,
  Plus,
  Trash2,
  CheckCircle2,
  AlertTriangle,
  FileSpreadsheet,
} from 'lucide-react';
import { dataApi, DataRetentionPolicy, LegalHold } from '@/lib/api/data';

export default function DataRetentionControl() {
  const [policies, setPolicies] = useState<DataRetentionPolicy[]>([]);
  const [holds, setHolds] = useState<LegalHold[]>([]);
  const [loading, setLoading] = useState(true);
  const [showHoldModal, setShowHoldModal] = useState(false);
  const [showPolicyModal, setShowPolicyModal] = useState(false);

  // Safety deletion check
  const [checkType, setCheckType] = useState('CONTRACT');
  const [checkId, setCheckId] = useState('CTR-9901');
  const [checkResult, setCheckResult] = useState<{
    can_delete: boolean;
    reason: string;
    message: string;
  } | null>(null);

  // Form states
  const [holdForm, setHoldForm] = useState({
    case_reference: 'CASE-2026-004',
    reason: 'Regulatory compliance investigation',
    entity_type: 'CONTRACT',
    entity_id: 'CTR-9901',
    notes: 'Preserve all revisions and communications',
  });

  const [policyForm, setPolicyForm] = useState({
    domain: 'AUDIT',
    entity_type: 'AUDIT_LOG',
    retention_period_days: 365,
    action_on_expiry: 'ARCHIVE',
  });

  const loadData = async () => {
    try {
      setLoading(true);
      const [policiesData, holdsData] = await Promise.all([
        dataApi.listRetentionPolicies(),
        dataApi.listLegalHolds(false),
      ]);
      setPolicies(policiesData || []);
      setHolds(holdsData || []);
    } catch (err) {
      console.error('Failed to load retention data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handlePlaceHold = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dataApi.placeLegalHold(holdForm);
      setShowHoldModal(false);
      loadData();
    } catch (err) {
      console.error('Failed to place legal hold', err);
    }
  };

  const handleReleaseHold = async (holdId: string) => {
    try {
      await dataApi.releaseLegalHold(holdId, 'Case closed by compliance team');
      loadData();
    } catch (err) {
      console.error('Failed to release legal hold', err);
    }
  };

  const handleCreatePolicy = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dataApi.createRetentionPolicy(policyForm as any);
      setShowPolicyModal(false);
      loadData();
    } catch (err) {
      console.error('Failed to create retention policy', err);
    }
  };

  const handleCheckDeletionSafety = async () => {
    try {
      const res = await dataApi.checkCanDelete(checkType, checkId);
      setCheckResult(res);
    } catch (err) {
      console.error('Failed to check deletion status', err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Lock className="w-5 h-5 text-rose-400" />
            Data Retention, Lifecycle Governance & Legal Holds
          </h2>
          <p className="text-sm text-slate-400">
            Enforce compliant data retention schedules and place binding legal holds preventing record deletion.
          </p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => setShowPolicyModal(true)}
            className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700"
          >
            + Add Retention Policy
          </button>
          <button
            onClick={() => setShowHoldModal(true)}
            className="px-3.5 py-2 bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold rounded-xl shadow-lg"
          >
            + Place Legal Hold
          </button>
        </div>
      </div>

      {/* Safety Deletion Pre-flight Checker */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <h3 className="text-base font-bold text-white mb-2 flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-rose-400" />
          Deletion Pre-Flight Safety Verification
        </h3>
        <p className="text-xs text-slate-400 mb-4">
          Test whether an entity is protected from deletion by legal holds or active retention locks.
        </p>

        <div className="flex flex-col sm:flex-row gap-3">
          <select
            value={checkType}
            onChange={(e) => setCheckType(e.target.value)}
            className="px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-xs text-white"
          >
            <option value="CONTRACT">CONTRACT</option>
            <option value="PROPOSAL">PROPOSAL</option>
            <option value="ESTIMATE">ESTIMATE</option>
            <option value="LEAD">LEAD</option>
          </select>
          <input
            type="text"
            value={checkId}
            onChange={(e) => setCheckId(e.target.value)}
            placeholder="Entity ID"
            className="flex-1 px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-xs text-white font-mono"
          />
          <button
            onClick={handleCheckDeletionSafety}
            className="px-4 py-2 bg-rose-600/80 hover:bg-rose-600 text-white text-xs font-semibold rounded-lg"
          >
            Check Safe Deletion
          </button>
        </div>

        {checkResult && (
          <div
            className={`mt-4 p-3.5 rounded-xl border flex items-center gap-3 text-xs ${
              checkResult.can_delete
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
            }`}
          >
            {checkResult.can_delete ? (
              <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-rose-400 flex-shrink-0" />
            )}
            <div>
              <strong className="block font-bold">
                {checkResult.can_delete ? 'DELETION PERMITTED' : 'DELETION BLOCKED'}
              </strong>
              <span>{checkResult.message}</span>
            </div>
          </div>
        )}
      </div>

      {/* Two Column Layout: Active Legal Holds & Policies */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Legal Holds */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Lock className="w-4 h-4 text-rose-400" />
              Active Legal Holds ({holds.filter((h) => h.active).length})
            </h3>
          </div>

          {holds.length === 0 ? (
            <div className="p-6 bg-slate-950/50 rounded-xl text-center text-slate-500 text-xs">
              No legal holds currently active.
            </div>
          ) : (
            <div className="space-y-3">
              {holds.map((hold) => (
                <div
                  key={hold.id}
                  className={`p-4 rounded-xl border space-y-2 ${
                    hold.active
                      ? 'bg-rose-500/5 border-rose-500/30'
                      : 'bg-slate-950 border-slate-800 opacity-60'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-bold text-white">
                      {hold.case_reference}
                    </span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded font-bold ${
                        hold.active
                          ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {hold.active ? 'ACTIVE LOCK' : 'RELEASED'}
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 font-medium">{hold.reason}</p>
                  <div className="text-[11px] text-slate-400 flex justify-between">
                    <span>Target: {hold.entity_type} ({hold.entity_id})</span>
                    <span>Placed: {new Date(hold.placed_at).toLocaleDateString()}</span>
                  </div>

                  {hold.active && (
                    <div className="pt-2 border-t border-rose-500/20 flex justify-end">
                      <button
                        onClick={() => handleReleaseHold(hold.id)}
                        className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 flex items-center gap-1"
                      >
                        <Unlock className="w-3 h-3 text-emerald-400" /> Release Hold
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Retention Policies */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-indigo-400" />
              Retention Schedules ({policies.length})
            </h3>
          </div>

          <div className="space-y-3">
            {policies.map((p) => (
              <div
                key={p.id}
                className="p-3.5 bg-slate-950 border border-slate-800 rounded-xl flex items-center justify-between"
              >
                <div>
                  <span className="text-xs font-bold text-white block">
                    {p.domain} • {p.entity_type}
                  </span>
                  <span className="text-[11px] text-slate-400">
                    Retain for {p.retention_period_days} days &rarr; {p.action_on_expiry}
                  </span>
                </div>

                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                  ENFORCING
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Place Legal Hold Modal */}
      {showHoldModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-4">Place Binding Legal Hold</h3>

            <form onSubmit={handlePlaceHold} className="space-y-4 text-sm">
              <div>
                <label className="block text-slate-300 mb-1">Case Reference</label>
                <input
                  type="text"
                  required
                  value={holdForm.case_reference}
                  onChange={(e) => setHoldForm({ ...holdForm, case_reference: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white font-mono"
                />
              </div>

              <div>
                <label className="block text-slate-300 mb-1">Reason for Hold</label>
                <input
                  type="text"
                  required
                  value={holdForm.reason}
                  onChange={(e) => setHoldForm({ ...holdForm, reason: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 mb-1">Entity Type</label>
                  <select
                    value={holdForm.entity_type}
                    onChange={(e) => setHoldForm({ ...holdForm, entity_type: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  >
                    <option value="CONTRACT">CONTRACT</option>
                    <option value="PROPOSAL">PROPOSAL</option>
                    <option value="ESTIMATE">ESTIMATE</option>
                    <option value="*">* (All Entities in Scope)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 mb-1">Entity ID</label>
                  <input
                    type="text"
                    required
                    value={holdForm.entity_id}
                    onChange={(e) => setHoldForm({ ...holdForm, entity_id: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white font-mono"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowHoldModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white font-medium rounded-xl"
                >
                  Confirm Legal Hold
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Retention Policy Modal */}
      {showPolicyModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-4">Define Retention Policy</h3>

            <form onSubmit={handleCreatePolicy} className="space-y-4 text-sm">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 mb-1">Domain</label>
                  <input
                    type="text"
                    required
                    value={policyForm.domain}
                    onChange={(e) => setPolicyForm({ ...policyForm, domain: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 mb-1">Entity Type</label>
                  <input
                    type="text"
                    required
                    value={policyForm.entity_type}
                    onChange={(e) => setPolicyForm({ ...policyForm, entity_type: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 mb-1">Period (Days)</label>
                  <input
                    type="number"
                    required
                    value={policyForm.retention_period_days}
                    onChange={(e) =>
                      setPolicyForm({ ...policyForm, retention_period_days: Number(e.target.value) })
                    }
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 mb-1">Expiry Action</label>
                  <select
                    value={policyForm.action_on_expiry}
                    onChange={(e) =>
                      setPolicyForm({ ...policyForm, action_on_expiry: e.target.value })
                    }
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  >
                    <option value="ARCHIVE">ARCHIVE</option>
                    <option value="DELETE">PURGE / DELETE</option>
                    <option value="ANONYMIZE">ANONYMIZE</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowPolicyModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-xl"
                >
                  Save Policy
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
