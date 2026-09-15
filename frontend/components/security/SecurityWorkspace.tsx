'use client';

import React, { useState, useEffect } from 'react';
import {
  Shield,
  Users,
  Key,
  Lock,
  History,
  AlertTriangle,
  FileText,
  Activity,
  CheckCircle2,
  RefreshCw
} from 'lucide-react';
import { securityApi, SecurityMetrics } from '@/lib/api/security';
import UserManagement from './UserManagement';
import RoleManagement from './RoleManagement';
import SessionManager from './SessionManager';
import APIKeyManager from './APIKeyManager';
import SecurityEventAuditViewer from './SecurityEventAuditViewer';
import MFAPolicyControl from './MFAPolicyControl';

type SecurityTab = 'overview' | 'users' | 'roles' | 'sessions' | 'api-keys' | 'mfa' | 'audit';

export default function SecurityWorkspace() {
  const [activeTab, setActiveTab] = useState<SecurityTab>('overview');
  const [metrics, setMetrics] = useState<SecurityMetrics | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      const res = await securityApi.getMetrics();
      if (res) {
        setMetrics(res);
      }
    } catch (err) {
      console.error('Failed to load security metrics', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
            <Shield className="w-8 h-8" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Security & Identity Control Plane</h1>
            <p className="text-sm text-slate-400">
              Centralized RBAC, ABAC, Session Isolation, MFA, Scoped API Keys & Immutable Audit Trail
            </p>
          </div>
        </div>

        <button
          onClick={fetchMetrics}
          className="flex items-center space-x-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-sm font-medium transition-colors border border-slate-700"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-emerald-400' : ''}`} />
          <span>Refresh Metrics</span>
        </button>
      </div>

      {/* KPI Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Sessions</span>
            <Activity className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="mt-2 text-2xl font-bold text-white">
            {metrics ? metrics.active_sessions_count : '--'}
          </div>
          <span className="text-xs text-slate-500">Live authenticated tokens</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Users</span>
            <Users className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="mt-2 text-2xl font-bold text-white">
            {metrics ? metrics.users_count : '--'}
          </div>
          <span className="text-xs text-slate-500">Internal & client accounts</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Security Events (24h)</span>
            <History className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="mt-2 text-2xl font-bold text-white">
            {metrics ? metrics.security_events_last_24h : '--'}
          </div>
          <span className="text-xs text-slate-500">Audit decisions logged</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active API Keys</span>
            <Key className="w-5 h-5 text-amber-400" />
          </div>
          <div className="mt-2 text-2xl font-bold text-white">
            {metrics ? metrics.api_keys_active_count : '--'}
          </div>
          <span className="text-xs text-slate-500">Scoped integration secrets</span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 overflow-x-auto space-x-2">
        <button
          onClick={() => setActiveTab('overview')}
          className={`flex items-center space-x-2 px-4 py-3 border-b-2 text-sm font-medium transition-colors whitespace-nowrap ${
            activeTab === 'overview'
              ? 'border-emerald-500 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Shield className="w-4 h-4" />
          <span>Overview</span>
        </button>

        <button
          onClick={() => setActiveTab('users')}
          className={`flex items-center space-x-2 px-4 py-3 border-b-2 text-sm font-medium transition-colors whitespace-nowrap ${
            activeTab === 'users'
              ? 'border-emerald-500 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Users className="w-4 h-4" />
          <span>User Directory</span>
        </button>

        <button
          onClick={() => setActiveTab('roles')}
          className={`flex items-center space-x-2 px-4 py-3 border-b-2 text-sm font-medium transition-colors whitespace-nowrap ${
            activeTab === 'roles'
              ? 'border-emerald-500 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Lock className="w-4 h-4" />
          <span>Roles & Permissions</span>
        </button>

        <button
          onClick={() => setActiveTab('sessions')}
          className={`flex items-center space-x-2 px-4 py-3 border-b-2 text-sm font-medium transition-colors whitespace-nowrap ${
            activeTab === 'sessions'
              ? 'border-emerald-500 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Activity className="w-4 h-4" />
          <span>Active Sessions</span>
        </button>

        <button
          onClick={() => setActiveTab('api-keys')}
          className={`flex items-center space-x-2 px-4 py-3 border-b-2 text-sm font-medium transition-colors whitespace-nowrap ${
            activeTab === 'api-keys'
              ? 'border-emerald-500 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Key className="w-4 h-4" />
          <span>API Keys</span>
        </button>

        <button
          onClick={() => setActiveTab('mfa')}
          className={`flex items-center space-x-2 px-4 py-3 border-b-2 text-sm font-medium transition-colors whitespace-nowrap ${
            activeTab === 'mfa'
              ? 'border-emerald-500 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <CheckCircle2 className="w-4 h-4" />
          <span>MFA & Step-Up</span>
        </button>

        <button
          onClick={() => setActiveTab('audit')}
          className={`flex items-center space-x-2 px-4 py-3 border-b-2 text-sm font-medium transition-colors whitespace-nowrap ${
            activeTab === 'audit'
              ? 'border-emerald-500 text-emerald-400'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <History className="w-4 h-4" />
          <span>Security Audit Trail</span>
        </button>
      </div>

      {/* Tab Panels */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl space-y-4">
            <h3 className="text-lg font-semibold text-white">Security Architecture Principles</h3>
            <div className="space-y-3 text-sm text-slate-300">
              <div className="flex items-start space-x-3 p-3 bg-slate-950/60 rounded-xl border border-slate-800">
                <Shield className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-medium text-white">Default Deny Policy</div>
                  <div className="text-xs text-slate-400 mt-0.5">
                    Every operation is denied unless explicitly permitted by an authorized RBAC role, project assignment, or policy gate.
                  </div>
                </div>
              </div>

              <div className="flex items-start space-x-3 p-3 bg-slate-950/60 rounded-xl border border-slate-800">
                <Lock className="w-5 h-5 text-cyan-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-medium text-white">Client vs Internal Isolation Boundary</div>
                  <div className="text-xs text-slate-400 mt-0.5">
                    Client accounts can never access internal cost estimates, AI execution traces, or internal discussions.
                  </div>
                </div>
              </div>

              <div className="flex items-start space-x-3 p-3 bg-slate-950/60 rounded-xl border border-slate-800">
                <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-medium text-white">High-Risk Step-Up & Dual Control</div>
                  <div className="text-xs text-slate-400 mt-0.5">
                    Critical actions (Contract Signing, Commercial Price Changes, AI Model Promotions) require recent MFA step-up re-authentication.
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
            <h3 className="text-lg font-semibold text-white mb-4">Quick Audit Summary</h3>
            <SecurityEventAuditViewer limit={5} compact={true} />
          </div>
        </div>
      )}

      {activeTab === 'users' && <UserManagement />}
      {activeTab === 'roles' && <RoleManagement />}
      {activeTab === 'sessions' && <SessionManager />}
      {activeTab === 'api-keys' && <APIKeyManager />}
      {activeTab === 'mfa' && <MFAPolicyControl />}
      {activeTab === 'audit' && <SecurityEventAuditViewer limit={50} />}
    </div>
  );
}
