'use client';

import React, { useState } from 'react';
import { BackupRecord, RestoreVerificationTest } from '@/lib/api/reliability';

interface Props {
  backups: BackupRecord[];
  restoreTests: RestoreVerificationTest[];
  onTriggerBackup: () => void;
  onRunRestoreTest: (backupId: string) => void;
  isLoading: boolean;
}

export function BackupRestoreStatus({
  backups,
  restoreTests,
  onTriggerBackup,
  onRunRestoreTest,
  isLoading,
}: Props) {
  const [selectedBackupId, setSelectedBackupId] = useState<string | null>(null);

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-6">
      {/* Backups Section */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <div>
            <h3 className="text-lg font-semibold text-white">Automated Backups & SHA-256 Integrity Verification</h3>
            <p className="text-xs text-slate-400">
              Database WAL, full dumps, configuration vaults, and distributed object storage
            </p>
          </div>

          <button
            onClick={onTriggerBackup}
            disabled={isLoading}
            className="px-4 py-2 bg-emerald-600/80 hover:bg-emerald-600 text-white text-xs font-semibold rounded-xl transition flex items-center gap-2"
          >
            <span>💾</span> {isLoading ? 'Triggering...' : 'Trigger Backup Snapshot'}
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/80 text-slate-400 text-[11px] uppercase border-b border-slate-800">
              <tr>
                <th className="p-3">Type</th>
                <th className="p-3">Status</th>
                <th className="p-3">Size</th>
                <th className="p-3">SHA-256 Checksum</th>
                <th className="p-3">Verified</th>
                <th className="p-3">Timestamp</th>
                <th className="p-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {backups.map((b) => (
                <tr key={b.id} className="hover:bg-slate-800/30 transition">
                  <td className="p-3 font-semibold text-white">{b.backup_type}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-[10px]">
                      {b.status}
                    </span>
                  </td>
                  <td className="p-3 font-mono">{formatBytes(b.size_bytes)}</td>
                  <td className="p-3 font-mono text-[10px] text-slate-400 truncate max-w-[140px]" title={b.checksum_sha256}>
                    {b.checksum_sha256.substring(0, 16)}...
                  </td>
                  <td className="p-3">
                    <span className={`text-[10px] font-bold ${b.verified ? 'text-emerald-400' : 'text-amber-400'}`}>
                      {b.verified ? '✓ Verified' : 'Pending Test'}
                    </span>
                  </td>
                  <td className="p-3 text-slate-400">{new Date(b.started_at).toLocaleString()}</td>
                  <td className="p-3 text-right">
                    <button
                      onClick={() => onRunRestoreTest(b.id)}
                      className="px-2.5 py-1 bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 border border-cyan-500/30 rounded text-[11px] transition"
                    >
                      Test Restore
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Restore Verification Tests Sandbox */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-white mb-1">Isolated Sandbox Restore Verification Tests</h3>
        <p className="text-xs text-slate-400 mb-4">
          Automated spin-up of isolated test databases to prove zero data corruption and validate RTO timings
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {restoreTests.map((test) => (
            <div key={test.test_id} className="bg-slate-950/60 border border-slate-800/80 p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-white">{test.environment}</span>
                <span className="text-[10px] font-bold px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                  {test.status}
                </span>
              </div>

              <div className="text-[11px] text-slate-400 space-y-1 pt-1">
                <div className="flex justify-between">
                  <span>RTO Achieved:</span>
                  <span className="font-mono text-emerald-400 font-bold">{test.rto_achieved_seconds}s</span>
                </div>
                <div className="flex justify-between">
                  <span>Tables Restored:</span>
                  <span className="font-mono text-slate-200">{test.tables_restored_count} tables</span>
                </div>
                <div className="flex justify-between">
                  <span>Records Verified:</span>
                  <span className="font-mono text-slate-200">{test.records_verified_count} rows</span>
                </div>
                <div className="flex justify-between">
                  <span>Data Integrity:</span>
                  <span className="text-emerald-400 font-semibold">{test.data_integrity_passed ? 'PASS (100%)' : 'FAIL'}</span>
                </div>
              </div>

              <div className="text-[10px] text-slate-500 pt-2 border-t border-slate-800/50">
                Executed: {new Date(test.executed_at).toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
