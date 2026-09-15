'use client';

import React, { useState, useEffect } from 'react';
import { AutomationRule, orchestrationApi } from '@/lib/api/orchestration';
import { Sliders, Plus, ToggleLeft, ToggleRight, ShieldCheck, RefreshCw } from 'lucide-react';

export const AutomationRuleBuilder: React.FC = () => {
  const [rules, setRules] = useState<AutomationRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [ruleName, setRuleName] = useState('');
  const [description, setDescription] = useState('');
  const [triggerEvent, setTriggerEvent] = useState('lead.qualified');
  const [conditionJson, setConditionJson] = useState('{\n  "score_min": 80\n}');
  const [actionJson, setActionJson] = useState('{\n  "workflow_key": "lead_acquisition_workflow"\n}');
  const [requiresApproval, setRequiresApproval] = useState(true);

  const loadRules = async () => {
    try {
      setLoading(true);
      const data = await orchestrationApi.listAutomations();
      setRules(data);
    } catch (err) {
      console.error('Failed to load automation rules', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRules();
  }, []);

  const handleToggle = async (ruleId: string, currentEnabled: boolean) => {
    try {
      await orchestrationApi.toggleAutomation(ruleId, !currentEnabled);
      loadRules();
    } catch (err) {
      console.error('Failed to toggle rule', err);
    }
  };

  const handleCreate = async () => {
    try {
      let parsedCond = {};
      let parsedAction = {};
      try {
        parsedCond = JSON.parse(conditionJson);
        parsedAction = JSON.parse(actionJson);
      } catch (e) {
        alert('Invalid JSON in condition or action configuration.');
        return;
      }

      await orchestrationApi.createAutomation({
        name: ruleName,
        description,
        trigger_type: 'EVENT',
        trigger_config: { event_type: triggerEvent },
        condition_config: parsedCond,
        action_config: parsedAction,
        requires_human_approval: requiresApproval,
      });

      setShowModal(false);
      setRuleName('');
      setDescription('');
      loadRules();
    } catch (err) {
      console.error('Failed to create automation rule', err);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <Sliders className="w-4 h-4 text-cyan-400" /> Automation Rules Engine
          </h3>
          <p className="text-xs text-slate-400">Declarative WHEN / IF / THEN triggers coordinating cross-phase workflows</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold px-3.5 py-2 rounded-lg transition-colors flex items-center gap-1.5"
        >
          <Plus className="w-3.5 h-3.5" /> Create Rule
        </button>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden divide-y divide-slate-800">
        {loading ? (
          <div className="p-8 text-center text-slate-500 text-xs">Loading automation rules...</div>
        ) : rules.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-xs">No automation rules configured.</div>
        ) : (
          rules.map((r) => (
            <div key={r.id} className="p-4 hover:bg-slate-800/40 transition-colors flex items-center justify-between">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-slate-200">{r.name}</span>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                    {r.version}
                  </span>
                  {r.requires_human_approval && (
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center gap-1">
                      <ShieldCheck className="w-3 h-3" /> Human Gate
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-400">{r.description}</p>
                <div className="text-[11px] font-mono text-slate-500 flex items-center gap-3">
                  <span>WHEN: {r.trigger_config?.event_type || 'Custom Event'}</span>
                  <span>•</span>
                  <span>ACTION: {r.action_config?.workflow_key || 'Custom Action'}</span>
                </div>
              </div>

              <button
                onClick={() => handleToggle(r.id, r.enabled)}
                className={`p-2 rounded-lg transition-colors ${
                  r.enabled ? 'text-cyan-400 hover:text-cyan-300' : 'text-slate-500 hover:text-slate-400'
                }`}
              >
                {r.enabled ? <ToggleRight className="w-6 h-6" /> : <ToggleLeft className="w-6 h-6" />}
              </button>
            </div>
          ))
        )}
      </div>

      {/* Modal for Creating New Rule */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 w-full max-w-lg space-y-4">
            <h3 className="text-base font-semibold text-slate-100">Create Automation Rule</h3>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Rule Name</label>
              <input
                type="text"
                value={ruleName}
                onChange={(e) => setRuleName(e.target.value)}
                placeholder="e.g. Auto Start Research on High Score Lead"
                className="w-full bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg p-2.5 outline-none focus:border-cyan-500"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Description</label>
              <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Rule intent and purpose"
                className="w-full bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg p-2.5 outline-none focus:border-cyan-500"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-300 block mb-1">Trigger Event</label>
              <input
                type="text"
                value={triggerEvent}
                onChange={(e) => setTriggerEvent(e.target.value)}
                placeholder="e.g. lead.qualified"
                className="w-full bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg p-2.5 outline-none focus:border-cyan-500"
              />
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="approvalReq"
                checked={requiresApproval}
                onChange={(e) => setRequiresApproval(e.target.checked)}
                className="rounded bg-slate-950 border-slate-700 text-cyan-500"
              />
              <label htmlFor="approvalReq" className="text-xs text-slate-300">
                Requires Human Approval before sensitive dispatch
              </label>
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setShowModal(false)}
                className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold px-4 py-2 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleCreate}
                disabled={!ruleName}
                className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors"
              >
                Save Rule
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
