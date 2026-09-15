'use client';

import React, { useState, useEffect } from 'react';
import { listProjectFiles, ProjectFileAsset } from '@/lib/api/client_portal';
import { FolderGit2, FileText, Eye, Lock, HardDrive, Download, AlertCircle } from 'lucide-react';

interface ClientFilesPanelProps {
  projectId: string;
}

export const ClientFilesPanel: React.FC<ClientFilesPanelProps> = ({ projectId }) => {
  const [files, setFiles] = useState<ProjectFileAsset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadFiles();
  }, [projectId]);

  const loadFiles = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listProjectFiles(projectId);
      setFiles(data);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch project files.');
    } finally {
      setLoading(false);
    }
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <FolderGit2 className="w-5 h-5 text-purple-400" />
            <span>Client Workspace File Assets</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Audited files published for client access. Internal work drafts remain strictly private.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs text-slate-400 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
          <HardDrive className="w-4 h-4 text-slate-500" />
          <span>Max File Size: 25 MB</span>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-950/40 border border-red-800/50 rounded-lg text-xs text-red-300 flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {loading ? (
        <div className="text-xs text-slate-500 py-8 text-center">Loading file assets...</div>
      ) : files.length === 0 ? (
        <div className="bg-slate-950 border border-slate-800 rounded-xl p-8 text-center space-y-2">
          <FileText className="w-8 h-8 text-slate-600 mx-auto" />
          <p className="text-sm font-semibold text-slate-400">No client-visible files published yet.</p>
          <p className="text-xs text-slate-500">Internal draft assets will appear here once published by North's team.</p>
        </div>
      ) : (
        <div className="divide-y divide-slate-800 border border-slate-800 rounded-xl bg-slate-950/60 overflow-hidden">
          {files.map((file) => (
            <div key={file.id} className="p-4 flex items-center justify-between hover:bg-slate-900/50 transition">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-lg text-purple-400">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-white">{file.filename}</h4>
                  <div className="flex items-center space-x-3 text-xs text-slate-400 mt-0.5">
                    <span>{formatBytes(file.size_bytes)}</span>
                    <span>•</span>
                    <span className="font-mono">{file.mime_type}</span>
                    <span>•</span>
                    <span>{new Date(file.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                {file.visibility === 'CLIENT_VISIBLE' ? (
                  <span className="flex items-center space-x-1 text-[11px] font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-md">
                    <Eye className="w-3.5 h-3.5" />
                    <span>Client Visible</span>
                  </span>
                ) : (
                  <span className="flex items-center space-x-1 text-[11px] font-semibold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded-md">
                    <Lock className="w-3.5 h-3.5" />
                    <span>Internal Only</span>
                  </span>
                )}

                <button
                  className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
                  title="Download File"
                >
                  <Download className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
