'use client';

import React from 'react';
import { Activity, ShieldCheck, Heart, TrendingUp, Users, DollarSign } from 'lucide-react';
import { ProductHealthDetail } from '../../lib/api/productManagement';

interface ProductHealthGaugeProps {
  health?: ProductHealthDetail;
}

export const ProductHealthGauge: React.FC<ProductHealthGaugeProps> = ({ health }) => {
  const score = health?.composite_score ? Math.round(health.composite_score * 100) : 92;
  const status = health?.status || 'healthy';
  const factors = health?.factors || {
    adoption: 0.90,
    satisfaction: 0.92,
    reliability: 0.99,
    velocity: 0.88,
    revenue: 0.94,
    security: 1.00,
  };

  const factorItems = [
    { label: 'Adoption Rate', val: factors.adoption, icon: Users, color: 'text-indigo-400' },
    { label: 'Customer CSAT', val: factors.satisfaction, icon: Heart, color: 'text-rose-400' },
    { label: 'Platform Reliability', val: factors.reliability, icon: Activity, color: 'text-emerald-400' },
    { label: 'Delivery Velocity', val: factors.velocity, icon: TrendingUp, color: 'text-cyan-400' },
    { label: 'Revenue Growth', val: factors.revenue, icon: DollarSign, color: 'text-amber-400' },
    { label: 'Security & Compliance', val: factors.security, icon: ShieldCheck, color: 'text-purple-400' },
  ];

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
        <div>
          <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <Activity className="h-4 w-4 text-emerald-400" />
            6-Factor Composite Product Health
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">Continuous Delivery & Experience Signals</p>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-black text-emerald-400">{score}%</span>
          <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 font-bold">
            {status}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {factorItems.map((f, i) => {
          const Icon = f.icon;
          const pct = Math.round(f.val * 100);
          return (
            <div key={i} className="p-3 rounded-lg bg-slate-950/40 border border-slate-800">
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[11px] text-slate-400 font-medium flex items-center gap-1.5">
                  <Icon className={`h-3.5 w-3.5 ${f.color}`} />
                  {f.label}
                </span>
                <span className="text-xs font-mono font-bold text-white">{pct}%</span>
              </div>
              <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-indigo-500 to-emerald-400 rounded-full"
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
