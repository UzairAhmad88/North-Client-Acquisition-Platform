'use client';

import React from 'react';
import { User, Building2, ShieldCheck, HeartHandshake, DollarSign, Calendar, TrendingUp } from 'lucide-react';
import { Customer360Profile as Customer360Type } from '../../lib/api/customerExperience';

interface Customer360ProfileProps {
  profile: Customer360Type;
}

export const Customer360Profile: React.FC<Customer360ProfileProps> = ({ profile }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-semibold">
            {profile.identity.segment}
          </span>
          <h2 className="text-base font-bold text-white mt-1 flex items-center gap-2">
            <Building2 className="h-5 w-5 text-indigo-400" />
            {profile.identity.name}
          </h2>
          <p className="text-xs text-slate-400 font-mono">Customer ID: {profile.customer_id}</p>
        </div>
        <div className="text-right">
          <div className="text-xs text-slate-400">Current ARR</div>
          <div className="text-lg font-bold text-emerald-400 font-mono">
            ${profile.organization.arr.toLocaleString()}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2">
        <div className="p-3 rounded-lg bg-slate-800/40 border border-slate-800/60">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
            <User className="h-3.5 w-3.5 text-blue-400" />
            Account Exec
          </div>
          <div className="text-xs font-semibold text-slate-200">{profile.identity.account_executive}</div>
        </div>

        <div className="p-3 rounded-lg bg-slate-800/40 border border-slate-800/60">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
            <HeartHandshake className="h-3.5 w-3.5 text-purple-400" />
            Lead CSM
          </div>
          <div className="text-xs font-semibold text-slate-200">{profile.identity.customer_success_manager}</div>
        </div>

        <div className="p-3 rounded-lg bg-slate-800/40 border border-slate-800/60">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
            <Calendar className="h-3.5 w-3.5 text-amber-400" />
            Renewal Date
          </div>
          <div className="text-xs font-semibold text-slate-200">{profile.organization.contract_renewal_date}</div>
        </div>

        <div className="p-3 rounded-lg bg-slate-800/40 border border-slate-800/60">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
            <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
            Governance Status
          </div>
          <div className="text-xs font-semibold text-emerald-400">Verified Compliant</div>
        </div>
      </div>
    </div>
  );
};
