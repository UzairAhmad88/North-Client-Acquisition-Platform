'use client';

import React from 'react';
import { Tag, ShieldAlert, CheckCircle2, DollarSign, Scale } from 'lucide-react';
import { PricingTierItem, DiscountRequestItem } from '../../lib/api/revenueGrowth';

interface PricingDiscountManagerProps {
  pricingTiers: PricingTierItem[];
  discounts: DiscountRequestItem[];
}

export const PricingDiscountManager: React.FC<PricingDiscountManagerProps> = ({ pricingTiers, discounts }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
          <Tag className="h-4 w-4 text-emerald-400" />
          Pricing Tiers & Discount Governance
        </h3>
        <span className="text-xs text-slate-400 font-mono">Pending Approvals: {discounts.filter(d => d.status === 'pending_approval').length}</span>
      </div>

      <div className="space-y-3">
        <div className="text-xs font-semibold text-slate-300">Active Pricing Tiers</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {pricingTiers.map((prc) => (
            <div key={prc.id} className="p-3 rounded-lg border border-slate-800 bg-slate-800/40 space-y-1">
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold text-slate-100">{prc.tier_name}</span>
                <span className="text-xs font-mono text-emerald-400 font-bold">
                  ${prc.list_price_usd.toLocaleString()}/yr
                </span>
              </div>
              <div className="text-[11px] text-slate-400 flex justify-between pt-1 border-t border-slate-800/60">
                <span>Target Margin: {prc.target_gross_margin_pct}%</span>
                <span>Avg Discount: {prc.average_discount_pct}%</span>
              </div>
            </div>
          ))}
        </div>

        {discounts.length > 0 && (
          <div className="space-y-2 pt-2">
            <div className="text-xs font-semibold text-slate-300">Discount Governance Requests</div>
            {discounts.map((dsc) => (
              <div key={dsc.id} className="p-3 rounded-lg border border-amber-500/20 bg-amber-500/5 space-y-1.5">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-semibold text-slate-200">
                    Requested Discount: <span className="text-amber-400 font-mono">{dsc.requested_discount_pct}%</span>
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase font-semibold">
                    {dsc.status.replace('_', ' ')}
                  </span>
                </div>
                <p className="text-xs text-slate-300">{dsc.justification}</p>
                <div className="flex justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800/60 font-mono">
                  <span>Orig: ${dsc.original_price_usd.toLocaleString()}</span>
                  <span className="text-emerald-400 font-bold">Prop: ${dsc.proposed_price_usd.toLocaleString()}</span>
                  <span>Margin Delta: -{dsc.margin_impact_pct}%</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
