"use client";

import React, { useState } from "react";
import { PromptItem, governanceApi } from "@/lib/api/governance";
import { FileCode, Shield, Check, Plus, Hash, Tag } from "lucide-react";

interface PromptRegistryManagerProps {
  prompts: PromptItem[];
  onRefresh: () => void;
}

export const PromptRegistryManager: React.FC<PromptRegistryManagerProps> = ({ prompts, onRefresh }) => {
  const [selectedPrompt, setSelectedPrompt] = useState<PromptItem | null>(prompts.length > 0 ? prompts[0] : null);
  const [showModal, setShowModal] = useState(false);
  const [newKey, setNewKey] = useState("");
  const [newName, setNewName] = useState("");
  const [newAgent, setNewAgent] = useState("research_agent");
  const [newPurpose, setNewPurpose] = useState("");
  const [newContent, setNewContent] = useState("");
  const [saving, setSaving] = useState(false);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await governanceApi.registerPrompt({
        prompt_key: newKey,
        name: newName,
        agent_target: newAgent,
        purpose: newPurpose,
        content: newContent,
      });
      setShowModal(false);
      onRefresh();
    } catch (err) {
      console.error("Failed to register prompt:", err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-zinc-100">Centralized Production Prompt Registry</h3>
          <p className="text-xs text-zinc-400 mt-1">
            Versioned, content-hashed, and tested prompts linked to explicit agent targets.
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white transition"
        >
          <Plus className="w-4 h-4" /> Register New Prompt
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left List */}
        <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-5 space-y-3">
          {prompts.map((p) => (
            <button
              key={p.id}
              onClick={() => setSelectedPrompt(p)}
              className={`w-full text-left p-3 rounded-lg border transition ${
                selectedPrompt?.id === p.id
                  ? "bg-indigo-950/40 border-indigo-500/50 text-indigo-200"
                  : "bg-zinc-950/60 border-zinc-800/80 text-zinc-400 hover:border-zinc-700"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-xs text-zinc-200">{p.name}</span>
                <span className="px-1.5 py-0.5 rounded text-[10px] bg-zinc-800 text-zinc-300 font-mono">
                  {p.current_version}
                </span>
              </div>
              <div className="text-[11px] text-zinc-500 mt-1 truncate">{p.purpose}</div>
              <div className="text-[10px] text-indigo-400 mt-2 flex items-center gap-1">
                <Tag className="w-3 h-3" /> {p.agent_target}
              </div>
            </button>
          ))}
        </div>

        {/* Right Detail */}
        <div className="lg:col-span-2 bg-zinc-900/80 border border-zinc-800 rounded-xl p-6 space-y-4">
          {selectedPrompt ? (
            <>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-base font-bold text-zinc-100">{selectedPrompt.name}</h3>
                  <div className="text-xs text-zinc-500 font-mono mt-0.5">{selectedPrompt.prompt_key}</div>
                </div>
                <span className="px-2 py-0.5 rounded text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                  {selectedPrompt.current_version} Active
                </span>
              </div>

              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-2">
                  Prompt Purpose & Scope
                </h4>
                <p className="text-xs text-zinc-300 bg-zinc-950 p-3 rounded-lg border border-zinc-850">
                  {selectedPrompt.purpose}
                </p>
              </div>

              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-zinc-400 mb-2 flex items-center gap-1">
                  <Hash className="w-3.5 h-3.5 text-indigo-400" /> Version History & Integrity Hashes
                </h4>
                <div className="space-y-2">
                  {selectedPrompt.versions && selectedPrompt.versions.length > 0 ? (
                    selectedPrompt.versions.map((v: any) => (
                      <div key={v.id} className="bg-zinc-950 border border-zinc-850 p-3 rounded-lg text-xs space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="font-semibold text-zinc-200">{v.version}</span>
                          <span className="text-[10px] text-zinc-500 font-mono">SHA-256: {v.content_hash.slice(0, 16)}...</span>
                        </div>
                        <pre className="text-zinc-400 text-[11px] font-mono whitespace-pre-wrap bg-zinc-900 p-2 rounded mt-2">
                          {v.content}
                        </pre>
                      </div>
                    ))
                  ) : (
                    <div className="text-xs text-zinc-500">Initial release version registered.</div>
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="p-12 text-center text-zinc-500">Select a prompt to view details.</div>
          )}
        </div>
      </div>

      {/* Creation Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleCreate} className="bg-zinc-900 border border-zinc-800 rounded-xl max-w-lg w-full p-6 space-y-4">
            <h3 className="font-bold text-zinc-100 text-sm">Register Production Prompt</h3>
            <div>
              <label className="text-xs text-zinc-400 block mb-1">Prompt Key</label>
              <input
                required
                value={newKey}
                onChange={(e) => setNewKey(e.target.value)}
                placeholder="e.g. research_analysis_v1"
                className="w-full px-3 py-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200"
              />
            </div>
            <div>
              <label className="text-xs text-zinc-400 block mb-1">Display Name</label>
              <input
                required
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder="e.g. Research In-depth Analysis"
                className="w-full px-3 py-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200"
              />
            </div>
            <div>
              <label className="text-xs text-zinc-400 block mb-1">Target Agent</label>
              <select
                value={newAgent}
                onChange={(e) => setNewAgent(e.target.value)}
                className="w-full px-3 py-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200"
              >
                <option value="research_agent">Research Agent</option>
                <option value="audit_agent">Audit Agent</option>
                <option value="qualification_agent">Qualification Agent</option>
                <option value="personalization_agent">Personalization Agent</option>
                <option value="decision_intelligence_agent">Decision Intelligence Agent</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-zinc-400 block mb-1">Purpose Description</label>
              <input
                required
                value={newPurpose}
                onChange={(e) => setNewPurpose(e.target.value)}
                placeholder="e.g. Extract digital footprint and competitive signals"
                className="w-full px-3 py-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200"
              />
            </div>
            <div>
              <label className="text-xs text-zinc-400 block mb-1">Prompt Template Content</label>
              <textarea
                required
                rows={4}
                value={newContent}
                onChange={(e) => setNewContent(e.target.value)}
                placeholder="You are an expert AI research agent..."
                className="w-full px-3 py-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-xs text-zinc-200 font-mono"
              />
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setShowModal(false)}
                className="px-3 py-1.5 rounded-lg text-xs text-zinc-400 hover:text-zinc-200"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={saving}
                className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white"
              >
                {saving ? "Registering..." : "Save Prompt"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default PromptRegistryManager;
