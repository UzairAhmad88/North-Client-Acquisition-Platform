'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { DiscoverySession, getDiscoverySessions } from '@/lib/api/requirements';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function DiscoveryRequirementsPage() {
  const [sessions, setSessions] = useState<DiscoverySession[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<string>('ALL');

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const filter = activeTab === 'ALL' ? undefined : activeTab;
        const res = await getDiscoverySessions(filter);
        setSessions(res);
      } catch (err) {
        console.error('Failed to load discovery sessions:', err);
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
            Client Requirements & Discovery Command Center
          </h1>
          <p className="text-xs text-slate-500 dark:text-zinc-400">
            Transform client conversations into structured, evidence-backed requirements, questions, and project scope.
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 border-b border-slate-200 dark:border-zinc-800 pb-2">
        {['ALL', 'OPEN', 'IN_PROGRESS', 'READY_FOR_REVIEW', 'CONFIRMED'].map((tab) => (
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
        <div className="p-8 text-center text-xs text-zinc-400">Loading discovery sessions...</div>
      ) : sessions.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-xs text-zinc-500">
            No discovery sessions match the selected filter tab.
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {sessions.map((s) => (
            <Card key={s.id} className="hover:border-indigo-500/50 transition-colors">
              <CardContent className="p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-slate-900 dark:text-zinc-100">
                      Discovery Session #{s.id.slice(0, 8)}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-semibold">
                      v{s.version}
                    </span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded font-semibold ${
                        s.status === 'CONFIRMED'
                          ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                          : 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/30'
                      }`}
                    >
                      {s.status}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-zinc-400">
                    <span>
                      Readiness: <strong className="text-emerald-400">{s.readiness_stage} ({s.readiness_score}%)</strong>
                    </span>
                    <span>
                      Completeness: <strong className="text-blue-400">{s.completeness_score}%</strong>
                    </span>
                    <span>
                      Complexity: <strong className="text-amber-400">{s.scope_complexity}</strong>
                    </span>
                  </div>
                </div>

                <Link href={`/requirements/${s.id}`}>
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
