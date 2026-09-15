'use client';

import React, { useEffect, useState } from 'react';
import {
  DeliveryChannel,
  DeliveryRecord,
  DeliveryStatus,
  communicationApi,
} from '@/lib/api/communication';

export const DeliveryAuditExplorer: React.FC = () => {
  const [deliveries, setDeliveries] = useState<DeliveryRecord[]>([]);
  const [statusFilter, setStatusFilter] = useState<DeliveryStatus | undefined>(undefined);
  const [channelFilter, setChannelFilter] = useState<DeliveryChannel | undefined>(undefined);
  const [loading, setLoading] = useState(true);
  const [retryingId, setRetryingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedLog, setSelectedLog] = useState<DeliveryRecord | null>(null);

  const loadDeliveries = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await communicationApi.listDeliveries({
        status: statusFilter,
        channel: channelFilter,
      });
      setDeliveries(data || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load delivery logs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDeliveries();
  }, [statusFilter, channelFilter]);

  const handleRetry = async (deliveryId: string) => {
    setRetryingId(deliveryId);
    try {
      await communicationApi.retryDelivery(deliveryId);
      loadDeliveries();
    } catch (err: any) {
      setError(err.message || 'Failed to retry delivery');
    } finally {
      setRetryingId(null);
    }
  };

  const getStatusBadge = (status: DeliveryStatus) => {
    switch (status) {
      case 'DELIVERED':
      case 'SENT':
        return 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40';
      case 'QUEUED':
      case 'PENDING':
        return 'bg-blue-500/20 text-blue-300 border border-blue-500/40';
      case 'FAILED':
        return 'bg-amber-500/20 text-amber-300 border border-amber-500/40';
      case 'DEAD_LETTER':
        return 'bg-red-500/20 text-red-300 border border-red-500/40 font-bold';
      case 'SKIPPED_QUIET_HOURS':
      case 'SUPPRESSED':
      default:
        return 'bg-slate-700/50 text-slate-400 border border-slate-700';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-orange-400"></span>
            Communication Delivery & Audit Explorer
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time delivery lifecycle telemetry, provider dispatch responses, and dead-letter retry controls.
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-2">
          <select
            value={statusFilter || ''}
            onChange={(e) => setStatusFilter((e.target.value as DeliveryStatus) || undefined)}
            className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-1.5 focus:ring-1 focus:ring-orange-500"
          >
            <option value="">All Statuses</option>
            <option value="QUEUED">QUEUED</option>
            <option value="SENT">SENT</option>
            <option value="DELIVERED">DELIVERED</option>
            <option value="FAILED">FAILED</option>
            <option value="DEAD_LETTER">DEAD_LETTER</option>
            <option value="SUPPRESSED">SUPPRESSED</option>
            <option value="SKIPPED_QUIET_HOURS">SKIPPED_QUIET_HOURS</option>
          </select>

          <select
            value={channelFilter || ''}
            onChange={(e) => setChannelFilter((e.target.value as DeliveryChannel) || undefined)}
            className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-1.5 focus:ring-1 focus:ring-orange-500"
          >
            <option value="">All Channels</option>
            <option value="IN_APP">IN_APP</option>
            <option value="EMAIL">EMAIL</option>
            <option value="SMS">SMS</option>
            <option value="WEBHOOK">WEBHOOK</option>
            <option value="PUSH">PUSH</option>
            <option value="REALTIME_WS">REALTIME_WS</option>
          </select>

          <button
            onClick={loadDeliveries}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs rounded-lg border border-slate-700"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-950/60 border border-red-800 rounded-lg text-red-200 text-xs">
          {error}
        </div>
      )}

      {/* Deliveries Table */}
      <div className="border border-slate-800 rounded-lg overflow-hidden">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-950/60 text-slate-400 border-b border-slate-800 font-semibold">
              <th className="p-3">Delivery ID</th>
              <th className="p-3">Channel</th>
              <th className="p-3">Status</th>
              <th className="p-3">Recipient</th>
              <th className="p-3">Retries</th>
              <th className="p-3">Created</th>
              <th className="p-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-500 animate-pulse">
                  Loading delivery logs...
                </td>
              </tr>
            ) : deliveries.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-8 text-slate-500">
                  No delivery records found matching criteria.
                </td>
              </tr>
            ) : (
              deliveries.map((del) => {
                const canRetry = del.status === 'FAILED' || del.status === 'DEAD_LETTER';
                return (
                  <tr key={del.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="p-3 font-mono text-[11px] text-slate-300">
                      {del.id.slice(0, 13)}...
                    </td>
                    <td className="p-3">
                      <span className="bg-slate-800 text-slate-300 px-2 py-0.5 rounded text-[10px] font-mono border border-slate-700">
                        {del.channel}
                      </span>
                    </td>
                    <td className="p-3">
                      <span
                        className={`text-[10px] font-mono px-2 py-0.5 rounded-full uppercase ${getStatusBadge(
                          del.status
                        )}`}
                      >
                        {del.status}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-slate-400 text-[11px]">
                      {del.recipient_id.slice(0, 8)}...
                    </td>
                    <td className="p-3 text-slate-400 font-mono">
                      {del.retry_count} / {del.max_retries}
                    </td>
                    <td className="p-3 text-slate-400 text-[11px]">
                      {new Date(del.created_at).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </td>
                    <td className="p-3 text-right space-x-2">
                      <button
                        onClick={() => setSelectedLog(del)}
                        className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 text-[11px] rounded border border-slate-700"
                      >
                        Inspect
                      </button>
                      {canRetry && (
                        <button
                          disabled={retryingId === del.id}
                          onClick={() => handleRetry(del.id)}
                          className="px-2 py-1 bg-orange-600/30 hover:bg-orange-600/50 text-orange-200 text-[11px] rounded border border-orange-500/40"
                        >
                          {retryingId === del.id ? 'Retrying...' : 'Retry'}
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Inspect Modal */}
      {selectedLog && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 max-w-lg w-full shadow-2xl space-y-4">
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <span>Delivery Audit Details</span>
              <span className={`text-xs px-2 py-0.5 rounded ${getStatusBadge(selectedLog.status)}`}>
                {selectedLog.status}
              </span>
            </h3>

            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-2 text-xs font-mono text-slate-300">
              <div>
                <span className="text-slate-500">ID:</span> {selectedLog.id}
              </div>
              <div>
                <span className="text-slate-500">Channel:</span> {selectedLog.channel}
              </div>
              <div>
                <span className="text-slate-500">Provider:</span> {selectedLog.provider || 'internal'}
              </div>
              <div>
                <span className="text-slate-500">Retry Count:</span> {selectedLog.retry_count} / {selectedLog.max_retries}
              </div>
              <div>
                <span className="text-slate-500">Sent At:</span> {selectedLog.sent_at || 'N/A'}
              </div>
              <div>
                <span className="text-slate-500">Delivered At:</span> {selectedLog.delivered_at || 'N/A'}
              </div>
              <div>
                <span className="text-slate-500">Failed At:</span> {selectedLog.failed_at || 'N/A'}
              </div>
              <div>
                <span className="text-slate-500">Error Payload:</span>
                <pre className="mt-1 bg-slate-900 p-2 rounded text-[11px] text-red-300 overflow-x-auto">
                  {JSON.stringify(selectedLog.error_details || {}, null, 2)}
                </pre>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setSelectedLog(null)}
                className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-lg"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
