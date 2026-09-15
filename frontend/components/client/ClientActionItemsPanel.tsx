'use client';

import React, { useState } from 'react';
import { CheckSquare, Square, Clock, AlertCircle, CheckCircle2, UserCheck } from 'lucide-react';

export interface ActionItem {
  id: string;
  title: string;
  description: string;
  due_date?: string;
  status: 'PENDING' | 'COMPLETED' | 'OVERDUE';
  assigned_to: string;
}

interface ClientActionItemsPanelProps {
  actionItems?: ActionItem[];
  onToggleStatus?: (id: string, newStatus: 'PENDING' | 'COMPLETED') => void;
}

export const ClientActionItemsPanel: React.FC<ClientActionItemsPanelProps> = ({
  actionItems = [
    {
      id: 'act-1',
      title: 'Provide Production API Credentials for Payment Gateway',
      description: 'Upload live API keys to secure vault for integration testing.',
      due_date: '2026-09-12',
      status: 'PENDING',
      assigned_to: 'Client Admin',
    },
    {
      id: 'act-2',
      title: 'Review & Sign Off Baseline Requirements Spec',
      description: 'Confirm all functional user stories in the discovery document.',
      due_date: '2026-09-10',
      status: 'COMPLETED',
      assigned_to: 'Project Sponsor',
    },
    {
      id: 'act-3',
      title: 'Supply Vector Brand Logos and Color Guidelines',
      description: 'SVG format brand assets needed for client portal customization.',
      due_date: '2026-09-15',
      status: 'PENDING',
      assigned_to: 'Design Lead',
    },
  ],
  onToggleStatus,
}) => {
  const [items, setItems] = useState<ActionItem[]>(actionItems);

  const toggleItem = (id: string) => {
    setItems((prev) =>
      prev.map((item) => {
        if (item.id === id) {
          const nextStatus = item.status === 'COMPLETED' ? 'PENDING' : 'COMPLETED';
          if (onToggleStatus) onToggleStatus(id, nextStatus);
          return { ...item, status: nextStatus };
        }
        return item;
      })
    );
  };

  const pendingCount = items.filter((i) => i.status !== 'COMPLETED').length;
  const completedCount = items.filter((i) => i.status === 'COMPLETED').length;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl text-slate-100 space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <UserCheck className="w-5 h-5 text-emerald-400" />
            <span>Client Outstanding Action Items</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Checklist of required actions and inputs from the client team to keep delivery on schedule.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs">
          <span className="px-3 py-1 rounded-full font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            {pendingCount} Pending
          </span>
          <span className="px-3 py-1 rounded-full font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            {completedCount} Completed
          </span>
        </div>
      </div>

      <div className="space-y-3">
        {items.map((item) => (
          <div
            key={item.id}
            onClick={() => toggleItem(item.id)}
            className={`p-4 rounded-xl border cursor-pointer transition duration-150 flex items-start space-x-3.5 ${
              item.status === 'COMPLETED'
                ? 'bg-slate-950/40 border-slate-800 opacity-70'
                : 'bg-slate-950 border-slate-800 hover:border-slate-700'
            }`}
          >
            <button className="mt-0.5 text-slate-400 hover:text-emerald-400 focus:outline-none">
              {item.status === 'COMPLETED' ? (
                <CheckSquare className="w-5 h-5 text-emerald-400 shrink-0" />
              ) : (
                <Square className="w-5 h-5 text-slate-500 shrink-0" />
              )}
            </button>
            <div className="flex-1 space-y-1">
              <div className="flex items-center justify-between">
                <h4
                  className={`text-sm font-semibold ${
                    item.status === 'COMPLETED' ? 'line-through text-slate-400' : 'text-white'
                  }`}
                >
                  {item.title}
                </h4>
                {item.due_date && (
                  <span className="text-[11px] font-medium text-slate-400 flex items-center space-x-1">
                    <Clock className="w-3.5 h-3.5 text-amber-400" />
                    <span>Due {item.due_date}</span>
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-400">{item.description}</p>
              <div className="text-[10px] font-mono text-slate-500 pt-1">
                Assigned: {item.assigned_to}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
