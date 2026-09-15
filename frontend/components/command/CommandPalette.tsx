'use client';

import React, { useEffect, useState } from 'react';
import {
  CommandDefinition,
  CommandResponse,
  searchApi,
} from '@/lib/api/search';

export const CommandPalette: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputText, setInputText] = useState('');
  const [commands, setCommands] = useState<CommandDefinition[]>([]);
  const [commandResponse, setCommandResponse] = useState<CommandResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Global Ctrl+K / Cmd+K shortcut listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  useEffect(() => {
    if (isOpen) {
      searchApi.listCommands().then(setCommands).catch(() => {});
    }
  }, [isOpen]);

  const handleParseAndExecute = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    setLoading(true);
    setError(null);
    setCommandResponse(null);
    try {
      // 1. Parse command
      const parsed = await searchApi.parseCommand(inputText.trim());
      if (!parsed) {
        setError('No recognized command intent. Try "go to leads", "create task...", or "open inbox".');
        return;
      }

      // 2. Execute command
      const executed = await searchApi.executeCommand({
        command_id: parsed.command_id,
        parameters: parsed.parameters,
      });
      setCommandResponse(executed);
    } catch (err: any) {
      setError(err.message || 'Command execution failed');
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmAction = async (approval: boolean) => {
    if (!commandResponse) return;
    setLoading(true);
    try {
      const executed = await searchApi.executeCommand({
        command_id: commandResponse.command_id,
        parameters: commandResponse.parameters,
        has_confirmation: true,
        has_approval: approval,
      });
      setCommandResponse(executed);
    } catch (err: any) {
      setError(err.message || 'Confirmation failed');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-start justify-center pt-24 p-4 z-50">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Command Input Header */}
        <form onSubmit={handleParseAndExecute} className="p-4 border-b border-slate-800 flex items-center space-x-3 bg-slate-950/60">
          <span className="text-cyan-400 text-lg">⚡</span>
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type a command or instruction (e.g. 'go to leads', 'create task homepage', 'open inbox')..."
            autoFocus
            className="flex-1 bg-transparent text-sm text-slate-100 placeholder-slate-500 focus:outline-none"
          />
          <span className="text-[10px] font-mono bg-slate-800 text-slate-400 px-2 py-1 rounded border border-slate-700">
            ESC to exit
          </span>
        </form>

        {error && (
          <div className="p-3 bg-red-950/60 border-b border-red-800 text-red-200 text-xs">
            {error}
          </div>
        )}

        {/* Command Result / Gate View */}
        {commandResponse && (
          <div className="p-4 bg-slate-950/80 border-b border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-200">
                Command: <strong className="text-cyan-300">{commandResponse.command_id}</strong>
              </span>
              <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded font-mono">
                Status: {commandResponse.status}
              </span>
            </div>

            {/* Approval / Confirmation Gate Banner */}
            {commandResponse.status === 'APPROVAL_REQUIRED' && (
              <div className="p-3 bg-amber-950/50 border border-amber-600/50 rounded-lg space-y-2">
                <div className="text-xs text-amber-200 font-semibold flex items-center gap-1.5">
                  <span>🛡️</span>
                  <span>Human Approval Required for Sensitive Action</span>
                </div>
                <p className="text-[11px] text-amber-300/80">{commandResponse.approval_reason}</p>
                <div className="flex space-x-2 pt-1">
                  <button
                    onClick={() => handleConfirmAction(true)}
                    className="px-3 py-1 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded shadow"
                  >
                    Authorize & Send
                  </button>
                  <button
                    onClick={() => setCommandResponse(null)}
                    className="px-3 py-1 bg-slate-800 text-slate-300 text-xs rounded"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {commandResponse.status === 'CONFIRMATION_REQUIRED' && (
              <div className="p-3 bg-blue-950/50 border border-blue-600/50 rounded-lg space-y-2">
                <div className="text-xs text-blue-200 font-semibold">Confirm Action Execution</div>
                <div className="flex space-x-2 pt-1">
                  <button
                    onClick={() => handleConfirmAction(false)}
                    className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded shadow"
                  >
                    Confirm
                  </button>
                  <button
                    onClick={() => setCommandResponse(null)}
                    className="px-3 py-1 bg-slate-800 text-slate-300 text-xs rounded"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {commandResponse.status === 'EXECUTED' && (
              <div className="p-3 bg-emerald-950/50 border border-emerald-600/50 rounded-lg text-emerald-200 text-xs font-mono">
                ✓ Executed: {JSON.stringify(commandResponse.execution_result)}
              </div>
            )}
          </div>
        )}

        {/* Quick Command Suggestions List */}
        <div className="p-3 max-h-72 overflow-y-auto space-y-1">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider px-2">
            Available Shortcuts
          </span>
          {commands.map((cmd) => (
            <button
              key={cmd.command_id}
              onClick={() => {
                setInputText(cmd.name);
              }}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-slate-800/60 flex items-center justify-between text-xs text-slate-300 transition-colors"
            >
              <div className="flex items-center space-x-2">
                <span className="text-slate-500">⌘</span>
                <span className="font-semibold text-slate-200">{cmd.name}</span>
                <span className="text-slate-500 text-[11px]">— {cmd.description}</span>
              </div>
              <span className="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded font-mono">
                {cmd.category}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
