'use client';

import React, { useState } from 'react';
import { ConfigItem, administrationApi } from '@/lib/api/administration';

interface ConfigurationManagerViewProps {
  configs: ConfigItem[];
  onRefresh: () => void;
}

export function ConfigurationManagerView({ configs, onRefresh }: ConfigurationManagerViewProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [editingConfig, setEditingConfig] = useState<ConfigItem | null>(null);
  const [newValue, setNewValue] = useState<string>('');
  const [changeReason, setChangeReason] = useState<string>('');
  const [riskLevel, setRiskLevel] = useState<string>('MEDIUM');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [rollbackConfig, setRollbackConfig] = useState<ConfigItem | null>(null);
  const [targetVersion, setTargetVersion] = useState<number>(1);
  const [rollbackReason, setRollbackReason] = useState<string>('');

  const categories = ['ALL', ...Array.from(new Set(configs.map((c) => c.category)))];

  const filteredConfigs =
    selectedCategory === 'ALL'
      ? configs
      : configs.filter((c) => c.category.toLowerCase() === selectedCategory.toLowerCase());

  const handleOpenEdit = (config: ConfigItem) => {
    setEditingConfig(config);
    setNewValue(
      typeof config.current_value === 'object'
        ? JSON.stringify(config.current_value, null, 2)
        : String(config.current_value)
    );
    setChangeReason('');
    setRiskLevel('MEDIUM');
  };

  const handleSubmitChange = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingConfig) return;
    setIsSubmitting(true);
    try {
      let parsedValue: any = newValue;
      if (editingConfig.config_type === 'INTEGER') parsedValue = parseInt(newValue, 10);
      else if (editingConfig.config_type === 'DECIMAL' || editingConfig.config_type === 'FLOAT')
        parsedValue = parseFloat(newValue);
      else if (editingConfig.config_type === 'BOOLEAN') parsedValue = newValue.toLowerCase() === 'true';
      else if (['JSON', 'LIST', 'MAP', 'ARRAY'].includes(editingConfig.config_type))
        parsedValue = JSON.parse(newValue);

      await administrationApi.submitChangeRequest({
        key: editingConfig.key,
        new_value: parsedValue,
        reason: changeReason || 'Configuration update via Admin Control Center',
        risk_level: riskLevel,
      });
      setEditingConfig(null);
      onRefresh();
    } catch (err: any) {
      alert(`Failed to submit change request: ${err.message || err}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleExecuteRollback = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!rollbackConfig) return;
    setIsSubmitting(true);
    try {
      await administrationApi.rollbackConfig({
        key: rollbackConfig.key,
        target_version: targetVersion,
        reason: rollbackReason || `Rollback to version ${targetVersion}`,
      });
      setRollbackConfig(null);
      onRefresh();
    } catch (err: any) {
      alert(`Rollback failed: ${err.message || err}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Filters and Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-slate-900/50 p-4 rounded-xl border border-slate-800 backdrop-blur">
        <div>
          <h3 className="text-lg font-semibold text-white">Central Configuration Registry</h3>
          <p className="text-xs text-slate-400">
            Immutable version-controlled runtime parameters with strict schema validation
          </p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-400">Category:</label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="bg-slate-800 text-xs text-slate-200 border border-slate-700 rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Configuration Grid */}
      <div className="grid grid-cols-1 gap-4">
        {filteredConfigs.map((cfg) => (
          <div
            key={cfg.key}
            className="bg-slate-900/40 border border-slate-800/80 rounded-xl p-5 hover:border-slate-700 transition"
          >
            <div className="flex flex-col md:flex-row justify-between md:items-center gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2.5">
                  <span className="text-sm font-bold text-white tracking-wide">{cfg.display_name}</span>
                  <code className="text-xs font-mono text-indigo-400 bg-indigo-950/40 px-2 py-0.5 rounded border border-indigo-800/40">
                    {cfg.key}
                  </code>
                  <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                    v{cfg.version}
                  </span>
                  {cfg.sensitive && (
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-rose-950/60 text-rose-300 border border-rose-800/50">
                      SENSITIVE
                    </span>
                  )}
                  {!cfg.mutable && (
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-amber-950/60 text-amber-300 border border-amber-800/50">
                      IMMUTABLE
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-400">{cfg.description}</p>
                <div className="flex items-center gap-3 text-[11px] text-slate-500 pt-1">
                  <span>Type: <strong className="text-slate-400">{cfg.config_type}</strong></span>
                  <span>•</span>
                  <span>Scope: <strong className="text-slate-400">{cfg.scope}</strong></span>
                  <span>•</span>
                  <span>Category: <strong className="text-slate-400">{cfg.category}</strong></span>
                </div>
              </div>

              {/* Current Value Preview and Actions */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
                <div className="bg-slate-950/80 border border-slate-800 rounded-lg px-3 py-2 text-right min-w-[160px]">
                  <span className="text-[10px] text-slate-500 block uppercase font-medium">Current Value</span>
                  <span className="text-xs font-mono text-emerald-400 font-semibold truncate block max-w-[200px]">
                    {typeof cfg.current_value === 'object'
                      ? JSON.stringify(cfg.current_value)
                      : String(cfg.current_value)}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleOpenEdit(cfg)}
                    disabled={!cfg.mutable}
                    className={`text-xs px-3 py-2 rounded-lg font-medium transition ${
                      cfg.mutable
                        ? 'bg-indigo-600 hover:bg-indigo-500 text-white'
                        : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                    }`}
                  >
                    Propose Change
                  </button>
                  <button
                    onClick={() => {
                      setRollbackConfig(cfg);
                      setTargetVersion(Math.max(1, cfg.version - 1));
                    }}
                    className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-2 rounded-lg font-medium border border-slate-700 transition"
                  >
                    Rollback
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Edit/Change Modal */}
      {editingConfig && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <h4 className="text-base font-bold text-white">Propose Configuration Change</h4>
            <p className="text-xs text-slate-400">
              Changes to <code className="text-indigo-400">{editingConfig.key}</code> undergo strict validation and require administrative approval.
            </p>

            <form onSubmit={handleSubmitChange} className="space-y-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">New Value ({editingConfig.config_type})</label>
                <textarea
                  rows={3}
                  value={newValue}
                  onChange={(e) => setNewValue(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-100 font-mono focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Risk Level</label>
                  <select
                    value={riskLevel}
                    onChange={(e) => setRiskLevel(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                  >
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                    <option value="CRITICAL">CRITICAL</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Validation Constraint</label>
                  <input
                    type="text"
                    disabled
                    value={JSON.stringify(editingConfig.validation_rules || {})}
                    className="w-full bg-slate-950/50 border border-slate-800 rounded-lg p-2 text-xs text-slate-500 font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Justification / Reason</label>
                <input
                  type="text"
                  placeholder="Reason for change..."
                  value={changeReason}
                  onChange={(e) => setChangeReason(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                  required
                />
              </div>

              <div className="flex justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setEditingConfig(null)}
                  className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-medium"
                >
                  {isSubmitting ? 'Submitting...' : 'Submit Change Proposal'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Rollback Modal */}
      {rollbackConfig && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <h4 className="text-base font-bold text-white">Emergency Configuration Rollback</h4>
            <p className="text-xs text-slate-400">
              Instantly revert <code className="text-indigo-400">{rollbackConfig.key}</code> to a verified historical snapshot.
            </p>

            <form onSubmit={handleExecuteRollback} className="space-y-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Target Version</label>
                <input
                  type="number"
                  min={1}
                  max={rollbackConfig.version - 1}
                  value={targetVersion}
                  onChange={(e) => setTargetVersion(parseInt(e.target.value, 10))}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Rollback Reason</label>
                <input
                  type="text"
                  placeholder="e.g., Mitigate production incident"
                  value={rollbackReason}
                  onChange={(e) => setRollbackReason(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs text-slate-200"
                  required
                />
              </div>

              <div className="flex justify-end gap-3 pt-3">
                <button
                  type="button"
                  onClick={() => setRollbackConfig(null)}
                  className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-xs font-medium"
                >
                  {isSubmitting ? 'Rolling back...' : 'Execute Immediate Rollback'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
