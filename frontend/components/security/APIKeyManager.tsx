'use client';

import React, { useState, useEffect } from 'react';
import { Key, Plus, Copy, Check, Trash2, RefreshCw, AlertTriangle } from 'lucide-react';
import { securityApi, APIKeyItem, APIKeyCreatedResponse } from '@/lib/api/security';

export default function APIKeyManager() {
  const [keys, setKeys] = useState<APIKeyItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [keyName, setKeyName] = useState<string>('');
  const [selectedScopes, setSelectedScopes] = useState<string[]>(['leads.read', 'projects.read']);
  const [createdSecret, setCreatedSecret] = useState<APIKeyCreatedResponse | null>(null);
  const [copied, setCopied] = useState<boolean>(false);
  const [submitting, setSubmitting] = useState<boolean>(false);

  const availableScopes = [
    'leads.read',
    'leads.write',
    'projects.read',
    'projects.write',
    'analytics.read',
    'webhooks.write',
    'research.run',
  ];

  const fetchKeys = async () => {
    try {
      setLoading(true);
      const res = await securityApi.listAPIKeys();
      if (res) {
        setKeys(res);
      }
    } catch (err) {
      console.error('Failed to load API keys', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKeys();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!keyName) return;
    try {
      setSubmitting(true);
      const res = await securityApi.createAPIKey({
        name: keyName,
        scopes: selectedScopes,
      });
      if (res) {
        setCreatedSecret(res);
      }
      fetchKeys();
    } catch (err) {
      console.error('Failed to create API key', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleRevoke = async (keyId: string) => {
    try {
      await securityApi.revokeAPIKey(keyId);
      fetchKeys();
    } catch (err) {
      console.error('Failed to revoke API key', err);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white">Machine-to-Machine API Keys</h3>
          <p className="text-xs text-slate-400">
            Scoped access credentials for background workers, integrations, and automated pipelines.
          </p>
        </div>

        <button
          onClick={() => {
            setCreatedSecret(null);
            setKeyName('');
            setIsModalOpen(true);
          }}
          className="flex items-center space-x-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-sm font-medium transition-colors shadow-lg shadow-emerald-900/20"
        >
          <Plus className="w-4 h-4" />
          <span>Generate API Key</span>
        </button>
      </div>

      {/* Keys List */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-slate-950/60 text-slate-400 text-xs uppercase font-semibold border-b border-slate-800">
            <tr>
              <th className="px-6 py-4">Key Name & Prefix</th>
              <th className="px-6 py-4">Granted Scopes</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Created Date</th>
              <th className="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {keys.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                  {loading ? 'Loading API keys...' : 'No API keys configured yet.'}
                </td>
              </tr>
            ) : (
              keys.map((k) => (
                <tr key={k.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-6 py-4">
                    <div className="font-medium text-white">{k.name}</div>
                    <div className="text-xs font-mono text-slate-400 mt-0.5">{k.key_prefix}...</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-wrap gap-1">
                      {k.scopes.map((s) => (
                        <span
                          key={s}
                          className="px-2 py-0.5 rounded bg-slate-800 text-[11px] font-mono text-slate-300"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    {!k.is_revoked ? (
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400">
                        Active
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400">
                        Revoked
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-xs text-slate-400">
                    {new Date(k.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 text-right">
                    {!k.is_revoked && (
                      <button
                        onClick={() => handleRevoke(k.id)}
                        className="p-1.5 text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
                        title="Revoke Key"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Key Creation Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5">
            {!createdSecret ? (
              <>
                <h3 className="text-lg font-bold text-white">Create New API Key</h3>
                <form onSubmit={handleCreate} className="space-y-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-400 uppercase mb-1">
                      Key Description / Service Name
                    </label>
                    <input
                      type="text"
                      required
                      value={keyName}
                      onChange={(e) => setKeyName(e.target.value)}
                      placeholder="e.g. CI/CD Deployment Worker"
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-400 uppercase mb-2">
                      Authorized Scopes
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      {availableScopes.map((scope) => {
                        const checked = selectedScopes.includes(scope);
                        return (
                          <label
                            key={scope}
                            className={`flex items-center space-x-2 p-2 rounded-xl border text-xs cursor-pointer transition-colors ${
                              checked
                                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                                : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
                            }`}
                          >
                            <input
                              type="checkbox"
                              checked={checked}
                              onChange={() => {
                                if (checked) {
                                  setSelectedScopes(selectedScopes.filter((s) => s !== scope));
                                } else {
                                  setSelectedScopes([...selectedScopes, scope]);
                                }
                              }}
                              className="rounded border-slate-700 text-emerald-500 focus:ring-0"
                            />
                            <span>{scope}</span>
                          </label>
                        );
                      })}
                    </div>
                  </div>

                  <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-800">
                    <button
                      type="button"
                      onClick={() => setIsModalOpen(false)}
                      className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-sm font-medium transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={submitting}
                      className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white rounded-xl text-sm font-medium transition-colors shadow-lg shadow-emerald-900/20"
                    >
                      {submitting ? 'Generating...' : 'Generate Key'}
                    </button>
                  </div>
                </form>
              </>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center space-x-3 text-amber-400">
                  <AlertTriangle className="w-6 h-6" />
                  <h3 className="text-lg font-bold text-white">Save Your API Key</h3>
                </div>

                <p className="text-xs text-slate-400">
                  This secret key will <strong>never be shown again</strong>. Please copy and store it securely in your environment variables.
                </p>

                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex items-center justify-between font-mono text-xs text-emerald-400 break-all">
                  <span>{createdSecret.secret_key}</span>
                  <button
                    onClick={() => copyToClipboard(createdSecret.secret_key)}
                    className="p-2 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors shrink-0 ml-2"
                  >
                    {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>

                <button
                  onClick={() => setIsModalOpen(false)}
                  className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-sm font-medium transition-colors"
                >
                  Done
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
