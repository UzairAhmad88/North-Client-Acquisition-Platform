'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { ConversationDetail, getConversations } from '@/lib/api/conversations';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<ConversationDetail[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<string>('ALL');

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const filter = activeTab === 'ALL' ? undefined : activeTab;
        const res = await getConversations(filter);
        setConversations(res);
      } catch (err) {
        console.error('Failed to load conversations:', err);
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
          <h1 className="text-xl font-bold text-slate-900 dark:text-zinc-100">Conversation Command Center</h1>
          <p className="text-xs text-slate-500 dark:text-zinc-400">
            Monitor client responses, intent signals, objections, and next action recommendations.
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 border-b border-slate-200 dark:border-zinc-800 pb-2">
        {['ALL', 'ACTIVE', 'OPTED_OUT', 'CLOSED'].map((tab) => (
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
        <div className="p-8 text-center text-xs text-zinc-400">Loading conversations...</div>
      ) : conversations.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-xs text-zinc-500">
            No conversations match the selected filter tab.
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {conversations.map((c) => (
            <Card key={c.id} className="hover:border-indigo-500/50 transition-colors">
              <CardContent className="p-4 flex items-center justify-between">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-slate-900 dark:text-zinc-100">
                      Conversation #{c.id.slice(0, 8)}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-semibold">
                      {c.channel}
                    </span>
                    <span className={`text-[10px] px-2 py-0.5 rounded font-semibold ${
                      c.status === 'OPTED_OUT' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/30' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                    }`}>
                      {c.status}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-zinc-400">
                    <span>Intent: <strong className="text-emerald-400">{c.current_intent || 'AMBIGUOUS'}</strong></span>
                    <span>Stage: <strong className="text-indigo-400">{c.conversation_stage}</strong></span>
                    <span>Next Action: <strong className="text-amber-400">{c.next_action || 'ESCALATE_TO_HUMAN'}</strong></span>
                  </div>
                </div>

                <Link href={`/conversations/${c.id}`}>
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
