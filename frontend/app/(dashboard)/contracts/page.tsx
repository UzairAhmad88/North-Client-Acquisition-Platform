'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Contract, getContracts } from '@/lib/api/contracts';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function ContractsPage() {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<string>('ALL');

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const filter = activeTab === 'ALL' ? undefined : activeTab;
        const res = await getContracts(filter);
        setContracts(res);
      } catch (err) {
        console.error('Failed to load contracts:', err);
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
            Contract & Scope Commitment Intelligence
          </h1>
          <p className="text-xs text-slate-500 dark:text-zinc-400">
            Manage technical services agreements, internal operator approvals, explicit client acceptance, and locked project baselines.
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 border-b border-slate-200 dark:border-zinc-800 pb-2">
        {['ALL', 'DRAFT', 'READY_FOR_CLIENT', 'CLIENT_APPROVED', 'SIGNED', 'ACTIVE'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold ${
              activeTab === tab
                ? 'bg-indigo-600 text-white'
                : 'bg-zinc-800/40 text-zinc-400 hover:bg-zinc-800'
            }`}
          >
            {tab.replace(/_/g, ' ')}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="p-8 text-center text-xs text-zinc-400">Loading contracts...</div>
      ) : contracts.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-xs text-zinc-500">
            No contracts match the selected filter tab.
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {contracts.map((c) => (
            <Card key={c.id} className="hover:border-indigo-500/50 transition-colors">
              <CardContent className="p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-slate-900 dark:text-zinc-100">
                      {c.title}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-semibold">
                      v{c.version}
                    </span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded font-semibold ${
                        c.status === 'ACTIVE' || c.status === 'SIGNED'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                          : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/30'
                      }`}
                    >
                      {c.status}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-zinc-400">
                    <span>Contract #: <strong className="text-slate-200">{c.contract_number}</strong></span>
                    <span>Pricing Status: <strong className="text-amber-400">{c.pricing_status}</strong></span>
                  </div>
                </div>

                <Link href={`/contracts/${c.id}`}>
                  <Button size="sm" variant="outline" className="text-xs">
                    Inspect Contract →
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
