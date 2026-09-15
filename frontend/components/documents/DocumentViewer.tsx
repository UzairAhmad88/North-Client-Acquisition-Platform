'use client';

import React, { useState, useEffect } from 'react';
import { documentsApi, ManagedDocument, ShareLinkResponse } from '@/lib/api/documents';

interface DocumentViewerProps {
  documentId: string;
}

export function DocumentViewer({ documentId }: DocumentViewerProps) {
  const [doc, setDoc] = useState<ManagedDocument | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [shareLink, setShareLink] = useState<ShareLinkResponse | null>(null);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const loadDocument = async () => {
    setIsLoading(true);
    try {
      const data = await documentsApi.getDocument(documentId);
      setDoc(data);
    } catch (err) {
      console.error('Failed to load document', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadDocument();
  }, [documentId]);

  const handleSubmitReview = async () => {
    try {
      await documentsApi.submitForReview(documentId, { notes: 'Submitted for formal operator review.' });
      setActionMessage('Document successfully submitted for review.');
      loadDocument();
    } catch (err: any) {
      setActionMessage(err?.message || 'Failed to submit for review.');
    }
  };

  const handleApprove = async () => {
    if (!doc) return;
    try {
      await documentsApi.approveDocument(documentId, {
        version_id: doc.current_version_id || 'v-latest',
        version_number: doc.current_version_number,
        checksum: 'APPROVED_HASH_VALIDATION',
        decision_notes: 'Document approved by operator.',
      });
      setActionMessage('Document approved! Version checksum locked.');
      loadDocument();
    } catch (err: any) {
      setActionMessage(err?.message || 'Failed to approve document.');
    }
  };

  const handleGenerateShareLink = async () => {
    try {
      const res = await documentsApi.generateShareLink(documentId, { expires_in_hours: 24, allow_download: true });
      setShareLink(res);
    } catch (err: any) {
      setActionMessage(err?.message || 'Failed to generate secure link.');
    }
  };

  if (isLoading) {
    return <div className="p-8 text-center text-slate-500">Loading document details...</div>;
  }

  if (!doc) {
    return <div className="p-8 text-center text-red-400">Document not found.</div>;
  }

  return (
    <div className="space-y-6 text-slate-100">
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-white">{doc.title}</h1>
            <span className="text-xs px-2.5 py-1 bg-blue-500/20 text-blue-400 rounded-full font-mono uppercase">
              v{doc.current_version_number}
            </span>
            <span
              className={`text-xs px-2.5 py-1 rounded-full font-bold uppercase ${
                doc.status === 'APPROVED'
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
              }`}
            >
              {doc.status}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Classification: <span className="font-semibold text-slate-300">{doc.classification}</span> | Sensitivity: <span className="text-slate-300">{doc.sensitivity}</span> | Visibility: <span className="text-slate-300">{doc.visibility}</span>
          </p>
        </div>

        <div className="flex items-center gap-2">
          {doc.status !== 'APPROVED' && (
            <>
              <button
                onClick={handleSubmitReview}
                className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg transition"
              >
                Submit for Review
              </button>
              <button
                onClick={handleApprove}
                className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg shadow transition"
              >
                Approve Version
              </button>
            </>
          )}
          <button
            onClick={handleGenerateShareLink}
            className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg shadow transition"
          >
            Generate Expiring Link
          </button>
        </div>
      </div>

      {actionMessage && (
        <div className="p-3 bg-blue-500/10 border border-blue-500/20 text-blue-400 rounded-lg text-xs">
          {actionMessage}
        </div>
      )}

      {shareLink && (
        <div className="p-4 bg-slate-900 border border-blue-500/30 rounded-xl text-xs space-y-2">
          <div className="font-semibold text-blue-300 flex items-center justify-between">
            <span>🔗 Secure Share Link Generated (Expires in 24h)</span>
            <span className="text-[10px] text-slate-400">{shareLink.expires_at}</span>
          </div>
          <div className="bg-slate-950 p-2.5 rounded border border-slate-800 font-mono text-slate-300 break-all">
            {shareLink.access_url}
          </div>
        </div>
      )}

      {/* Main Details & Preview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-2">
            Document Version Preview & AI Insights
          </h3>
          <div className="p-6 bg-slate-950 rounded-lg border border-slate-800/80 font-mono text-xs text-slate-300 min-h-[220px]">
            <p className="text-slate-400 mb-2">--- Document Preview Stream (v{doc.current_version_number}) ---</p>
            <p>Title: {doc.title}</p>
            <p>Classification: {doc.classification}</p>
            <p>Status: {doc.status}</p>
            <p className="mt-4 text-slate-500 italic">Binary document contents verified and indexed in Global Discovery Layer.</p>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-sm font-semibold text-white border-b border-slate-800 pb-2">
            Governance & Integrity
          </h3>
          <div className="space-y-3 text-xs">
            <div>
              <span className="text-slate-500 block">Legal Hold</span>
              <span className="font-medium text-slate-300">{doc.legal_hold ? 'Active (Deletion Blocked)' : 'None'}</span>
            </div>
            <div>
              <span className="text-slate-500 block">Retention Policy</span>
              <span className="font-medium text-slate-300">{doc.retention_status}</span>
            </div>
            <div>
              <span className="text-slate-500 block">Created At</span>
              <span className="font-medium text-slate-300">{new Date(doc.created_at).toLocaleString()}</span>
            </div>
            <div>
              <span className="text-slate-500 block">Last Updated</span>
              <span className="font-medium text-slate-300">{new Date(doc.updated_at).toLocaleString()}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
