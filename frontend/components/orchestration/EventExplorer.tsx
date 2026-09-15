'use client';

import React, { useState, useEffect } from 'react';
import { DomainEventRecord, orchestrationApi } from '@/lib/api/orchestration';
import { Activity, RotateCcw, Filter, Radio, ChevronRight, RefreshCw, Play } from 'lucide-react';

export const EventExplorer: React.FC = () => {
  const [events, setEvents] = useState<DomainEventRecord[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<DomainEventRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [eventTypeFilter, setEventTypeFilter] = useState<string>('');
  const [replayType, setReplayType] = useState<string>('');
  const [replayMode, setReplayMode] = useState<string>('DRY_RUN');
  const [replayMessage, setReplayMessage] = useState<string>('');

  const loadEvents = async () => {
    try {
      setLoading(true);
      const data = await orchestrationApi.listEvents(eventTypeFilter || undefined);
      setEvents(data);
    } catch (err) {
      console.error('Failed to load events', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, [eventTypeFilter]);

  const handleReplay = async () => {
    if (!replayType) return;
    try {
      setReplayMessage('Executing replay...');
      const res = await orchestrationApi.replayEvents({
        event_type: replayType,
        replay_mode: replayMode,
      });
      setReplayMessage(`Replay complete: ${res.events_replayed_count} events replayed in mode ${res.replay_mode}`);
      loadEvents();
    } catch (err: any) {
      setReplayMessage(`Replay failed: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Replay Control Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <RotateCcw className="w-4 h-4 text-cyan-400" /> Controlled Event Replay
          </h3>
          <p className="text-xs text-slate-400">Replay historical domain events without re-executing sensitive side-effects</p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <input
            type="text"
            placeholder="Event type (e.g. lead.qualified)..."
            value={replayType}
            onChange={(e) => setReplayType(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2 outline-none focus:border-cyan-500 w-56"
          />
          <select
            value={replayMode}
            onChange={(e) => setReplayMode(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2 outline-none"
          >
            <option value="DRY_RUN">Dry Run (No Side Effects)</option>
            <option value="READ_ONLY">Read Only</option>
            <option value="REBUILD_PROJECTION">Rebuild Projection</option>
            <option value="CONTROLLED_REEXECUTION">Controlled Re-execution</option>
          </select>
          <button
            onClick={handleReplay}
            disabled={!replayType}
            className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors flex items-center gap-1.5"
          >
            <Play className="w-3.5 h-3.5" /> Trigger Replay
          </button>
        </div>
      </div>

      {replayMessage && (
        <div className="p-3 rounded-lg bg-slate-800/80 border border-cyan-500/30 text-xs text-cyan-300 font-mono">
          {replayMessage}
        </div>
      )}

      {/* Events Stream & Detail Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Events Stream */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col h-[500px]">
          <div className="p-4 border-b border-slate-800 flex items-center justify-between">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-400" /> Domain Events Stream
            </h3>
            <button onClick={loadEvents} className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg">
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto divide-y divide-slate-800">
            {loading ? (
              <div className="p-8 text-center text-slate-500 text-xs">Loading domain events...</div>
            ) : events.length === 0 ? (
              <div className="p-8 text-center text-slate-500 text-xs">No domain events recorded.</div>
            ) : (
              events.map((evt) => (
                <div
                  key={evt.id}
                  onClick={() => setSelectedEvent(evt)}
                  className={`p-3.5 hover:bg-slate-800/40 transition-colors cursor-pointer flex items-center justify-between ${
                    selectedEvent?.id === evt.id ? 'bg-slate-800/60 border-l-2 border-cyan-500' : ''
                  }`}
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-slate-200">{evt.event_type}</span>
                      <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                        {evt.event_version}
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-400 flex items-center gap-2">
                      <span>Aggregate: {evt.aggregate_type} ({evt.aggregate_id})</span>
                      <span>•</span>
                      <span>{new Date(evt.created_at).toLocaleTimeString()}</span>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-600" />
                </div>
              ))
            )}
          </div>
        </div>

        {/* Selected Event Inspector */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 overflow-y-auto h-[500px]">
          {selectedEvent ? (
            <div className="space-y-4">
              <div className="border-b border-slate-800 pb-3">
                <h4 className="text-sm font-semibold text-slate-100">{selectedEvent.event_type}</h4>
                <p className="text-xs text-slate-400 font-mono mt-0.5">Event ID: {selectedEvent.event_id}</p>
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div>
                  <span className="text-slate-500">Aggregate Type:</span>
                  <div className="text-slate-200 font-medium">{selectedEvent.aggregate_type}</div>
                </div>
                <div>
                  <span className="text-slate-500">Aggregate ID:</span>
                  <div className="text-slate-200 font-mono">{selectedEvent.aggregate_id}</div>
                </div>
                <div>
                  <span className="text-slate-500">Correlation ID:</span>
                  <div className="text-slate-200 font-mono">{selectedEvent.correlation_id}</div>
                </div>
                <div>
                  <span className="text-slate-500">Delivery Status:</span>
                  <span className="text-emerald-400 font-semibold">{selectedEvent.status}</span>
                </div>
              </div>

              <div>
                <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1.5">
                  Payload JSON
                </div>
                <pre className="text-xs font-mono bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-300 overflow-x-auto">
                  {JSON.stringify(selectedEvent.payload, null, 2)}
                </pre>
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-slate-500">
              Select an event from the stream to inspect details and payload.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
