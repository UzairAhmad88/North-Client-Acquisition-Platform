'use client';

import React from 'react';
import { UserCheck, Bot, Database, Settings, Plug, DollarSign } from 'lucide-react';

interface SecurityHealthProps {
  domainBreakdown: {
    identity: number;
    ai: number;
    data: number;
    configuration: number;
    integrations: number;
    financial: number;
  };
}

export default function SecurityHealth({ domainBreakdown }: SecurityHealthProps) {
  const domains = [
    {
      name: 'Identity & Auth',
      key: 'identity',
      score: domainBreakdown.identity,
      icon: UserCheck,
      description: 'Credential stuffing, brute-force, and session anomalies',
    },
    {
      name: 'AI & Autonomous Agents',
      key: 'ai',
      score: domainBreakdown.ai,
      icon: Bot,
      description: 'Prompt injections, tool authorization, runaway loops',
    },
    {
      name: 'Data Access & Isolation',
      key: 'data',
      score: domainBreakdown.data,
      icon: Database,
      description: 'Bulk exports, exfiltration, and cross-tenant violations',
    },
    {
      name: 'Configuration & RBAC',
      key: 'configuration',
      score: domainBreakdown.configuration,
      icon: Settings,
      description: 'Privilege escalation, kill switches, and policy tampering',
    },
    {
      name: 'API & Integrations',
      key: 'integrations',
      score: domainBreakdown.integrations,
      icon: Plug,
      description: 'Third-party providers, token leaks, and rate abuse',
    },
    {
      name: 'Financial Security',
      key: 'financial',
      score: domainBreakdown.financial,
      icon: DollarSign,
      description: 'Duplicate payments, refund anomalies, and fraud signals',
    },
  ];

  const getStatusColor = (score: number) => {
    if (score >= 70) return { bar: 'bg-rose-500', text: 'text-rose-600', badge: 'bg-rose-50 text-rose-700 border-rose-200' };
    if (score >= 40) return { bar: 'bg-amber-500', text: 'text-amber-600', badge: 'bg-amber-50 text-amber-700 border-amber-200' };
    return { bar: 'bg-emerald-500', text: 'text-emerald-600', badge: 'bg-emerald-50 text-emerald-700 border-emerald-200' };
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900">Security Domain Health & Risk Exposure</h3>
          <p className="text-xs text-slate-500">Real-time threat level across 6 platform security vectors</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
        {domains.map((dom) => {
          const colors = getStatusColor(dom.score);
          const Icon = dom.icon;
          return (
            <div key={dom.key} className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 hover:bg-slate-50 transition-colors">
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-lg bg-white border border-slate-200 text-slate-700 shadow-xs">
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-slate-900">{dom.name}</h4>
                    <span className="text-xs text-slate-400">Risk index</span>
                  </div>
                </div>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${colors.badge}`}>
                  {dom.score} / 100
                </span>
              </div>

              <div className="w-full bg-slate-200 rounded-full h-2 mt-3 overflow-hidden">
                <div
                  className={`h-2 rounded-full transition-all duration-500 ${colors.bar}`}
                  style={{ width: `${Math.max(5, dom.score)}%` }}
                />
              </div>

              <p className="text-xs text-slate-500 mt-2.5 line-clamp-1">{dom.description}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
