'use client';

import React, { useState, useRef } from 'react';
import { documentsApi, FileUploadResponse } from '@/lib/api/documents';

interface FileUploadProps {
  workspaceId?: string;
  onUploadSuccess?: (result: FileUploadResponse) => void;
}

export function FileUpload({ workspaceId = 'default_workspace', onUploadSuccess }: FileUploadProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successResult, setSuccessResult] = useState<FileUploadResponse | null>(null);
  const [classification, setClassification] = useState('GENERAL');
  const [sensitivity, setSensitivity] = useState('INTERNAL');
  const [visibility, setVisibility] = useState('INTERNAL');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setError(null);
    setSuccessResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('workspace_id', workspaceId);
      formData.append('classification', classification);
      formData.append('sensitivity', sensitivity);
      formData.append('visibility', visibility);

      const res = await documentsApi.uploadFile(formData);
      setSuccessResult(res);
      if (onUploadSuccess) onUploadSuccess(res);
    } catch (err: any) {
      setError(err?.message || 'File upload failed or blocked by security policy.');
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">Upload Digital Asset / Document</h3>
        <span className="text-xs px-2.5 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full font-medium">
          Multi-Stage Scanning & Validation
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1">Classification</label>
          <select
            value={classification}
            onChange={(e) => setClassification(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="GENERAL">General</option>
            <option value="REQUIREMENTS">Requirements</option>
            <option value="PROPOSAL">Proposal</option>
            <option value="CONTRACT">Contract</option>
            <option value="PROJECT_DOCUMENT">Project Document</option>
            <option value="DELIVERABLE">Deliverable</option>
            <option value="TEST_EVIDENCE">Test Evidence</option>
            <option value="SUPPORT_ATTACHMENT">Support Attachment</option>
            <option value="KNOWLEDGE_SOURCE">Knowledge Source</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1">Sensitivity</label>
          <select
            value={sensitivity}
            onChange={(e) => setSensitivity(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="INTERNAL">Internal</option>
            <option value="PUBLIC">Public</option>
            <option value="CONFIDENTIAL">Confidential</option>
            <option value="RESTRICTED">Restricted</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-medium text-slate-400 mb-1">Visibility Scope</label>
          <select
            value={visibility}
            onChange={(e) => setVisibility(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="INTERNAL">Internal Only</option>
            <option value="CLIENT_VISIBLE">Client Visible</option>
            <option value="RESTRICTED">Restricted</option>
          </select>
        </div>
      </div>

      <div
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
          isUploading
            ? 'border-blue-500 bg-blue-500/5'
            : 'border-slate-700 hover:border-blue-500 hover:bg-slate-800/50'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          onChange={handleFileChange}
          disabled={isUploading}
        />
        <div className="flex flex-col items-center justify-center space-y-2">
          <div className="p-3 bg-slate-800 rounded-full text-blue-400">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <p className="text-sm font-medium text-slate-300">
            {isUploading ? 'Validating, Scanning & Uploading...' : 'Click or Drag file to upload'}
          </p>
          <p className="text-xs text-slate-500">PDF, DOCX, PNG, JPG, MD, CSV, JSON (Up to 100MB)</p>
        </div>
      </div>

      {error && (
        <div className="mt-4 p-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg text-xs flex items-center space-x-2">
          <span>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {successResult && (
        <div className="mt-4 p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-400 text-xs">
          <div className="font-semibold text-emerald-300 mb-1">Upload & Scanning Complete!</div>
          <div>Filename: {successResult.filename} ({Math.round(successResult.size_bytes / 1024)} KB)</div>
          <div>SHA-256: {successResult.checksum_sha256}</div>
          <div>Status: <span className="font-mono uppercase">{successResult.status}</span></div>
          {successResult.chunks_count > 0 && (
            <div className="text-slate-400 mt-1">Indexed {successResult.chunks_count} structured text chunks for Global Search & AI.</div>
          )}
        </div>
      )}
    </div>
  );
}
