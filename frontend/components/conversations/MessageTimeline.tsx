import React from 'react';
import { MessageItem } from '@/lib/api/conversations';

interface MessageTimelineProps {
  messages: MessageItem[];
}

export function MessageTimeline({ messages }: MessageTimelineProps) {
  if (!messages || messages.length === 0) {
    return (
      <div className="p-8 text-center bg-zinc-900/40 rounded-xl border border-zinc-800 text-zinc-500 text-xs">
        No message history recorded yet for this conversation.
      </div>
    );
  }

  return (
    <div className="space-y-4 p-4 rounded-xl bg-zinc-950 border border-zinc-800 max-h-[500px] overflow-y-auto">
      {messages.map((m) => {
        const isInbound = m.direction === 'INBOUND';
        return (
          <div
            key={m.id}
            className={`flex flex-col ${isInbound ? 'items-start' : 'items-end'}`}
          >
            <div className="flex items-center gap-2 mb-1 text-[10px] text-zinc-400">
              <span className="font-bold">{isInbound ? 'Prospect Inbound' : 'Outbound Sent'}</span>
              <span>•</span>
              <span>{m.sent_at ? new Date(m.sent_at).toLocaleString() : new Date(m.created_at).toLocaleString()}</span>
            </div>
            <div
              className={`p-3.5 rounded-xl max-w-[85%] text-xs space-y-1 ${
                isInbound
                  ? 'bg-zinc-900 text-zinc-200 border border-zinc-800 rounded-tl-none'
                  : 'bg-indigo-600/90 text-white rounded-tr-none'
              }`}
            >
              {m.subject && <p className="font-bold border-b border-white/10 pb-1 mb-1">{m.subject}</p>}
              <p className="whitespace-pre-wrap leading-relaxed">{m.body}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
