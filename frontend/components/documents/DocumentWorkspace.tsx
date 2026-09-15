'use client';

import React, { useState, useEffect } from 'react';
import { documentsApi, FileItem, ManagedDocument } from '@/lib/api/documents';
import { FileUpload } from '@/components/files/FileUpload';
import Link from 'next/link';

export function DocumentWorkspace() {
  const [activeTab, setActiveTab] = useState<'documents' | 'files' | 'upload'>('documents');
  const [documents, setDocuments] = useState<ManagedDocument[]>([]);
  const [files, setFiles] = useState<FileItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchFilter, setSearchFilter] = useState('');
  const [classificationFilter, setClassificationFilter] = useState('');

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [docsRes, filesRes] = await Promise.all([
        documentsApi.listDocuments(),
        documentsApi.listFiles(),
      ]);
      setDocuments(docsRes || []);
      setFiles(filesRes || []);
    } catch (err) {
      console.error('Failed to load documents workspace data', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const filteredDocs = documents.filter((d) => {
    const matchesSearch = d.title.toLowerCase().includes(searchFilter.toLowerCase());
    const matchesClass = !classificationFilter || d.classification === classificationFilter;
    return matchesSearch && matchesClass;
  });

  const filteredFiles = files.filter((f) => {
    const matchesSearch = f.name.toLowerCase().includes(searchFilter.toLowerCase());
    const matchesClass = !classificationFilter || f.classification === classificationFilter;
    return matchesSearch && matchesClass;
  });

  return (
    <div className="space-y-6 text-slate-100">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <span>📁</span> Unified Document & Digital Asset Workspace
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Governed document lifecycle, immutable versioning, secure previews, and AI document understanding.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab('upload')}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold rounded-lg shadow-lg shadow-blue-500/20 transition"
          >
            + Upload Asset
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('documents')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
            activeTab === 'documents'
              ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          📄 Managed Documents ({documents.length})
        </button>
        <button
          onClick={() => setActiveTab('files')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
            activeTab === 'files'
              ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          📦 Raw Files & Storage ({files.length})
        </button>
        <button
          onClick={() => setActiveTab('upload')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
            activeTab === 'upload'
              ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          ⬆️ Upload Pipeline
        </button>
      </div>

      {/* Filter Bar */}
      {activeTab !== 'upload' && (
        <div className="flex flex-col md:flex-row items-center gap-4 bg-slate-900/60 p-4 border border-slate-800 rounded-xl">
          <input
            type="text"
            placeholder="Filter by name, keyword..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full md:w-80 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
          />
          <select
            value={classificationFilter}
            onChange={(e) => setClassificationFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="">All Classifications</option>
            <option value="GENERAL">General</option>
            <option value="REQUIREMENTS">Requirements</option>
            <option value="PROPOSAL">Proposal</option>
            <option value="CONTRACT">Contract</option>
            <option value="DELIVERABLE">Deliverable</option>
            <option value="TEST_EVIDENCE">Test Evidence</option>
            <option value="SUPPORT_ATTACHMENT">Support Attachment</option>
            <option value="KNOWLEDGE_SOURCE">Knowledge Source</option>
          </select>
        </div>
      )}

      {/* Tab Contents */}
      {activeTab === 'upload' && (
        <FileUpload
          onUploadSuccess={() => {
            loadData();
            setActiveTab('documents');
          }}
        />
      )}

      {activeTab === 'documents' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {isLoading ? (
            <div className="col-span-full py-12 text-center text-slate-500">Loading documents...</div>
          ) : filteredDocs.length === 0 ? (
            <div className="col-span-full py-12 text-center text-slate-500 border border-slate-800 rounded-xl">
              No managed documents found matching filters.
            </div>
          ) : (
            filteredDocs.map((doc) => (
              <div
                key={doc.id}
                className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition space-y-3"
              >
                <div className="flex items-start justify-between">
                  <span className="text-xl">📄</span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${
                      doc.status === 'APPROVED'
                        ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        : doc.status === 'SUBMITTED_FOR_REVIEW'
                        ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                        : 'bg-slate-800 text-slate-300'
                    }`}
                  >
                    {doc.status}
                  </span>
                </div>
                <div>
                  <h4 className="font-semibold text-white truncate">{doc.title}</h4>
                  <div className="text-xs text-slate-400 mt-1 flex items-center gap-2">
                    <span>v{doc.current_version_number}</span>
                    <span>•</span>
                    <span className="uppercase text-[11px] font-mono text-blue-400">{doc.classification}</span>
                  </div>
                </div>
                <div className="text-xs text-slate-500 pt-2 border-t border-slate-800 flex items-center justify-between">
                  <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                  <Link
                    href={`/documents/${doc.id}`}
                    className="text-blue-400 hover:text-blue-300 font-medium"
                  >
                    View Details →
                  </Link>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'files' && (
        <div className="overflow-x-auto bg-slate-900 border border-slate-800 rounded-xl">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/60 text-slate-400 border-b border-slate-800 uppercase font-semibold text-[10px]">
              <tr>
                <th className="py-3 px-4">Name</th>
                <th className="py-3 px-4">Type</th>
                <th className="py-3 px-4">Size</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Classification</th>
                <th className="py-3 px-4">Created</th>
                <th className="py-3 px-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filteredFiles.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-slate-500">
                    No files found.
                  </td>
                </tr>
              ) : (
                filteredFiles.map((file) => (
                  <tr key={file.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3 px-4 font-medium text-white flex items-center gap-2">
                      <span>📎</span>
                      <span className="truncate max-w-xs">{file.name}</span>
                    </td>
                    <td className="py-3 px-4 text-slate-400">{file.mime_type}</td>
                    <td className="py-3 px-4 text-slate-400">{Math.round(file.size_bytes / 1024)} KB</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        {file.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400">{file.classification}</td>
                    <td className="py-3 px-4 text-slate-500">{new Date(file.created_at).toLocaleDateString()}</td>
                    <td className="py-3 px-4 text-right">
                      <a
                        href={`/api/v1/files/${file.id}/download`}
                        className="text-blue-400 hover:text-blue-300 font-medium"
                      >
                        Download
                      </a>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
