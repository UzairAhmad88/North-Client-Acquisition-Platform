'use client';

import React, { useState, useEffect } from 'react';
import {
  Database,
  Search,
  Filter,
  Layers,
  ShieldCheck,
  Clock,
  Plus,
  Tag,
  AlertCircle,
  ExternalLink,
} from 'lucide-react';
import { dataApi, DataCatalogItem, DataSource } from '@/lib/api/data';

export default function DataCatalogViewer() {
  const [items, setItems] = useState<DataCatalogItem[]>([]);
  const [sources, setSources] = useState<DataSource[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [selectedAuthority, setSelectedAuthority] = useState<string>('all');
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    name: '',
    domain: 'LEAD',
    table_or_entity_name: '',
    description: '',
    classification: 'INTERNAL',
    authority_level: 'VERIFIED_DATA',
    data_owner: '',
    sla_freshness_hours: 24,
    sla_quality_threshold: 0.95,
  });

  const loadData = async () => {
    try {
      setLoading(true);
      const [catalogData, sourceData] = await Promise.all([
        dataApi.listCatalogItems(),
        dataApi.listDataSources(),
      ]);
      setItems(catalogData || []);
      setSources(sourceData || []);
    } catch (err) {
      console.error('Failed to load data catalog', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dataApi.createCatalogItem(formData as any);
      setShowCreateModal(false);
      setFormData({
        name: '',
        domain: 'LEAD',
        table_or_entity_name: '',
        description: '',
        classification: 'INTERNAL',
        authority_level: 'VERIFIED_DATA',
        data_owner: '',
        sla_freshness_hours: 24,
        sla_quality_threshold: 0.95,
      });
      loadData();
    } catch (err) {
      console.error('Failed to create catalog item', err);
    }
  };

  const filteredItems = items.filter((item) => {
    const matchesSearch =
      item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.table_or_entity_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (item.description && item.description.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesDomain = selectedDomain === 'all' || item.domain === selectedDomain;
    const matchesAuth = selectedAuthority === 'all' || item.authority_level === selectedAuthority;
    return matchesSearch && matchesDomain && matchesAuth;
  });

  return (
    <div className="space-y-6">
      {/* Header and Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-indigo-400" />
            Enterprise Data Catalog & Semantic Hierarchy
          </h2>
          <p className="text-sm text-slate-400">
            Authoritative registry of datasets, classification tiers, SLA freshness thresholds, and schemas.
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium rounded-xl shadow-lg transition-all"
        >
          <Plus className="w-4 h-4 mr-2" />
          Register Dataset
        </button>
      </div>

      {/* Filter Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-900/60 p-4 border border-slate-800 rounded-xl">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            placeholder="Search catalog items, tables, entities..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div>
          <select
            value={selectedDomain}
            onChange={(e) => setSelectedDomain(e.target.value)}
            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="all">All Domains</option>
            <option value="BUSINESS">Business Discovery</option>
            <option value="LEAD">Leads & Contacts</option>
            <option value="AUDIT">Digital Audit & Scores</option>
            <option value="PROPOSAL">Proposals & Contracts</option>
            <option value="PROJECT">Projects & Tasks</option>
            <option value="GOVERNANCE">Governance & Security</option>
          </select>
        </div>

        <div>
          <select
            value={selectedAuthority}
            onChange={(e) => setSelectedAuthority(e.target.value)}
            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="all">All Authority Levels</option>
            <option value="RAW_DATA">Raw Data (External/Untrusted)</option>
            <option value="NORMALIZED_DATA">Normalized Data</option>
            <option value="VERIFIED_DATA">Verified Data (Authoritative)</option>
            <option value="DERIVED_DATA">Derived Data</option>
            <option value="HUMAN_CONFIRMATION">Human Confirmation</option>
            <option value="CONTRACTUAL_COMMITMENT">Contractual Commitment</option>
          </select>
        </div>
      </div>

      {/* Grid of Catalog Items */}
      {loading ? (
        <div className="p-12 text-center text-slate-400">Loading catalog items...</div>
      ) : filteredItems.length === 0 ? (
        <div className="p-12 bg-slate-900 border border-slate-800 rounded-xl text-center">
          <Layers className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <p className="text-slate-300 font-medium">No catalog items match your search</p>
          <p className="text-slate-500 text-sm mt-1">Register new datasets or adjust filters above.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredItems.map((item) => (
            <div
              key={item.id}
              className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-5 shadow-lg transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-3">
                  <div>
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                      {item.domain}
                    </span>
                    <h3 className="text-base font-bold text-white mt-1.5">{item.name}</h3>
                    <p className="text-xs text-slate-400 font-mono mt-0.5">{item.table_or_entity_name}</p>
                  </div>
                  <span
                    className={`text-xs px-2 py-0.5 rounded font-medium ${
                      item.classification === 'RESTRICTED'
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        : item.classification === 'CONFIDENTIAL'
                        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    }`}
                  >
                    {item.classification}
                  </span>
                </div>

                <p className="text-sm text-slate-400 mb-4 line-clamp-2">
                  {item.description || 'No description provided for this catalog dataset.'}
                </p>

                <div className="space-y-2 pt-3 border-t border-slate-800 text-xs">
                  <div className="flex items-center justify-between text-slate-400">
                    <span className="flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5 text-slate-500" />
                      Authority Tier:
                    </span>
                    <span className="font-medium text-slate-200">{item.authority_level}</span>
                  </div>

                  <div className="flex items-center justify-between text-slate-400">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-slate-500" />
                      Freshness SLA:
                    </span>
                    <span className="font-medium text-slate-200">
                      {item.sla_freshness_hours ? `${item.sla_freshness_hours}h` : 'N/A'}
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-slate-400">
                    <span className="flex items-center gap-1">
                      <Tag className="w-3.5 h-3.5 text-slate-500" />
                      Owner / Steward:
                    </span>
                    <span className="font-medium text-slate-200">{item.data_owner || 'Unassigned'}</span>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-500">
                <span>Created {new Date(item.created_at).toLocaleDateString()}</span>
                <span className="text-indigo-400 hover:text-indigo-300 font-medium cursor-pointer flex items-center gap-1">
                  View Lineage <ExternalLink className="w-3 h-3" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Register Dataset Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-4">Register New Catalog Dataset</h3>

            <form onSubmit={handleCreate} className="space-y-4 text-sm">
              <div>
                <label className="block text-slate-300 mb-1">Dataset Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Qualified Leads Master"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 mb-1">Domain</label>
                  <select
                    value={formData.domain}
                    onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  >
                    <option value="BUSINESS">Business Discovery</option>
                    <option value="LEAD">Leads & Contacts</option>
                    <option value="AUDIT">Digital Audit</option>
                    <option value="PROPOSAL">Proposals</option>
                    <option value="PROJECT">Projects</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 mb-1">Entity / Table</label>
                  <input
                    type="text"
                    required
                    placeholder="leads_master"
                    value={formData.table_or_entity_name}
                    onChange={(e) => setFormData({ ...formData, table_or_entity_name: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 mb-1">Authority Level</label>
                  <select
                    value={formData.authority_level}
                    onChange={(e) => setFormData({ ...formData, authority_level: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  >
                    <option value="RAW_DATA">Raw Data</option>
                    <option value="NORMALIZED_DATA">Normalized Data</option>
                    <option value="VERIFIED_DATA">Verified Data</option>
                    <option value="DERIVED_DATA">Derived Data</option>
                    <option value="HUMAN_CONFIRMATION">Human Confirmation</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 mb-1">Classification</label>
                  <select
                    value={formData.classification}
                    onChange={(e) => setFormData({ ...formData, classification: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  >
                    <option value="PUBLIC">PUBLIC</option>
                    <option value="INTERNAL">INTERNAL</option>
                    <option value="CONFIDENTIAL">CONFIDENTIAL</option>
                    <option value="RESTRICTED">RESTRICTED</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-slate-300 mb-1">Description</label>
                <textarea
                  rows={2}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Primary canonical table for enterprise leads and verified company scores..."
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
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-xl"
                >
                  Save Dataset
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
