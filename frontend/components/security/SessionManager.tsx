'use client';

import React, { useState, useEffect } from 'react';
import { Activity, ShieldAlert, Laptop, Clock, RefreshCw, XCircle } from 'lucide-react';
import { securityApi, UserSession } from '@/lib/api/security';

export default function SessionManager() {
  const [sessions, setSessions] = useState<UserSession[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchSessions = async () => {
    try {
      setLoading(true);
      const res = await securityApi.listSessions();
      if (res) {
        setSessions(res);
      }
    } catch (err) {
      console.error('Failed to load sessions', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  const handleRevoke = async (sessionId: string) => {
    try {
      await securityApi.revokeSession(sessionId);
      fetchSessions();
    } catch (err) {
      console.error('Failed to revoke session', err);
    }
  };

  const handleRevokeAll = async () => {
    try {
      await securityApi.revokeAllSessions();
      fetchSessions();
    } catch (err) {
      console.error('Failed to revoke all sessions', err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Controls Bar */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white">Active Authenticated Sessions</h3>
          <p className="text-xs text-slate-400">
            Live JWT access tokens, device metadata, and instant revocation controls.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={fetchSessions}
            className="p-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-xl text-slate-400 hover:text-slate-200 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-emerald-400' : ''}`} />
          </button>

          <button
            onClick={handleRevokeAll}
            className="px-4 py-2 bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30 rounded-xl text-xs font-semibold transition-colors"
          >
            Revoke All Other Sessions
          </button>
        </div>
      </div>

      {/* Sessions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sessions.map((s) => (
          <div
            key={s.id}
            className={`p-5 rounded-2xl border transition-all ${
              s.is_revoked
                ? 'bg-slate-950/40 border-slate-800/40 opacity-50'
                : 'bg-slate-900 border-slate-800'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 bg-slate-800 rounded-xl text-slate-300">
                  <Laptop className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-sm font-semibold text-white">
                    {s.user_agent ? s.user_agent.slice(0, 32) + '...' : 'Browser Client'}
                  </div>
                  <div className="text-xs text-slate-400 font-mono">
                    IP: {s.ip_address || '127.0.0.1'}
                  </div>
                </div>
              </div>

              {!s.is_revoked ? (
                <button
                  onClick={() => handleRevoke(s.id)}
                  className="px-2.5 py-1 text-xs font-medium text-rose-400 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/20 rounded-lg transition-colors"
                >
                  Revoke
                </button>
              ) : (
                <span className="text-[11px] font-bold text-slate-500 uppercase">Revoked</span>
              )}
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800/60 grid grid-cols-2 gap-2 text-xs text-slate-400">
              <div className="flex items-center space-x-1.5">
                <Clock className="w-3.5 h-3.5 text-slate-500" />
                <span>Last Seen: {new Date(s.last_seen_at).toLocaleTimeString()}</span>
              </div>
              <div className="text-right">
                <span>Expires: {new Date(s.expires_at).toLocaleDateString()}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
