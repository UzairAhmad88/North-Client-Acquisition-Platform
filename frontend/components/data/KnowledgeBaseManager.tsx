'use client';

import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  CheckCircle,
  Search,
  Sparkles,
  Plus,
  ArrowUpRight,
  ShieldCheck,
  Tag,
  Clock,
  Layers,
  Bot,
} from 'lucide-react';
import { dataApi, KnowledgeItem, KnowledgeRetrievalResponse } from '@/lib/api/data';

export default function KnowledgeBaseManager() {
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Context Retrieval Simulator
  const [retrievalQuery, setRetrievalQuery] = useState('pricing and estimation guidelines');
  const [retrievalResults, setRetrievalResults] = useState<KnowledgeRetrievalResponse | null>(null);
  const [retrieving, setRetrieving] = useState(false);

  // Form State
  const [newItem, setNewItem] = useState({
    title: '',
    topic: 'Sales Estimation',
    domain: 'ESTIMATION',
    content: '',
    authority_level: 'VERIFIED_DATA',
    lifecycle_state: 'VERIFIED',
    classification: 'INTERNAL',
  });

  const loadItems = async () => {
    try {
      setLoading(true);
      const data = await dataApi.listKnowledgeItems();
      setItems(data || []);
    } catch (err) {
      console.error('Failed to load knowledge items', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadItems();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dataApi.createKnowledgeItem(newItem as any);
      setShowCreateModal(false);
      setNewItem({
        title: '',
        topic: 'Sales Estimation',
        domain: 'ESTIMATION',
        content: '',
        authority_level: 'VERIFIED_DATA',
        lifecycle_state: 'VERIFIED',
        classification: 'INTERNAL',
      });
      loadItems();
    } catch (err) {
      console.error('Failed to create knowledge item', err);
    }
  };

  const handlePromote = async (id: string, targetState: string) => {
    try {
      await dataApi.promoteKnowledgeItem(id, targetState, 'Manual verification in UI');
      loadItems();
    } catch (err) {
      console.error('Failed to promote knowledge item', err);
    }
  };

  const handleSimulateContextRetrieval = async () => {
    try {
      setRetrieving(true);
      const res = await dataApi.retrieveKnowledgeContext(retrievalQuery);
      setRetrievalResults(res);
    } catch (err) {
      console.error('Failed to retrieve knowledge context', err);
    } finally {
      setRetrieving(false);
    }
  };

  const filteredItems = items.filter((item) => {
    const matchesSearch =
      item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.topic.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.content.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDomain = selectedDomain === 'all' || item.domain === selectedDomain;
    return matchesSearch && matchesDomain;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-amber-400" />
            Curated Knowledge Base & AI Semantic Architecture
          </h2>
          <p className="text-sm text-slate-400">
            Lifecycle promotion from ingested facts to canonical knowledge with strict clearance boundaries.
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="inline-flex items-center px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white text-sm font-medium rounded-xl shadow-lg transition-all"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Knowledge Item
        </button>
      </div>

      {/* AI Context Retrieval Simulator Sandbox */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Bot className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-bold text-white">AI Context Retrieval Simulator</h3>
          </div>
          <span className="text-xs text-slate-400">Authorized Clearance Filtering</span>
        </div>

        <div className="flex gap-3 mb-4">
          <input
            type="text"
            value={retrievalQuery}
            onChange={(e) => setRetrievalQuery(e.target.value)}
            placeholder="Enter query for LLM prompt context injection..."
            className="flex-1 px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-sm text-white focus:outline-none focus:border-amber-500"
          />
          <button
            onClick={handleSimulateContextRetrieval}
            disabled={retrieving}
            className="px-4 py-2 bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-white text-xs font-semibold rounded-xl shadow transition-all flex items-center gap-1.5"
          >
            <Sparkles className="w-3.5 h-3.5" />
            {retrieving ? 'Retrieving...' : 'Retrieve Context'}
          </button>
        </div>

        {retrievalResults && (
          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-2">
              <span>Matches: <strong className="text-white">{retrievalResults.results_count}</strong></span>
              <span>Retrieved: {new Date(retrievalResults.retrieved_at).toLocaleTimeString()}</span>
            </div>

            {retrievalResults.items.length === 0 ? (
              <p className="text-xs text-slate-500 text-center py-2">No verified knowledge items matched the query.</p>
            ) : (
              <div className="space-y-2">
                {retrievalResults.items.map((res) => (
                  <div key={res.id} className="p-3 bg-slate-900 border border-slate-800 rounded-lg space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-white">{res.title}</span>
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-medium">
                        {res.lifecycle_state}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 line-clamp-2">{res.content}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Filter and Knowledge Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-900/60 p-4 border border-slate-800 rounded-xl">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            placeholder="Search knowledge items..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-amber-500"
          />
        </div>

        <div>
          <select
            value={selectedDomain}
            onChange={(e) => setSelectedDomain(e.target.value)}
            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-amber-500"
          >
            <option value="all">All Domains</option>
            <option value="ESTIMATION">Estimation & Pricing</option>
            <option value="CONTRACT">Contracts & Commitments</option>
            <option value="ARCHITECTURE">Solution Architecture</option>
            <option value="QA">Quality & UAT</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">Loading knowledge items...</div>
      ) : filteredItems.length === 0 ? (
        <div className="p-12 bg-slate-900 border border-slate-800 rounded-xl text-center">
          <BookOpen className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <p className="text-slate-300 font-medium">No knowledge items found</p>
          <p className="text-slate-500 text-sm mt-1">Add curated knowledge or change search filters.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredItems.map((item) => (
            <div
              key={item.id}
              className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
                    {item.topic}
                  </span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-semibold ${
                      item.lifecycle_state === 'CANONICAL'
                        ? 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
                        : item.lifecycle_state === 'VERIFIED'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {item.lifecycle_state}
                  </span>
                </div>

                <h3 className="text-base font-bold text-white mb-2">{item.title}</h3>
                <p className="text-xs text-slate-300 mb-4 line-clamp-3 leading-relaxed">{item.content}</p>

                <div className="space-y-1.5 text-xs text-slate-400 border-t border-slate-800 pt-3">
                  <div className="flex justify-between">
                    <span>Authority:</span>
                    <span className="text-slate-200 font-medium">{item.authority_level}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Confidence:</span>
                    <span className="text-emerald-400 font-medium">
                      {(item.confidence_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
                <span className="text-[11px] text-slate-500 font-mono">{item.canonical_key || 'UNKEYED'}</span>

                {item.lifecycle_state !== 'CANONICAL' && (
                  <button
                    onClick={() =>
                      handlePromote(
                        item.id,
                        item.lifecycle_state === 'INGESTED' ? 'VERIFIED' : 'CANONICAL'
                      )
                    }
                    className="text-xs px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-amber-300 font-medium rounded-lg border border-slate-700 flex items-center gap-1 transition-all"
                  >
                    Promote <ArrowUpRight className="w-3 h-3" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-4">Add Curated Knowledge Item</h3>

            <form onSubmit={handleCreate} className="space-y-4 text-sm">
              <div>
                <label className="block text-slate-300 mb-1">Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Standard Hourly Pricing for Microservices"
                  value={newItem.title}
                  onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 mb-1">Topic</label>
                  <input
                    type="text"
                    required
                    value={newItem.topic}
                    onChange={(e) => setNewItem({ ...newItem, topic: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 mb-1">Domain</label>
                  <select
                    value={newItem.domain}
                    onChange={(e) => setNewItem({ ...newItem, domain: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  >
                    <option value="ESTIMATION">ESTIMATION</option>
                    <option value="CONTRACT">CONTRACT</option>
                    <option value="ARCHITECTURE">ARCHITECTURE</option>
                    <option value="QA">QA</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-slate-300 mb-1">Content / Knowledge Body</label>
                <textarea
                  rows={4}
                  required
                  value={newItem.content}
                  onChange={(e) => setNewItem({ ...newItem, content: e.target.value })}
                  placeholder="Detailed factual statement, standard, or approved design pattern..."
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white font-medium rounded-xl"
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
