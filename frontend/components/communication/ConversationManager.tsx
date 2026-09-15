'use client';

import React, { useEffect, useState } from 'react';
import {
  Conversation,
  ConversationDetail,
  ConversationMessage,
  MessageVisibility,
  communicationApi,
} from '@/lib/api/communication';

export const ConversationManager: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [threadDetail, setThreadDetail] = useState<ConversationDetail | null>(null);
  const [messageBody, setMessageBody] = useState('');
  const [visibility, setVisibility] = useState<MessageVisibility>('CLIENT_VISIBLE');
  const [loadingList, setLoadingList] = useState(true);
  const [loadingThread, setLoadingThread] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // New conversation modal state
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newType, setNewType] = useState<any>('PROJECT');

  const loadConversations = async () => {
    setLoadingList(true);
    setError(null);
    try {
      const data = await communicationApi.listConversations();
      setConversations(data || []);
      if (data && data.length > 0 && !activeConversationId) {
        setActiveConversationId(data[0].id);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load conversations');
    } finally {
      setLoadingList(false);
    }
  };

  const loadThread = async (id: string) => {
    setLoadingThread(true);
    setError(null);
    try {
      const detail = await communicationApi.getConversation(id);
      setThreadDetail(detail);
    } catch (err: any) {
      setError(err.message || 'Failed to load thread messages');
    } finally {
      setLoadingThread(false);
    }
  };

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    if (activeConversationId) {
      loadThread(activeConversationId);
    }
  }, [activeConversationId]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeConversationId || !messageBody.trim()) return;

    setSending(true);
    try {
      await communicationApi.postMessage(activeConversationId, {
        body: messageBody.trim(),
        visibility,
      });
      setMessageBody('');
      loadThread(activeConversationId);
    } catch (err: any) {
      setError(err.message || 'Failed to post message');
    } finally {
      setSending(false);
    }
  };

  const handleCreateConversation = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;

    try {
      const created = await communicationApi.createConversation({
        title: newTitle.trim(),
        conversation_type: newType,
      });
      setShowCreateModal(false);
      setNewTitle('');
      await loadConversations();
      if (created?.conversation_id) {
        setActiveConversationId(created.conversation_id);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to create conversation');
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col space-y-4 h-[750px]">
      <div className="flex justify-between items-center pb-3 border-b border-slate-800">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-indigo-400"></span>
            Conversations & Collaboration
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time project discussions, client messaging, and protected internal notes.
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg shadow transition"
        >
          + New Thread
        </button>
      </div>

      {error && (
        <div className="p-2.5 bg-red-950/60 border border-red-800 rounded-lg text-red-200 text-xs">
          {error}
        </div>
      )}

      {/* Main Grid: Left thread list, Right conversation messages */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 flex-1 min-h-0">
        {/* Thread Sidebar */}
        <div className="border border-slate-800 rounded-lg p-3 bg-slate-950/40 flex flex-col space-y-2 overflow-y-auto">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-1">
            Active Threads
          </span>
          {loadingList ? (
            <div className="text-center py-6 text-slate-500 text-xs animate-pulse">
              Loading threads...
            </div>
          ) : conversations.length === 0 ? (
            <div className="text-center py-8 text-slate-500 text-xs border border-dashed border-slate-800 rounded">
              No conversations found.
            </div>
          ) : (
            conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => setActiveConversationId(conv.id)}
                className={`text-left p-3 rounded-lg border transition-all ${
                  activeConversationId === conv.id
                    ? 'bg-indigo-950/50 border-indigo-500/60 text-slate-100 shadow-sm'
                    : 'bg-slate-900/40 border-slate-800 text-slate-300 hover:bg-slate-800/40'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold truncate">{conv.title}</span>
                  <span className="text-[9px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded font-mono">
                    {conv.conversation_type}
                  </span>
                </div>
                <div className="text-[10px] text-slate-500 mt-1 flex justify-between items-center">
                  <span>{new Date(conv.updated_at).toLocaleDateString()}</span>
                  {conv.is_closed && (
                    <span className="text-red-400 text-[9px] font-medium">Closed</span>
                  )}
                </div>
              </button>
            ))
          )}
        </div>

        {/* Message Thread Body */}
        <div className="md:col-span-2 border border-slate-800 rounded-lg bg-slate-950/40 flex flex-col min-h-0">
          {/* Header */}
          <div className="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-900/30">
            <div>
              <span className="text-sm font-semibold text-slate-200">
                {threadDetail?.conversation.title || 'Select a conversation'}
              </span>
              <span className="text-xs text-slate-500 ml-2">
                ({threadDetail?.members.length || 0} members)
              </span>
            </div>
            {threadDetail?.conversation.is_closed && (
              <span className="px-2 py-0.5 bg-red-950/60 text-red-300 border border-red-800 rounded text-[10px]">
                Closed
              </span>
            )}
          </div>

          {/* Messages Stream */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3">
            {loadingThread ? (
              <div className="text-center py-12 text-slate-500 text-xs animate-pulse">
                Loading messages...
              </div>
            ) : !threadDetail || threadDetail.messages.length === 0 ? (
              <div className="text-center py-12 text-slate-500 text-xs">
                No messages yet. Send the first message below.
              </div>
            ) : (
              threadDetail.messages.map((msg: ConversationMessage) => {
                const isInternal = msg.visibility === 'INTERNAL';
                return (
                  <div
                    key={msg.id}
                    className={`p-3 rounded-lg border text-xs ${
                      isInternal
                        ? 'bg-amber-950/20 border-amber-600/40 text-amber-100 ml-6'
                        : 'bg-slate-900/70 border-slate-800 text-slate-200'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center space-x-2">
                        <span className="font-semibold text-slate-300 font-mono text-[11px]">
                          User {msg.sender_id.slice(0, 8)}
                        </span>
                        {isInternal && (
                          <span className="bg-amber-500/20 text-amber-300 border border-amber-500/40 px-1.5 py-0.2 rounded text-[9px] font-bold">
                            INTERNAL NOTE (Protected)
                          </span>
                        )}
                        {msg.is_edited && (
                          <span className="text-[10px] text-slate-500 italic">
                            (edited v{msg.edit_count + 1})
                          </span>
                        )}
                      </div>
                      <span className="text-[10px] text-slate-500 font-mono">
                        {new Date(msg.created_at).toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </span>
                    </div>
                    <p className="text-slate-300 leading-relaxed whitespace-pre-wrap">{msg.body}</p>
                  </div>
                );
              })
            )}
          </div>

          {/* Message Composer */}
          <form
            onSubmit={handleSendMessage}
            className="p-3 border-t border-slate-800 bg-slate-900/50 flex flex-col space-y-2"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <label className="text-xs text-slate-400 flex items-center space-x-1.5">
                  <span>Visibility:</span>
                  <select
                    value={visibility}
                    onChange={(e) => setVisibility(e.target.value as MessageVisibility)}
                    className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded px-2 py-1 focus:ring-1 focus:ring-indigo-500"
                  >
                    <option value="CLIENT_VISIBLE">Client-Visible Message</option>
                    <option value="INTERNAL">Internal Team Note (Hidden from client)</option>
                  </select>
                </label>
              </div>
              <span className="text-[10px] text-slate-500 italic">
                {visibility === 'INTERNAL'
                  ? '🔒 Internal notes are strictly stripped from client portals'
                  : '🌐 Visible to all members & clients'}
              </span>
            </div>

            <div className="flex space-x-2">
              <input
                type="text"
                value={messageBody}
                onChange={(e) => setMessageBody(e.target.value)}
                placeholder={
                  visibility === 'INTERNAL'
                    ? 'Write an internal note...'
                    : 'Type a message to project members...'
                }
                disabled={sending || !activeConversationId}
                className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
              <button
                type="submit"
                disabled={sending || !activeConversationId || !messageBody.trim()}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow transition"
              >
                {sending ? 'Sending...' : 'Send'}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* New Thread Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 max-w-md w-full shadow-2xl space-y-4">
            <h3 className="text-base font-bold text-slate-100">Create New Conversation Thread</h3>
            <form onSubmit={handleCreateConversation} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Thread Title
                </label>
                <input
                  type="text"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Q3 Architecture Review"
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Conversation Type
                </label>
                <select
                  value={newType}
                  onChange={(e) => setNewType(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                >
                  <option value="PROJECT">PROJECT</option>
                  <option value="GROUP">GROUP</option>
                  <option value="PROPOSAL">PROPOSAL</option>
                  <option value="CONTRACT">CONTRACT</option>
                  <option value="SUPPORT_TICKET">SUPPORT_TICKET</option>
                  <option value="CHANGE_REQUEST">CHANGE_REQUEST</option>
                  <option value="DIRECT">DIRECT</option>
                </select>
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg shadow"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
