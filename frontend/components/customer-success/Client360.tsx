'use client';

import React, { useState, useEffect } from 'react';
import { customerSuccessApi, Client360Dossier } from '@/lib/api/customer_success';
import { ClientHealthBreakdown } from './ClientHealthBreakdown';
import { ClientTimeline } from './ClientTimeline';
import { ClientRisks } from './ClientRisks';
import { ClientOpportunities } from './ClientOpportunities';
import { RenewalTable } from './RenewalTable';

interface Client360Props {
  clientId: string;
}

export function Client360({ clientId }: Client360Props) {
  const [dossier, setDossier] = useState<Client360Dossier | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'timeline' | 'risks' | 'renewals'>('overview');

  useEffect(() => {
    async function load360() {
      setIsLoading(true);
      try {
        const res = await customerSuccessApi.getClient360(clientId);
        setDossier(res);
      } catch (err) {
        console.error('Failed to load client 360 view', err);
      } finally {
        setIsLoading(false);
      }
    }
    if (clientId) {
      load360();
    }
  }, [clientId]);

  if (isLoading) {
    return (
      <div className="p-12 text-center text-slate-500 bg-slate-900 border border-slate-800 rounded-2xl">
        Loading comprehensive Client 360 Dossier...
      </div>
    );
  }

  if (!dossier) {
    return (
      <div className="p-8 text-center text-slate-500 bg-slate-900 border border-slate-800 rounded-2xl">
        No Client 360 data available.
      </div>
    );
  }

  const profile = dossier.profile;

  return (
    <div className="space-y-6 text-slate-100">
      {/* Client Header Card */}
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-2xl font-extrabold text-white">{profile?.business_name || profile?.company_name || 'Client Profile'}</h2>
            <span className="px-3 py-1 bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 rounded-full text-xs font-semibold uppercase">
              {profile?.lifecycle_stage || 'ACTIVE'}
            </span>
          </div>
          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 mt-2">
            <span>Tier: <strong className="text-slate-200">{profile?.strategic_tier || 'STANDARD'}</strong></span>
            <span>Strength: <strong className="text-emerald-400">{profile?.relationship_strength || 'ESTABLISHED'}</strong></span>
            <span>Cadence: <strong className="text-slate-200">{profile?.communication_cadence || 'BI_WEEKLY'}</strong></span>
            <span>Timezone: <strong className="text-slate-200">{profile?.client_timezone || 'UTC'}</strong></span>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'overview' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            360 Overview
          </button>
          <button
            onClick={() => setActiveTab('timeline')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'timeline' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Activity Stream
          </button>
          <button
            onClick={() => setActiveTab('risks')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'risks' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Risks & Opps
          </button>
          <button
            onClick={() => setActiveTab('renewals')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'renewals' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            Renewals
          </button>
        </div>
      </div>

      {/* Tab Panels */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <ClientHealthBreakdown healthScore={dossier.latest_health} />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ClientRisks risks={dossier.active_risks || []} />
            <ClientOpportunities opportunities={dossier.opportunities || []} />
          </div>
          <RenewalTable renewals={dossier.upcoming_renewals || []} />
        </div>
      )}

      {activeTab === 'timeline' && (
        <ClientTimeline events={dossier.recent_timeline || []} />
      )}

      {activeTab === 'risks' && (
        <div className="space-y-6">
          <ClientRisks risks={dossier.active_risks || []} />
          <ClientOpportunities opportunities={dossier.opportunities || []} />
        </div>
      )}

      {activeTab === 'renewals' && (
        <RenewalTable renewals={dossier.upcoming_renewals || []} />
      )}
    </div>
  );
}
