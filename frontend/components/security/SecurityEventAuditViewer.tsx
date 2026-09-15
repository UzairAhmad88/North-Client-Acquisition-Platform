'use client';

import React, { useState, useEffect } from 'react';
import { History, Shield, AlertOctagon, CheckCircle2, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';
import { securityApi, SecurityEventItem } from '@/lib/api/security';

interface Props {
  limit?: number;
  compact?: boolean;
}

export default function SecurityEventAuditViewer({ limit = 50, compact = false }: Props) {
  const [events, setEvents] = useState<SecurityEventItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      const res = await securityApi.listEvents(limit);
      if (res) {
        setEvents(res);
      }
    } catch (err) {
      console.error('Failed to load security audit events', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [limit]);

  return (
    <div className="space-y-4">
      {!compact && (
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white">Security Event Audit Trail</h3>
            <p className="text-xs text-slate-400">
              Immutable chronological record of authentication and authorization evaluations.
            </p>
          </div>

          <button
            onClick={fetchEvents}
            className="p-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-xl text-slate-400 hover:text-slate-200 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-emerald-400' : ''}`} />
          </button>
        </div>
      )}

      <div className="space-y-2">
        {events.length === 0 ? (
          <div className="p-6 text-center text-slate-500 text-xs bg-slate-950/40 rounded-xl border border-slate-800">
            {loading ? 'Loading audit records...' : 'No security events recorded yet.'}
          </div>
        ) : (
          events.map((e) => {
            const isExpanded = expandedId === e.id;
            const isDeny = e.result === 'DENY' || e.result === 'BLOCK';

            return (
              <div
                key={e.id}
                className={`rounded-xl border transition-all ${
                  isDeny
                    ? 'bg-rose-950/10 border-rose-500/20'
                    : 'bg-slate-900/60 border-slate-800/80 hover:border-slate-700'
                }`}
              >
                <div
                  onClick={() => setExpandedId(isExpanded ? null : e.id)}
                  className="p-3.5 flex items-center justify-between cursor-pointer"
                >
                  <div className="flex items-center space-x-3">
                    <div
                      className={`p-2 rounded-lg ${
                        isDeny
                          ? 'bg-rose-500/10 text-rose-400'
                          : 'bg-emerald-500/10 text-emerald-400'
                      }`}
                    >
                      {isDeny ? <AlertOctagon className="w-4 h-4" /> : <Shield className="w-4 h-4" />}
                    </div>

                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="font-mono text-xs font-bold text-white">{e.event_type}</span>
                        <span
                          className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                            e.severity === 'HIGH' || e.severity === 'CRITICAL'
                              ? 'bg-rose-500/10 text-rose-400'
                              : 'bg-slate-800 text-slate-400'
                          }`}
                        >
                          {e.severity}
                        </span>
                      </div>
                      <div className="text-[11px] text-slate-400 mt-0.5">
                        Principal: <span className="font-mono text-slate-300">{e.principal_id.slice(0, 16)}</span>
                        {e.action ? ` • Action: ${e.action}` : ''}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3 text-right">
                    <div>
                      <span
                        className={`text-xs font-bold ${
                          isDeny ? 'text-rose-400' : 'text-emerald-400'
                        }`}
                      >
                        {e.result}
                      </span>
                      <div className="text-[10px] text-slate-500">
                        {new Date(e.occurred_at).toLocaleTimeString()}
                      </div>
                    </div>
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-slate-400" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-slate-400" />
                    )}
                  </div>
                </div>

                {isExpanded && (
                  <div className="px-4 pb-4 pt-1 border-t border-slate-800/60 text-xs space-y-2">
                    <div className="grid grid-cols-2 gap-2 text-slate-400 pt-2">
                      <div>
                        Reason Code: <span className="text-white font-mono">{e.reason_code}</span>
                      </div>
                      <div>
                        Tenant ID: <span className="text-white font-mono">{e.tenant_id}</span>
                      </div>
                    </div>

                    {e.details && Object.keys(e.details).length > 0 && (
                      <div className="mt-2">
                        <div className="text-[11px] font-semibold text-slate-400 uppercase mb-1">
                          Event Details
                        </div>
                        <pre className="p-2.5 bg-slate-950 rounded-lg text-[11px] text-slate-300 font-mono overflow-x-auto border border-slate-800">
                          {JSON.stringify(e.details, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
