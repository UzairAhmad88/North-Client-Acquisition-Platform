'use client';

import React, { useState } from 'react';
import {
  Wrench,
  Calendar,
  CheckCircle2,
  Clock,
  Plus,
  FileCheck,
  ShieldCheck,
} from 'lucide-react';
import { MaintenancePlan, MaintenanceWorkOrder, supportApi } from '@/lib/api/support';

interface MaintenanceWorkOrderPanelProps {
  plans: MaintenancePlan[];
  workOrders: MaintenanceWorkOrder[];
  onRefresh: () => void;
}

export const MaintenanceWorkOrderPanel: React.FC<MaintenanceWorkOrderPanelProps> = ({
  plans,
  workOrders,
  onRefresh,
}) => {
  const [selectedOrder, setSelectedOrder] = useState<MaintenanceWorkOrder | null>(null);
  const [executionNotes, setExecutionNotes] = useState('');
  const [completing, setCompleting] = useState(false);

  // New Work Order Modal
  const [showScheduleModal, setShowScheduleModal] = useState(false);
  const [selectedPlanId, setSelectedPlanId] = useState(plans[0]?.id || '');
  const [orderTitle, setOrderTitle] = useState('');
  const [scheduledFor, setScheduledFor] = useState(new Date().toISOString().split('T')[0]);

  const handleScheduleOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPlanId) return;
    try {
      await supportApi.scheduleWorkOrder(selectedPlanId, {
        title: orderTitle,
        scheduled_for: new Date(scheduledFor).toISOString(),
      });
      setShowScheduleModal(false);
      setOrderTitle('');
      onRefresh();
    } catch (err) {
      console.error(err);
    }
  };

  const handleCompleteOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedOrder) return;
    setCompleting(true);
    try {
      await supportApi.completeWorkOrder(selectedOrder.id, {
        execution_notes: executionNotes || 'All preventive checklist items verified and successfully patched.',
        checklist_results: [
          { task: 'Security patch audit', completed: true },
          { task: 'Database vacuum & re-index', completed: true },
          { task: 'SSL / Certificate renewal check', completed: true },
          { task: 'Log rotation & disk space check', completed: true },
        ],
      });
      setSelectedOrder(null);
      setExecutionNotes('');
      onRefresh();
    } catch (err) {
      console.error(err);
    } finally {
      setCompleting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Wrench className="w-5 h-5 text-amber-400" />
              Scheduled Maintenance & Preventive Work Orders
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Recurring health checks, patch compliance, performance tuning, and audit trails
            </p>
          </div>
          {plans.length > 0 && (
            <button
              onClick={() => setShowScheduleModal(true)}
              className="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 transition"
            >
              <Plus className="w-4 h-4" /> Schedule Work Order
            </button>
          )}
        </div>

        {/* Maintenance Plans Summary */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {plans.map((p) => (
            <div key={p.id} className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">
                  {p.plan_type} • {p.frequency}
                </span>
                <span className="text-[10px] font-mono text-emerald-400">{p.status}</span>
              </div>
              <h4 className="text-sm font-bold text-white">{p.title}</h4>
              <p className="text-xs text-slate-400 mt-1">{p.scope_description}</p>
              <div className="mt-3 pt-2 border-t border-slate-800 text-[11px] text-slate-500 flex justify-between">
                <span>Frequency: {p.frequency}</span>
                <span>Work Orders: {p.work_orders?.length || 0}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Work Orders List */}
        <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3">Work Orders Queue</h3>
        {workOrders.length === 0 ? (
          <div className="text-center py-10 border border-dashed border-slate-800 rounded-xl">
            <Calendar className="w-8 h-8 text-slate-600 mx-auto mb-2" />
            <p className="text-xs text-slate-400">No scheduled work orders found.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800 font-semibold uppercase tracking-wider">
                <tr>
                  <th className="pb-3 px-3">Title / Scope</th>
                  <th className="pb-3 px-3">Scheduled For</th>
                  <th className="pb-3 px-3">Status</th>
                  <th className="pb-3 px-3">Executed By</th>
                  <th className="pb-3 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {workOrders.map((order) => (
                  <tr key={order.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-3 px-3 font-medium text-white">{order.task_name}</td>
                    <td className="py-3 px-3 text-slate-400">
                      {new Date(order.scheduled_at).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-3">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        order.status === 'COMPLETED'
                          ? 'bg-emerald-500/20 text-emerald-400'
                          : 'bg-amber-500/20 text-amber-400'
                      }`}>
                        {order.status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-slate-400 text-[11px]">
                      {order.executed_by ? `${order.executed_by}` : 'Pending execution'}
                    </td>
                    <td className="py-3 px-3 text-right">
                      {order.status === 'PLANNED' && (
                        <button
                          onClick={() => setSelectedOrder(order)}
                          className="px-2.5 py-1 text-[11px] bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 border border-emerald-500/30 rounded flex items-center gap-1 ml-auto"
                        >
                          <FileCheck className="w-3 h-3" /> Complete & Sign-off
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

      </div>

      {/* Complete Work Order Modal */}
      {selectedOrder && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              Sign-off Maintenance Work Order: {selectedOrder.task_name}
            </h3>
            <form onSubmit={handleCompleteOrder} className="space-y-4 text-xs">
              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <p className="font-semibold text-slate-300 mb-2">Checklist Verification</p>
                <div className="space-y-1.5 text-slate-400">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" defaultChecked disabled className="rounded text-emerald-500" />
                    <span>Security patch audit & vulnerability remediation</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" defaultChecked disabled className="rounded text-emerald-500" />
                    <span>Database index optimization & backup verification</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" defaultChecked disabled className="rounded text-emerald-500" />
                    <span>SSL/TLS certificates & domain renewal verification</span>
                  </label>
                </div>
              </div>
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Execution Summary</label>
                <textarea
                  rows={3}
                  value={executionNotes}
                  onChange={(e) => setExecutionNotes(e.target.value)}
                  placeholder="Record summary of checks conducted, metrics observed, and patches applied..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                />
              </div>
              <div className="flex justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setSelectedOrder(null)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={completing}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-bold"
                >
                  {completing ? 'Signing off...' : 'Sign-off Work Order'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Schedule Work Order Modal */}
      {showScheduleModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Calendar className="w-5 h-5 text-amber-400" />
              Schedule Maintenance Work Order
            </h3>
            <form onSubmit={handleScheduleOrder} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Maintenance Plan</label>
                <select
                  value={selectedPlanId}
                  onChange={(e) => setSelectedPlanId(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                >
                  {plans.map((p) => (
                    <option key={p.id} value={p.id}>{p.title} ({p.frequency})</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Work Order Title</label>
                <input
                  type="text"
                  required
                  value={orderTitle}
                  onChange={(e) => setOrderTitle(e.target.value)}
                  placeholder="e.g. Q3 Security & Database Maintenance"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Scheduled Date</label>
                <input
                  type="date"
                  required
                  value={scheduledFor}
                  onChange={(e) => setScheduledFor(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                />
              </div>
              <div className="flex justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowScheduleModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-lg font-bold"
                >
                  Schedule Order
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
