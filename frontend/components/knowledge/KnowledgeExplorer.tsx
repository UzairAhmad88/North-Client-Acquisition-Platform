'use client';

import React, { useState, useEffect } from 'react';
import { listKnowledgeItems, createKnowledgeItem, KnowledgeItem } from '@/lib/api/knowledge';
import {
  BookOpen,
  Plus,
  GitBranch,
  ShieldCheck,
  Clock,
  User,
  Hash,
  Layers,
  FileCode,
  X,
} from 'lucide-react';

export default function KnowledgeExplorerComponent() {
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDomain, setSelectedDomain] = useState<string>('ALL');
  const [activeItem, setActiveItem] = useState<KnowledgeItem | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Form states
  const [newCode, setNewCode] = useState('');
  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');
  const [newDomain, setNewDomain] = useState('TECHNICAL');
  const [newAuthority, setNewAuthority] = useState('OBSERVED');
  const [isAiGen, setIsAiGen] = useState(false);
  const [createError, setCreateError] = useState<string | null>(null);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const data = await listKnowledgeItems(selectedDomain === 'ALL' ? undefined : selectedDomain);
      setItems(data);
      if (data.length > 0 && !activeItem) {
        setActiveItem(data[0]);
      }
    } catch (err) {
      console.error('Failed to load knowledge items:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, [selectedDomain]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreateError(null);

    try {
      await createKnowledgeItem({
        knowledge_code: newCode.trim(),
        title: newTitle.trim(),
        content: newContent.trim(),
        domain: newDomain,
        authority: newAuthority,
        is_ai_generated: isAiGen,
      });
      setShowCreateModal(false);
      setNewCode('');
      setNewTitle('');
      setNewContent('');
      fetchItems();
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Creation failed';
      setCreateError(msg);
    }
  };

  const domains = ['ALL', 'TECHNICAL', 'SECURITY', 'AI', 'CLIENT', 'DECISIONS', 'GOVERNANCE', 'RELIABILITY'];

  return (
    <div className="space-y-6">
      {/* Action Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-5 rounded-xl border border-slate-200">
        <div className="flex items-center gap-2 overflow-x-auto pb-1 max-w-full">
          {domains.map((dom) => (
            <button
              key={dom}
              onClick={() => setSelectedDomain(dom)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                selectedDomain === dom
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {dom}
            </button>
          ))}
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 transition-colors shadow-sm"
        >
          <Plus className="w-4 h-4" />
          Add Governed Knowledge
        </button>
      </div>

      {/* Main Split View */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        {/* Left List Column */}
        <div className="md:col-span-5 space-y-3 max-h-[700px] overflow-y-auto pr-1">
          {loading ? (
            <div className="p-8 text-center text-slate-500 animate-pulse bg-white rounded-xl border border-slate-200">
              Loading canonical knowledge repository...
            </div>
          ) : items.length === 0 ? (
            <div className="p-8 text-center bg-white rounded-xl border border-slate-200 text-slate-500 text-sm">
              No items in this domain.
            </div>
          ) : (
            items.map((item) => (
              <div
                key={item.knowledge_code}
                onClick={() => setActiveItem(item)}
                className={`p-4 rounded-xl border transition-all cursor-pointer ${
                  activeItem?.knowledge_code === item.knowledge_code
                    ? 'bg-indigo-50/50 border-indigo-300 shadow-sm'
                    : 'bg-white border-slate-200 hover:border-slate-300'
                }`}
              >
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-mono font-bold text-indigo-600">{item.knowledge_code}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700">
                    {item.domain}
                  </span>
                </div>
                <h4 className="text-sm font-bold text-slate-900 line-clamp-1">{item.title}</h4>
                <p className="text-xs text-slate-500 line-clamp-2 mt-1">{item.content}</p>
                <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-100 text-[11px] text-slate-400">
                  <span>Auth: <strong>{item.authority}</strong></span>
                  <span>v{item.version}</span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Right Detail Pane */}
        <div className="md:col-span-7">
          {activeItem ? (
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6 sticky top-6">
              <div>
                <div className="flex items-center gap-2 flex-wrap mb-2">
                  <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-indigo-50 text-indigo-700">
                    {activeItem.knowledge_code}
                  </span>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                    {activeItem.domain}
                  </span>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">
                    {activeItem.authority}
                  </span>
                  <span className="text-xs font-medium text-slate-400 flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    v{activeItem.version} ({activeItem.freshness_status})
                  </span>
                </div>
                <h3 className="text-xl font-extrabold text-slate-900">{activeItem.title}</h3>
              </div>

              <div>
                <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                  Authoritative Content
                </div>
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 text-sm text-slate-800 leading-relaxed whitespace-pre-wrap font-sans">
                  {activeItem.content}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-xs bg-slate-50 p-4 rounded-xl border border-slate-100">
                <div>
                  <span className="text-slate-400 block mb-0.5">Provenance Origin:</span>
                  <span className="font-semibold text-slate-800">{activeItem.provenance}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5">Classification Scope:</span>
                  <span className="font-semibold text-slate-800">{activeItem.classification}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5">Owner Principal:</span>
                  <span className="font-semibold text-slate-800">{activeItem.owner_id}</span>
                </div>
                <div>
                  <span className="text-slate-400 block mb-0.5">SHA-256 Digest:</span>
                  <span className="font-mono text-[10px] text-slate-600 truncate block">
                    {activeItem.content_hash || 'Verified'}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white p-12 text-center rounded-2xl border border-slate-200 text-slate-400 text-sm">
              Select an item on the left to inspect canonical details and version history.
            </div>
          )}
        </div>
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-xl border border-slate-200 space-y-4 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-base font-bold text-slate-900">Add Governed Knowledge Item</h3>
              <button onClick={() => setShowCreateModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            {createError && (
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-rose-700 text-xs font-medium">
                {createError}
              </div>
            )}

            <form onSubmit={handleCreate} className="space-y-3 text-xs">
              <div>
                <label className="font-semibold text-slate-700 block mb-1">Knowledge Code</label>
                <input
                  type="text"
                  required
                  placeholder="KNW-TECH-POSTGRES-001"
                  value={newCode}
                  onChange={(e) => setNewCode(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500 font-mono"
                />
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Title</label>
                <input
                  type="text"
                  required
                  placeholder="Multi-Tenant Database Partitioning Policy"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Domain</label>
                  <select
                    value={newDomain}
                    onChange={(e) => setNewDomain(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  >
                    <option value="TECHNICAL">TECHNICAL</option>
                    <option value="SECURITY">SECURITY</option>
                    <option value="AI">AI</option>
                    <option value="CLIENT">CLIENT</option>
                    <option value="DECISIONS">DECISIONS</option>
                    <option value="GOVERNANCE">GOVERNANCE</option>
                    <option value="RELIABILITY">RELIABILITY</option>
                  </select>
                </div>

                <div>
                  <label className="font-semibold text-slate-700 block mb-1">Authority Level</label>
                  <select
                    value={newAuthority}
                    onChange={(e) => setNewAuthority(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  >
                    <option value="AUTHORITATIVE">AUTHORITATIVE</option>
                    <option value="VERIFIED">VERIFIED</option>
                    <option value="CONFIRMED">CONFIRMED</option>
                    <option value="OBSERVED">OBSERVED</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="font-semibold text-slate-700 block mb-1">Authoritative Content</label>
                <textarea
                  required
                  rows={4}
                  placeholder="Enter canonical knowledge description, procedure, or policy details..."
                  value={newContent}
                  onChange={(e) => setNewContent(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              <div className="flex items-center gap-2 pt-2">
                <input
                  type="checkbox"
                  id="aiGen"
                  checked={isAiGen}
                  onChange={(e) => setIsAiGen(e.target.checked)}
                  className="rounded text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="aiGen" className="text-slate-600 font-medium">
                  Is AI Inferred (Rule 1-3: Prohibits unverified authoritative status)
                </label>
              </div>

              <div className="flex justify-end gap-2 pt-4 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 text-slate-600 hover:bg-slate-100 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow-sm"
                >
                  Save Knowledge Item
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
