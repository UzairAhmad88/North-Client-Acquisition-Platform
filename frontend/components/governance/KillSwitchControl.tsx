"use client";

import React, { useState } from "react";
import { KillSwitchEvent, governanceApi } from "@/lib/api/governance";
import { AlertOctagon, ShieldAlert, Power, Lock, CheckCircle2 } from "lucide-react";

interface KillSwitchControlProps {
  activeSwitches: KillSwitchEvent[];
  onRefresh: () => void;
}

export const KillSwitchControl: React.FC<KillSwitchControlProps> = ({ activeSwitches, onRefresh }) => {
  const [level, setLevel] = useState<string>("GLOBAL_AI_OFF");
  const [targetKey, setTargetKey] = useState<string>("GLOBAL");
  const [reason, setReason] = useState<string>("");
  const [confirmed, setConfirmed] = useState<boolean>(false);
  const [submitting, setSubmitting] = useState<boolean>(false);

  const isGlobalActive = activeSwitches.some((s) => s.level === "GLOBAL_AI_OFF" && s.is_active);

  const handleToggle = async (isActivating: boolean) => {
    if (isActivating && (!confirmed || !reason)) {
      alert("Please provide an authoritative operational reason and check the confirmation box.");
      return;
    }
    setSubmitting(true);
    try {
      await governanceApi.triggerKillSwitch({
        level,
        target_key: targetKey,
        is_active: isActivating,
        activated_by: "system_admin",
        reason: reason || "Emergency deactivation of circuit breaker by authorized operator.",
      });
      setReason("");
      setConfirmed(false);
      onRefresh();
    } catch (err) {
      console.error("Kill switch action failed:", err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Emergency Status Banner */}
      <div
        className={`rounded-xl p-6 border ${
          isGlobalActive
            ? "bg-rose-950/40 border-rose-800 text-rose-200"
            : "bg-zinc-900/80 border-zinc-800 text-zinc-300"
        }`}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <ShieldAlert className={`w-8 h-8 ${isGlobalActive ? "text-rose-400" : "text-emerald-400"}`} />
            <div>
              <h3 className="text-lg font-bold text-zinc-100">
                AI Emergency Kill Switch &amp; Safety Circuit Breaker
              </h3>
              <p className="text-xs text-zinc-400 mt-0.5">
                {isGlobalActive
                  ? "CRITICAL: Global emergency kill-switch is ACTIVE. All AI executions are completely halted."
                  : "Status: All AI agent systems operational. Emergency isolation available."}
              </p>
            </div>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-xs font-bold ${
              isGlobalActive ? "bg-rose-500/20 text-rose-300 border border-rose-500/30" : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
            }`}
          >
            {isGlobalActive ? "GLOBAL EMERGENCY SHUTDOWN" : "SYSTEM OPERATIONAL"}
          </span>
        </div>
      </div>

      {/* Control Panel Form */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6 space-y-4">
        <h4 className="font-bold text-zinc-100 text-sm flex items-center gap-2">
          <Lock className="w-4 h-4 text-indigo-400" />
          Authorize Circuit Breaker Action
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs text-zinc-400 block mb-1">Shutdown Level</label>
            <select
              value={level}
              onChange={(e) => {
                setLevel(e.target.value);
                if (e.target.value === "GLOBAL_AI_OFF") setTargetKey("GLOBAL");
              }}
              className="w-full px-3 py-2 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200"
            >
              <option value="GLOBAL_AI_OFF">Global AI Off (All Agents &amp; Models)</option>
              <option value="AGENT_OFF">Specific Agent Off</option>
              <option value="MODEL_OFF">Specific Model Off</option>
              <option value="TOOL_OFF">Specific Tool Off</option>
            </select>
          </div>

          <div>
            <label className="text-xs text-zinc-400 block mb-1">Target Key</label>
            <input
              disabled={level === "GLOBAL_AI_OFF"}
              value={targetKey}
              onChange={(e) => setTargetKey(e.target.value)}
              placeholder="e.g. research_agent, gpt-4o, search_web"
              className="w-full px-3 py-2 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200 disabled:opacity-50"
            />
          </div>
        </div>

        <div>
          <label className="text-xs text-zinc-400 block mb-1">Authoritative Incident / Audit Reason</label>
          <input
            required
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="e.g. Unusual hallucination spike detected during research workflow"
            className="w-full px-3 py-2 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200"
          />
        </div>

        <div className="flex items-center gap-2 pt-2">
          <input
            type="checkbox"
            id="kill-confirm"
            checked={confirmed}
            onChange={(e) => setConfirmed(e.target.checked)}
            className="rounded border-zinc-700 text-rose-600 focus:ring-rose-500"
          />
          <label htmlFor="kill-confirm" className="text-xs text-zinc-400">
            I confirm that this action will immediately isolate AI workflows and log an audit event.
          </label>
        </div>

        <div className="flex gap-3 pt-3">
          <button
            onClick={() => handleToggle(true)}
            disabled={submitting || !confirmed || !reason}
            className="flex items-center gap-2 px-5 py-2.5 rounded-lg text-xs font-bold bg-rose-600 hover:bg-rose-500 text-white transition disabled:opacity-40"
          >
            <Power className="w-4 h-4" /> Trigger Emergency Isolation
          </button>

          {isGlobalActive && (
            <button
              onClick={() => handleToggle(false)}
              disabled={submitting}
              className="flex items-center gap-2 px-5 py-2.5 rounded-lg text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition"
            >
              <CheckCircle2 className="w-4 h-4" /> Restore AI Operations
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default KillSwitchControl;
