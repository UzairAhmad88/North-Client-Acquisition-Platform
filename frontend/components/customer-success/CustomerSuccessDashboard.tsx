'use client';

import React, { useState, useEffect } from 'react';
import { customerSuccessApi, ClientProfile, ClientRisk, ClientOpportunity, ClientRenewal } from '@/lib/api/customer_success';
import { Client360 } from './Client360';
import Link from 'next/link';

export function CustomerSuccessDashboard() {
  const [profiles, setProfiles] = useState<ClientProfile[]>([]);
  const [risks, setRisks] = useState<ClientRisk[]>([]);
  const [opportunities, setOpportunities] = useState<ClientOpportunity[]>([]);
  const [renewals, setRenewals] = useState<ClientRenewal[]>([]);
  const [selectedClientId, setSelectedClientId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadPortfolioData() {
      setIsLoading(true);
      try {
        const [profRes, riskRes, oppRes, renewRes] = await Promise.all([
          customerSuccessApi.listProfiles({ limit: 50 }),
          customerSuccessApi.listRisks({ status: 'OPEN' }),
          customerSuccessApi.listOpportunities(),
          customerSuccessApi.listRenewals(),
        ]);
        setProfiles(profRes || []);
        setRisks(riskRes || []);
        setOpportunities(oppRes || []);
        setRenewals(renewRes || []);
        if (profRes && profRes.length > 0) {
          setSelectedClientId(profRes[0].client_account_id || profRes[0].client_id || profRes[0].id);
        }
      } catch (err) {
        console.error('Failed to load customer success portfolio', err);
      } finally {
        setIsLoading(false);
      }
    }
    loadPortfolioData();
  }, []);

  const totalPipelineExpansion = opportunities.reduce(
    (acc, opp) => acc + parseFloat(opp.estimated_value || '0'),
    0
  );
  const totalRenewalValue = renewals.reduce(
    (acc, r) => acc + parseFloat(r.contract_value || r.estimated_renewal_value || '0'),
    0
  );

  return (
    <div className="space-y-6 text-slate-100">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <span>🤝</span> Client Relationship Intelligence & Customer Success
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Understand the client before recommending what to do next. Multi-factor health scoring, proactive risk matrix, and closed-loop renewals.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-sm font-medium border border-slate-700 transition"
          >
            Refresh Telemetry
          </button>
        </div>
      </div>

      {/* High-Level Portfolio KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Client Portfolio</span>
          <div className="text-2xl font-bold text-white mt-2">{profiles.length}</div>
          <span className="text-xs text-slate-500 mt-1 block">Tracked relationships</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs font-semibold text-rose-400 uppercase tracking-wider">Identified Open Risks</span>
          <div className="text-2xl font-bold text-rose-400 mt-2">{risks.length}</div>
          <span className="text-xs text-slate-500 mt-1 block">Telemetry & churn signals</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">Expansion Pipeline</span>
          <div className="text-2xl font-bold text-emerald-400 mt-2">
            ${totalPipelineExpansion.toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </div>
          <span className="text-xs text-slate-500 mt-1 block">{opportunities.length} active opportunities</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs font-semibold text-purple-400 uppercase tracking-wider">Renewals Under Window</span>
          <div className="text-2xl font-bold text-purple-400 mt-2">
            ${totalRenewalValue.toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </div>
          <span className="text-xs text-slate-500 mt-1 block">{renewals.length} upcoming contracts</span>
        </div>
      </div>

      {/* Main Workspace Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Column: Client Selector List */}
        <div className="lg:col-span-1 bg-slate-900 border border-slate-800 p-4 rounded-2xl space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Clients</h3>
            <span className="text-xs text-slate-500 font-mono">{profiles.length} total</span>
          </div>

          <div className="space-y-1.5 max-h-[600px] overflow-y-auto pr-1">
            {profiles.map((p) => {
              const cid = p.client_account_id || p.client_id || p.id;
              const isSelected = selectedClientId === cid;
              return (
                <button
                  key={p.id}
                  onClick={() => setSelectedClientId(cid)}
                  className={`w-full text-left p-3 rounded-xl transition border ${
                    isSelected
                      ? 'bg-indigo-600/15 border-indigo-500/40 text-white'
                      : 'bg-slate-950/40 border-slate-800/40 text-slate-300 hover:border-slate-700'
                  }`}
                >
                  <div className="font-semibold text-sm truncate">{p.business_name || p.company_name || 'Organization'}</div>
                  <div className="flex items-center justify-between text-[11px] text-slate-400 mt-1">
                    <span className="capitalize">{p.lifecycle_stage.toLowerCase()}</span>
                    <span className="text-emerald-400 font-medium">{p.relationship_strength}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Interactive Client 360 Dossier */}
        <div className="lg:col-span-3">
          {selectedClientId ? (
            <Client360 clientId={selectedClientId} />
          ) : (
            <div className="p-12 text-center text-slate-500 bg-slate-900 border border-slate-800 rounded-2xl">
              Select a client to inspect their unified relationship dossier.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
