'use client';

import React, { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { analyzeConversation, ConversationDetail, getConversationDetail } from '@/lib/api/conversations';
import { MessageTimeline } from '@/components/conversations/MessageTimeline';
import { IntelligenceCard } from '@/components/conversations/IntelligenceCard';
import { ResponseDraftEditor } from '@/components/conversations/ResponseDraftEditor';
import { Button } from '@/components/ui/button';

export default function ConversationWorkspacePage() {
  const params = useParams();
  const conversationId = params.id as string;

  const [conversation, setConversation] = useState<ConversationDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDetail = useCallback(async () => {
    if (!conversationId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await getConversationDetail(conversationId);
      setConversation(res);
    } catch (err: any) {
      setError(err.message || 'Failed to load conversation details.');
    } finally {
      setLoading(false);
    }
  }, [conversationId]);

  useEffect(() => {
    fetchDetail();
  }, [fetchDetail]);

  const handleRunAnalysis = async () => {
    setAnalyzing(true);
    try {
      await analyzeConversation(conversationId);
      fetchDetail();
    } catch (err: any) {
      setError(err.message || 'Failed to analyze conversation.');
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-xs text-zinc-400">Loading conversation workspace...</div>;
  }

  if (error || !conversation) {
    return (
      <div className="p-6 space-y-4">
        <Link href="/conversations" className="text-xs text-indigo-400 hover:underline">← Back to Conversations</Link>
        <div className="p-4 rounded-xl bg-rose-50 text-rose-700 text-xs border border-rose-200">{error || 'Conversation not found.'}</div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center pb-4 border-b border-zinc-800">
        <div>
          <Link href="/conversations" className="text-xs text-indigo-400 hover:underline block mb-1">← Back to Directory</Link>
          <h1 className="text-xl font-bold text-zinc-100 flex items-center gap-2">
            Conversation Workspace #{conversation.id.slice(0, 8)}
            <span className="text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 font-semibold">{conversation.channel}</span>
            <span className="text-xs px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 font-semibold">{conversation.status}</span>
          </h1>
        </div>
        <Button onClick={handleRunAnalysis} disabled={analyzing} className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs">
          {analyzing ? 'Analyzing...' : 'Run Response Agent Analysis'}
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Message Timeline (Left 2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          <div>
            <h2 className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2">Message History Timeline</h2>
            <MessageTimeline messages={conversation.messages} />
          </div>

          <ResponseDraftEditor conversationId={conversation.id} onGenerateDraft={handleRunAnalysis} />
        </div>

        {/* Intelligence & Actions (Right 1 col) */}
        <div className="space-y-6">
          <IntelligenceCard conversationId={conversation.id} analysis={conversation.latest_analysis || null} onRefresh={fetchDetail} />
        </div>
      </div>
    </div>
  );
}
