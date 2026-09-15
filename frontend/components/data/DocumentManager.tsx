'use client';

import React, { useState, useEffect } from 'react';
import {
  FileText,
  ShieldCheck,
  CheckCircle2,
  XCircle,
  Plus,
  Search,
  Lock,
  FileCode,
  Hash,
  RefreshCw,
  ExternalLink,
} from 'lucide-react';
import { dataApi, DocumentRecord, DocumentIntegrityVerification } from '@/lib/api/data';

export default function DocumentManager() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Integrity Check Modal / State
  const [selectedDoc, setSelectedDoc] = useState<DocumentRecord | null>(null);
  const [verificationContent, setVerificationContent] = useState('');
  const [verificationResult, setVerificationResult] = useState<DocumentIntegrityVerification | null>(
    null
  );
  const [verifying, setVerifying] = useState(false);

  // Form State
  const [newDoc, setNewDoc] = useState({
    title: '',
    document_type: 'CONTRACT',
    content: 'Master Service Agreement between Uzaii Develop and Acme Corp...',
    summary: 'Definitive contract commitment',
    classification: 'CONFIDENTIAL',
    authority_level: 'CONTRACTUAL_COMMITMENT',
    domain: 'CONTRACT',
  });

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const docs = await dataApi.listDocuments();
      setDocuments(docs || []);
    } catch (err) {
      console.error('Failed to load documents', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dataApi.createDocument(newDoc as any);
      setShowCreateModal(false);
      setNewDoc({
        title: '',
        document_type: 'CONTRACT',
        content: '',
        summary: '',
        classification: 'CONFIDENTIAL',
        authority_level: 'CONTRACTUAL_COMMITMENT',
        domain: 'CONTRACT',
      });
      loadDocuments();
    } catch (err) {
      console.error('Failed to create document', err);
    }
  };

  const handleVerify = async () => {
    if (!selectedDoc) return;
    try {
      setVerifying(true);
      const res = await dataApi.verifyDocument(
        selectedDoc.id,
        verificationContent,
        selectedDoc.current_version
      );
      setVerificationResult(res);
    } catch (err) {
      console.error('Failed to verify document integrity', err);
    } finally {
      setVerifying(false);
    }
  };

  const filteredDocs = documents.filter((d) =>
    d.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.tracking_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.document_type.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-400" />
            Immutable Business Documents & Integrity Archive
          </h2>
          <p className="text-sm text-slate-400">
            Cryptographic SHA-256 integrity checksums, version history, and tamper verification.
          </p>
        </div>

        <button
          onClick={() => setShowCreateModal(true)}
          className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-xl shadow-lg transition-all"
        >
          <Plus className="w-4 h-4 mr-2" />
          Create Document
        </button>
      </div>

      {/* Filter */}
      <div className="relative bg-slate-900 border border-slate-800 rounded-xl p-2">
        <Search className="w-4 h-4 absolute left-4 top-4 text-slate-400" />
        <input
          type="text"
          placeholder="Search documents by title, tracking ID, or type..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-blue-500"
        />
      </div>

      {/* Document Grid */}
      {loading ? (
        <div className="p-12 text-center text-slate-400">Loading documents...</div>
      ) : filteredDocs.length === 0 ? (
        <div className="p-12 bg-slate-900 border border-slate-800 rounded-xl text-center">
          <FileText className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <p className="text-slate-300 font-medium">No documents found</p>
          <p className="text-slate-500 text-sm mt-1">Create an authoritative business document to begin.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDocs.map((doc) => (
            <div
              key={doc.id}
              className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                    {doc.tracking_id}
                  </span>
                  <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                    {doc.status}
                  </span>
                </div>

                <h3 className="text-base font-bold text-white mb-1">{doc.title}</h3>
                <p className="text-xs text-slate-400 mb-4">{doc.document_type} • v{doc.current_version}</p>

                <div className="p-2.5 bg-slate-950 border border-slate-800 rounded-lg space-y-1 mb-4">
                  <div className="flex items-center justify-between text-[11px] text-slate-400">
                    <span className="flex items-center gap-1">
                      <Hash className="w-3 h-3 text-slate-500" />
                      SHA-256 Checksum:
                    </span>
                  </div>
                  <p className="font-mono text-[10px] text-slate-300 break-all leading-tight">
                    {doc.latest_sha256}
                  </p>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
                <span className="text-[11px] text-slate-500">
                  {new Date(doc.created_at).toLocaleDateString()}
                </span>

                <button
                  onClick={() => {
                    setSelectedDoc(doc);
                    setVerificationContent('');
                    setVerificationResult(null);
                  }}
                  className="text-xs px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-blue-300 font-medium rounded-lg border border-slate-700 flex items-center gap-1.5 transition-all"
                >
                  <ShieldCheck className="w-3.5 h-3.5 text-blue-400" />
                  Verify Hash
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Verify Hash Modal */}
      {selectedDoc && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-2 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-blue-400" />
              Cryptographic Integrity Verification
            </h3>
            <p className="text-xs text-slate-400 mb-4">
              Paste the file content or payload to mathematically test for unauthorized tampering.
            </p>

            <div className="space-y-4 text-sm">
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1 text-xs">
                <span className="text-slate-400">Document:</span> <strong className="text-white">{selectedDoc.title}</strong>
                <div className="text-slate-400 truncate">
                  Expected SHA-256: <span className="font-mono text-slate-300">{selectedDoc.latest_sha256}</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  Content to Validate
                </label>
                <textarea
                  rows={4}
                  value={verificationContent}
                  onChange={(e) => setVerificationContent(e.target.value)}
                  placeholder="Paste document text here to test integrity..."
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white font-mono text-xs"
                />
              </div>

              {verificationResult && (
                <div
                  className={`p-3 rounded-xl border flex items-center gap-3 text-xs ${
                    verificationResult.is_valid
                      ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                      : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
                  }`}
                >
                  {verificationResult.is_valid ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
                  ) : (
                    <XCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
                  )}
                  <div>
                    <strong className="block font-bold">
                      {verificationResult.is_valid
                        ? 'Integrity Verified: Match 100%'
                        : 'TAMPER DETECTED: Hash Mismatch'}
                    </strong>
                    <span className="font-mono text-[10px] break-all">
                      Calculated: {verificationResult.calculated_sha256}
                    </span>
                  </div>
                </div>
              )}

              <div className="flex justify-end space-x-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setSelectedDoc(null)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl"
                >
                  Close
                </button>
                <button
                  type="button"
                  onClick={handleVerify}
                  disabled={verifying || !verificationContent}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-medium rounded-xl"
                >
                  {verifying ? 'Verifying...' : 'Compute & Compare'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Create Document Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-4">Create Immutable Business Document</h3>

            <form onSubmit={handleCreate} className="space-y-4 text-sm">
              <div>
                <label className="block text-slate-300 mb-1">Document Title</label>
                <input
                  type="text"
                  required
                  placeholder="Master Service Agreement - Enterprise v1"
                  value={newDoc.title}
                  onChange={(e) => setNewDoc({ ...newDoc, title: e.target.value })}
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 mb-1">Document Type</label>
                  <select
                    value={newDoc.document_type}
                    onChange={(e) => setNewDoc({ ...newDoc, document_type: e.target.value })}
                    className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white"
                  >
                    <option value="CONTRACT">CONTRACT</option>
                    <option value="PROPOSAL">PROPOSAL</option>
                    <option value="AUDIT_REPORT">AUDIT REPORT</option>
                    <option value="CHANGE_BASELINE">CHANGE BASELINE</option>
                    <option value="SPECIFICATION">SPECIFICATION</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 mb-1">Classification</label>
                  <select
                    value={newDoc.classification}
                    onChange={(e) => setNewDoc({ ...newDoc, classification: e.target.value })}
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
                <label className="block text-slate-300 mb-1">Document Content</label>
                <textarea
                  rows={4}
                  required
                  value={newDoc.content}
                  onChange={(e) => setNewDoc({ ...newDoc, content: e.target.value })}
                  placeholder="Full text of the immutable document..."
                  className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white font-mono text-xs"
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
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-xl"
                >
                  Publish & Generate Hash
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
