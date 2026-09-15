'use client';

import React, { useEffect, useState } from 'react';

interface RealtimeEvent {
  id: string;
  channel: string;
  event_type: string;
  timestamp: string;
  payload: Record<string, any>;
}

export const RealtimeCollaborationPanel: React.FC = () => {
  const [isConnected, setIsConnected] = useState(true);
  const [activeChannels, setActiveChannels] = useState<string[]>([
    'tenant:current:notifications',
    'project:global:events',
    'presence:active-users',
  ]);
  const [events, setEvents] = useState<RealtimeEvent[]>([
    {
      id: 'evt-1',
      channel: 'tenant:current:notifications',
      event_type: 'notification.dispatched',
      timestamp: new Date().toLocaleTimeString(),
      payload: { title: 'System health check passed', priority: 'LOW' },
    },
    {
      id: 'evt-2',
      channel: 'presence:active-users',
      event_type: 'user.heartbeat',
      timestamp: new Date().toLocaleTimeString(),
      payload: { user_id: 'usr_admin', status: 'online' },
    },
  ]);

  const [newChannel, setNewChannel] = useState('');

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newChannel.trim() || activeChannels.includes(newChannel.trim())) return;
    setActiveChannels((prev) => [...prev, newChannel.trim()]);
    setNewChannel('');
  };

  const handleUnsubscribe = (channel: string) => {
    setActiveChannels((prev) => prev.filter((c) => c !== channel));
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col space-y-6">
      <div className="flex justify-between items-center pb-3 border-b border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
            Real-Time Collaboration & Event Gateway
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            WebSocket presence tracking, collaborative editing locks, and low-latency broadcast streaming.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <span
            className={`w-2.5 h-2.5 rounded-full ${
              isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'
            }`}
          ></span>
          <span className="text-xs font-mono text-slate-300">
            {isConnected ? 'LIVE GATEWAY CONNECTED' : 'DISCONNECTED'}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Channel Subscription Management */}
        <div className="border border-slate-800 rounded-lg p-4 bg-slate-950/40 flex flex-col space-y-4">
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Active Subscriptions
          </h3>

          <form onSubmit={handleSubscribe} className="flex space-x-2">
            <input
              type="text"
              value={newChannel}
              onChange={(e) => setNewChannel(e.target.value)}
              placeholder="channel:name"
              className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-100 focus:outline-none focus:border-cyan-500"
            />
            <button
              type="submit"
              className="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold rounded-lg"
            >
              + Join
            </button>
          </form>

          <div className="space-y-2 overflow-y-auto max-h-[300px]">
            {activeChannels.map((channel) => (
              <div
                key={channel}
                className="flex items-center justify-between p-2 rounded bg-slate-900/60 border border-slate-800 text-xs font-mono text-cyan-300"
              >
                <span className="truncate">{channel}</span>
                <button
                  onClick={() => handleUnsubscribe(channel)}
                  className="text-slate-500 hover:text-red-400 text-xs px-1"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Live Event Stream Feed */}
        <div className="md:col-span-2 border border-slate-800 rounded-lg p-4 bg-slate-950/40 flex flex-col space-y-3">
          <div className="flex justify-between items-center">
            <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
              Live Broadcast Stream
            </h3>
            <span className="text-[10px] text-slate-500 font-mono">
              Auto-scrolling stream
            </span>
          </div>

          <div className="space-y-2 overflow-y-auto max-h-[350px]">
            {events.map((evt) => (
              <div
                key={evt.id}
                className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 flex flex-col space-y-1 text-xs"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-cyan-400 font-mono font-semibold">{evt.event_type}</span>
                    <span className="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded font-mono">
                      {evt.channel}
                    </span>
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono">{evt.timestamp}</span>
                </div>
                <pre className="bg-slate-950 p-2 rounded text-[11px] text-slate-400 overflow-x-auto font-mono">
                  {JSON.stringify(evt.payload, null, 2)}
                </pre>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
