'use client';

import React, { useState, useEffect } from 'react';
import {
  listProjectThreads,
  createThread,
  postMessage,
  runClientAgent,
  DiscussionThread,
  ThreadMessage,
} from '@/lib/api/client_portal';
import { MessageSquare, Send, Plus, Bot, Sparkles, Filter, ShieldCheck, Tag } from 'lucide-react';

interface ClientThreadsPanelProps {
  projectId: string;
}

export const ClientThreadsPanel: React.FC<ClientThreadsPanelProps> = ({ projectId }) => {
  const [threads, setThreads] = useState<DiscussionThread[]>([]);
  const [selectedThreadId, setSelectedThreadId] = useState<string | null>(null);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [posting, setPosting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // New Thread Modal
  const [showNewThreadModal, setShowNewThreadModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newType, setNewType] = useState('GENERAL_QUESTION');

  // AI Agent Action State
  const [agentRunning, setAgentRunning] = useState(false);
  const [agentOutput, setAgentOutput] = useState<any | null>(null);

  useEffect(() => {
    loadThreads();
  }, [projectId]);

  const loadThreads = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listProjectThreads(projectId);
      setThreads(data);
      if (data.length > 0 && !selectedThreadId) {
        setSelectedThreadId(data[0].id);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch discussion threads.');
    } finally {
      setLoading(false);
    }
  };

  const selectedThread = threads.find((t) => t.id === selectedThreadId);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedThreadId || !newMessage.trim()) return;

    setPosting(true);
    try {
      const msg = await postMessage(selectedThreadId, { content: newMessage });
      setThreads((prev) =>
        prev.map((t) =>
          t.id === selectedThreadId ? { ...t, messages: [...(t.messages || []), msg] } : t
        )
      );
      setNewMessage('');
    } catch (err: any) {
      setError(err?.message || 'Failed to send message.');
    } finally {
      setPosting(false);
    }
  };

  const handleCreateThread = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    try {
      const created = await createThread(projectId, {
        title: newTitle,
        thread_type: newType,
      });
      setThreads((prev) => [created, ...prev]);
      setSelectedThreadId(created.id);
      setShowNewThreadModal(false);
      setNewTitle('');
    } catch (err: any) {
      setError(err?.message || 'Failed to create thread.');
    }
  };

  const handleRunAgentAction = async (
    action: 'CLASSIFY_REQUEST' | 'SUMMARIZE_FEEDBACK' | 'EXTRACT_ACTIONS' | 'EVALUATE_SCOPE'
  ) => {
    setAgentRunning(true);
    setAgentOutput(null);
    try {
      const res = await runClientAgent(projectId, action);
      setAgentOutput({ action, data: res });
    } catch (err: any) {
      setError(err?.message || `Failed to run agent action ${action}`);
    } finally {
      setAgentRunning(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-slate-800 pb-4 gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <MessageSquare className="w-5 h-5 text-blue-400" />
            <span>Client Discussion & Communication</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Audited discussion threads. Messages visible to clients are sanitized and client-friendly.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowNewThreadModal(true)}
            className="px-3.5 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-xs font-semibold text-white flex items-center space-x-1.5 shadow"
          >
            <Plus className="w-4 h-4" />
            <span>New Thread</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-950/40 border border-red-800/50 rounded-lg text-xs text-red-300">
          {error}
        </div>
      )}

      {/* AI Assistant Quick Intelligence Toolbar */}
      <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 space-y-3">
        <div className="flex items-center space-x-2 text-xs font-bold text-amber-400">
          <Bot className="w-4 h-4" />
          <span>ClientCollaborationAgent v1.0 Intelligence Tools</span>
          <span className="text-[10px] font-normal text-slate-500">(Restricted: AI cannot approve scope/pricing)</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => handleRunAgentAction('CLASSIFY_REQUEST')}
            disabled={agentRunning}
            className="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 border border-slate-700 flex items-center space-x-1"
          >
            <Tag className="w-3.5 h-3.5 text-blue-400" />
            <span>Classify Feedback</span>
          </button>
          <button
            onClick={() => handleRunAgentAction('SUMMARIZE_FEEDBACK')}
            disabled={agentRunning}
            className="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 border border-slate-700 flex items-center space-x-1"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>Summarize Feedback</span>
          </button>
          <button
            onClick={() => handleRunAgentAction('EXTRACT_ACTIONS')}
            disabled={agentRunning}
            className="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 border border-slate-700 flex items-center space-x-1"
          >
            <Filter className="w-3.5 h-3.5 text-emerald-400" />
            <span>Extract Action Items</span>
          </button>
          <button
            onClick={() => handleRunAgentAction('EVALUATE_SCOPE')}
            disabled={agentRunning}
            className="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300 border border-slate-700 flex items-center space-x-1"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-purple-400" />
            <span>Detect Scope Creep</span>
          </button>
        </div>

        {agentRunning && (
          <div className="text-xs text-amber-300 animate-pulse">Running AI Agent Analysis...</div>
        )}

        {agentOutput && (
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-3 text-xs text-slate-300 space-y-1">
            <div className="font-semibold text-amber-400">Analysis Result ({agentOutput.action}):</div>
            <pre className="text-[11px] font-mono text-slate-300 whitespace-pre-wrap overflow-x-auto">
              {JSON.stringify(agentOutput.data, null, 2)}
            </pre>
          </div>
        )}
      </div>

      {/* Main Threads Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 min-h-[400px]">
        {/* Threads Sidebar */}
        <div className="md:col-span-1 border border-slate-800 rounded-xl bg-slate-950 p-4 space-y-3">
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Discussion Threads
          </h3>
          {loading ? (
            <p className="text-xs text-slate-500">Loading threads...</p>
          ) : threads.length === 0 ? (
            <p className="text-xs text-slate-500">No active threads found.</p>
          ) : (
            <div className="space-y-2">
              {threads.map((t) => (
                <div
                  key={t.id}
                  onClick={() => setSelectedThreadId(t.id)}
                  className={`p-3 rounded-lg border cursor-pointer transition duration-150 ${
                    selectedThreadId === t.id
                      ? 'bg-blue-600/10 border-blue-500/50 text-white'
                      : 'bg-slate-900 border-slate-800 hover:border-slate-700 text-slate-300'
                  }`}
                >
                  <div className="flex items-center justify-between text-xs font-semibold">
                    <span className="truncate">{t.title}</span>
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                      {t.type}
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-400 mt-1 flex items-center justify-between">
                    <span>{t.messages?.length || 0} messages</span>
                    <span>{new Date(t.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Selected Thread Conversation */}
        <div className="md:col-span-2 border border-slate-800 rounded-xl bg-slate-950 p-4 flex flex-col justify-between">
          {selectedThread ? (
            <>
              {/* Thread Info Bar */}
              <div className="border-b border-slate-800 pb-3 mb-4 flex items-center justify-between">
                <div>
                  <h4 className="font-bold text-sm text-white">{selectedThread.title}</h4>
                  <div className="flex items-center space-x-2 text-xs text-slate-400 mt-0.5">
                    <span>Type: {selectedThread.type}</span>
                    <span>•</span>
                    <span className="text-emerald-400">Visibility: {selectedThread.visibility}</span>
                  </div>
                </div>
              </div>

              {/* Messages Container */}
              <div className="flex-1 overflow-y-auto space-y-3 pr-2 mb-4 max-h-[350px]">
                {selectedThread.messages?.length === 0 ? (
                  <p className="text-xs text-slate-500 text-center py-8">No messages in this thread yet.</p>
                ) : (
                  selectedThread.messages?.map((msg) => (
                    <div
                      key={msg.id}
                      className={`p-3 rounded-lg text-xs space-y-1 ${
                        msg.sender_type === 'CLIENT'
                          ? 'bg-blue-950/40 border border-blue-800/40 ml-4'
                          : 'bg-slate-900 border border-slate-800 mr-4'
                      }`}
                    >
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="font-semibold text-slate-200">
                          {msg.sender_type === 'CLIENT' ? 'Client Member' : 'North’s Team'}
                        </span>
                        <span className="text-slate-500">
                          {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                      <p className="text-slate-300 whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  ))
                )}
              </div>

              {/* Reply Box */}
              <form onSubmit={handleSendMessage} className="flex items-center space-x-2 pt-2 border-t border-slate-800">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Write a response..."
                  className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
                />
                <button
                  type="submit"
                  disabled={posting || !newMessage.trim()}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-xs font-semibold text-white rounded-lg flex items-center space-x-1.5"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>Send</span>
                </button>
              </form>
            </>
          ) : (
            <div className="flex items-center justify-center flex-1 text-xs text-slate-500">
              Select a thread to read or post messages.
            </div>
          )}
        </div>
      </div>

      {/* Modal: New Thread */}
      {showNewThreadModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <h3 className="font-bold text-base text-white">Create New Discussion Thread</h3>
            <form onSubmit={handleCreateThread} className="space-y-4">
              <div>
                <label className="text-xs font-medium text-slate-300">Thread Title</label>
                <input
                  type="text"
                  required
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Design Feedback on Dashboard V1"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 mt-1"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300">Thread Type</label>
                <select
                  value={newType}
                  onChange={(e) => setNewType(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500 mt-1"
                >
                  <option value="GENERAL_QUESTION">General Question</option>
                  <option value="DELIVERABLE_FEEDBACK">Deliverable Feedback</option>
                  <option value="SCOPE_CHANGE_REQUEST">Scope Change Request</option>
                  <option value="TECHNICAL_CLARIFICATION">Technical Clarification</option>
                </select>
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowNewThreadModal(false)}
                  className="px-4 py-2 bg-slate-800 text-xs font-semibold text-slate-300 rounded-lg hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-xs font-semibold text-white rounded-lg hover:bg-blue-500"
                >
                  Create Thread
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
