'use client';

import React, { useState, useEffect } from 'react';
import { DeadLetterRecord, orchestrationApi } from '@/lib/api/orchestration';
import { AlertOctagon, RotateCcw, Trash2, RefreshCw } from 'lucide-react';

export const DeadLetterQueueViewer: React.FC = () => {
  const [messages, setMessages] = useState<DeadLetterRecord[]>([]);
  const [selectedMessage, setSelectedMessage] = useState<DeadLetterRecord | null>(null);
  const [loading, setLoading] = useState(true);

  const loadDLQ = async () => {
    try {
      setLoading(true);
      const data = await orchestrationApi.listDeadLetters();
      setMessages(data);
    } catch (err) {
      console.error('Failed to load DLQ records', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDLQ();
  }, []);

  const handleRetry = async (id: string) => {
    try {
      await orchestrationApi.retryDeadLetter(id);
      loadDLQ();
    } catch (err) {
      console.error('Failed to schedule retry for DLQ message', err);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* DLQ Message List */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col h-[500px]">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <AlertOctagon className="w-4 h-4 text-rose-400" /> Dead Letter Queue (DLQ)
          </h3>
          <button onClick={loadDLQ} className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg">
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto divide-y divide-slate-800">
          {loading ? (
            <div className="p-8 text-center text-slate-500 text-xs">Loading DLQ messages...</div>
          ) : messages.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs">No poisoned messages in DLQ. All clear.</div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                onClick={() => setSelectedMessage(msg)}
                className={`p-4 hover:bg-slate-800/40 transition-colors cursor-pointer flex items-center justify-between ${
                  selectedMessage?.id === msg.id ? 'bg-slate-800/60 border-l-2 border-rose-500' : ''
                }`}
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-slate-200">{msg.event_type}</span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
                      {msg.status}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400">
                    Consumer: <strong className="text-slate-300">{msg.consumer}</strong> • Attempts: {msg.attempt_count}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Selected DLQ Detail & Retry */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 overflow-y-auto h-[500px]">
        {selectedMessage ? (
          <div className="space-y-4">
            <div className="border-b border-slate-800 pb-3 flex items-center justify-between">
              <div>
                <h4 className="text-sm font-semibold text-slate-100">{selectedMessage.event_type}</h4>
                <p className="text-xs text-slate-400 font-mono mt-0.5">Event ID: {selectedMessage.event_id}</p>
              </div>
              <button
                onClick={() => handleRetry(selectedMessage.id)}
                className="bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" /> Replay / Retry
              </button>
            </div>

            <div>
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                Failure Reason & Stack Trace
              </div>
              <div className="bg-rose-950/30 border border-rose-900/50 text-rose-300 p-3 rounded-lg text-xs font-mono">
                {selectedMessage.error_summary}
              </div>
            </div>

            <div>
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
                Message Payload
              </div>
              <pre className="text-xs font-mono bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-300 overflow-x-auto">
                {JSON.stringify(selectedMessage.payload, null, 2)}
              </pre>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-xs text-slate-500">
            Select a dead letter message to inspect error summary and schedule safe retry.
          </div>
        )}
      </div>
    </div>
  );
};
