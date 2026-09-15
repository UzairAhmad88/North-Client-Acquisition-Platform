'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { ProjectEstimate, getEstimates } from '@/lib/api/estimates';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function EstimatesPage() {
  const [estimates, setEstimates] = useState<ProjectEstimate[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<string>('ALL');

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const filter = activeTab === 'ALL' ? undefined : activeTab;
        const res = await getEstimates(filter);
        setEstimates(res);
      } catch (err) {
        console.error('Failed to load estimates:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [activeTab]);

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-zinc-100">
            Project Estimation & Commercial Intelligence
          </h1>
          <p className="text-xs text-slate-500 dark:text-zinc-400">
            Evaluate engineering effort, PERT three-point ranges, role allocations, labor/external costs, and recommended commercial ranges.
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 border-b border-slate-200 dark:border-zinc-800 pb-2">
        {['ALL', 'DRAFT', 'REVIEW', 'APPROVED', 'STALE'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold ${
              activeTab === tab
                ? 'bg-indigo-600 text-white'
                : 'bg-zinc-800/40 text-zinc-400 hover:bg-zinc-800'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="p-8 text-center text-xs text-zinc-400">Loading estimates...</div>
      ) : estimates.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-xs text-zinc-500">
            No estimates match the selected filter tab.
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {estimates.map((e) => (
            <Card key={e.id} className="hover:border-indigo-500/50 transition-colors">
              <CardContent className="p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-slate-900 dark:text-zinc-100">
                      Estimate #{e.id.slice(0, 8)}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-semibold">
                      v{e.version}
                    </span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded font-semibold ${
                        e.status === 'APPROVED'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                          : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/30'
                      }`}
                    >
                      {e.status}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-zinc-400">
                    <span>Hours: <strong className="text-slate-200">{e.estimated_hours}h</strong></span>
                    <span>Internal Cost: <strong className="text-amber-400">${e.internal_cost || 0}</strong></span>
                    <span>Recommended Range: <strong className="text-emerald-400">${e.recommended_min || 0} – ${e.recommended_max || 0}</strong></span>
                  </div>
                </div>

                <Link href={`/estimates/${e.id}`}>
                  <Button size="sm" variant="outline" className="text-xs">
                    Inspect Workspace →
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
