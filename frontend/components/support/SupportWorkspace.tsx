'use client';

import React, { useState, useEffect } from 'react';
import {
  LifeBuoy,
  AlertOctagon,
  Wrench,
  BookOpen,
  Sparkles,
  RefreshCw,
  Activity,
  Plus,
  TrendingUp,
} from 'lucide-react';
import {
  SupportRequest,
  Incident,
  Warranty,
  MaintenancePlan,
  MaintenanceWorkOrder,
  KnowledgeArticle,
  SupportOpportunity,
  ClientHealthSnapshot,
  supportApi,
} from '@/lib/api/support';

import { SupportDashboardOverview } from './SupportDashboardOverview';
import { SupportRequestTracker } from './SupportRequestTracker';
import { IncidentManager } from './IncidentManager';
import { MaintenanceWorkOrderPanel } from './MaintenanceWorkOrderPanel';
import { KnowledgeBaseViewer } from './KnowledgeBaseViewer';

interface SupportWorkspaceProps {
  projectId?: string;
  clientAccountId?: string;
}

export const SupportWorkspace: React.FC<SupportWorkspaceProps> = ({
  projectId,
  clientAccountId = 'default_client',
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'requests' | 'incidents' | 'maintenance' | 'kb' | 'opportunities'>('overview');
  const [loading, setLoading] = useState(true);

  const [requests, setRequests] = useState<SupportRequest[]>([]);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [warranties, setWarranties] = useState<Warranty[]>([]);
  const [maintenancePlans, setMaintenancePlans] = useState<MaintenancePlan[]>([]);
  const [workOrders, setWorkOrders] = useState<MaintenanceWorkOrder[]>([]);
  const [articles, setArticles] = useState<KnowledgeArticle[]>([]);
  const [opportunities, setOpportunities] = useState<SupportOpportunity[]>([]);
  const [health, setHealth] = useState<ClientHealthSnapshot | null>(null);


  // New Ticket Modal state
  const [showNewTicketModal, setShowNewTicketModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [submittingTicket, setSubmittingTicket] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [reqRes, incRes, warRes, planRes, woRes, artRes, oppRes, healthRes] = await Promise.all([
        supportApi.listRequests({ project_id: projectId, client_account_id: clientAccountId }),
        supportApi.listIncidents({ project_id: projectId }),
        supportApi.listWarranties({ client_account_id: clientAccountId }),
        supportApi.listMaintenancePlans({ project_id: projectId, client_account_id: clientAccountId }),
        supportApi.listWorkOrders({ project_id: projectId }),
        supportApi.listKnowledgeArticles(),
        supportApi.listOpportunities({ client_account_id: clientAccountId }),
        supportApi.getClientHealth(clientAccountId, { open_tickets: 2, incidents: 0 }),
      ]);

      setRequests(reqRes || []);
      setIncidents(incRes || []);
      setWarranties(warRes || []);
      setMaintenancePlans(planRes || []);
      setWorkOrders(woRes || []);
      setArticles(artRes || []);
      setOpportunities(oppRes || []);
      setHealth(healthRes || null);

    } catch (err) {
      console.error('Failed to load support workspace data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [projectId, clientAccountId]);

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittingTicket(true);
    try {
      await supportApi.createRequest({
        title: newTitle,
        description: newDesc,
        project_id: projectId || 'default_project',
      });
      setShowNewTicketModal(false);
      setNewTitle('');
      setNewDesc('');
      loadData();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmittingTicket(false);
    }
  };


  const handleDetectOpportunities = async () => {
    try {
      await supportApi.detectOpportunities(clientAccountId, {
        project_id: projectId,
        ticket_summaries: requests.map((r) => `${r.title}: ${r.description}`),
      });
      loadData();
      setActiveTab('opportunities');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
              <LifeBuoy className="w-6 h-6 text-cyan-400" />
              Post-Delivery Support, Maintenance & Client Success
            </h1>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
              PHASE 30
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Deterministic ticket classification, contractual warranty governance, SLA tracking, and operational incident command
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowNewTicketModal(true)}
            className="px-3.5 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-lg shadow-cyan-950/40 transition"
          >
            <Plus className="w-4 h-4" /> Submit Support Request
          </button>
          <button
            onClick={handleDetectOpportunities}
            className="px-3.5 py-1.5 bg-purple-600/20 hover:bg-purple-600/40 text-purple-300 border border-purple-500/30 rounded-lg text-xs font-bold flex items-center gap-1.5 transition"
          >
            <Sparkles className="w-4 h-4" /> AI Expansion Scan
          </button>
          <button
            onClick={loadData}
            disabled={loading}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-800 pb-3 overflow-x-auto text-xs">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-2 rounded-lg font-bold transition flex items-center gap-2 shrink-0 ${
            activeTab === 'overview'
              ? 'bg-cyan-600 text-white'
              : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
          }`}
        >
          <Activity className="w-4 h-4" /> Overview & Health
        </button>
        <button
          onClick={() => setActiveTab('requests')}
          className={`px-4 py-2 rounded-lg font-bold transition flex items-center gap-2 shrink-0 ${
            activeTab === 'requests'
              ? 'bg-cyan-600 text-white'
              : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
          }`}
        >
          <LifeBuoy className="w-4 h-4" /> Support Tickets ({requests.length})
        </button>
        <button
          onClick={() => setActiveTab('incidents')}
          className={`px-4 py-2 rounded-lg font-bold transition flex items-center gap-2 shrink-0 ${
            activeTab === 'incidents'
              ? 'bg-cyan-600 text-white'
              : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
          }`}
        >
          <AlertOctagon className="w-4 h-4" /> Incidents ({incidents.length})
        </button>
        <button
          onClick={() => setActiveTab('maintenance')}
          className={`px-4 py-2 rounded-lg font-bold transition flex items-center gap-2 shrink-0 ${
            activeTab === 'maintenance'
              ? 'bg-cyan-600 text-white'
              : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
          }`}
        >
          <Wrench className="w-4 h-4" /> Maintenance & Work Orders ({workOrders.length})
        </button>
        <button
          onClick={() => setActiveTab('kb')}
          className={`px-4 py-2 rounded-lg font-bold transition flex items-center gap-2 shrink-0 ${
            activeTab === 'kb'
              ? 'bg-cyan-600 text-white'
              : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
          }`}
        >
          <BookOpen className="w-4 h-4" /> Knowledge Base ({articles.length})
        </button>
        <button
          onClick={() => setActiveTab('opportunities')}
          className={`px-4 py-2 rounded-lg font-bold transition flex items-center gap-2 shrink-0 ${
            activeTab === 'opportunities'
              ? 'bg-cyan-600 text-white'
              : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
          }`}
        >
          <TrendingUp className="w-4 h-4" /> Expansion Intelligence ({opportunities.length})
        </button>
      </div>

      {/* Tab Panels */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <SupportDashboardOverview
            activeTicketsCount={requests.filter((r) => r.status !== 'RESOLVED' && r.status !== 'CLOSED').length}
            openIncidentsCount={incidents.filter((i) => i.status !== 'RESOLVED' && i.status !== 'CLOSED').length}
            activeWarrantyCount={warranties.filter((w) => w.status === 'ACTIVE').length}
            healthScore={health?.health_score || 94.0}
            healthStatus={health?.health_status || 'HEALTHY'}
            maintenanceOrdersDueCount={workOrders.filter((w) => w.status === 'PLANNED').length}
          />
          <SupportRequestTracker requests={requests} onRefresh={loadData} />
        </div>
      )}

      {activeTab === 'requests' && (
        <SupportRequestTracker requests={requests} onRefresh={loadData} />
      )}

      {activeTab === 'incidents' && (
        <IncidentManager incidents={incidents} onRefresh={loadData} />
      )}

      {activeTab === 'maintenance' && (
        <MaintenanceWorkOrderPanel
          plans={maintenancePlans}
          workOrders={workOrders}
          onRefresh={loadData}
        />
      )}

      {activeTab === 'kb' && (
        <KnowledgeBaseViewer articles={articles} onRefresh={loadData} />
      )}

      {activeTab === 'opportunities' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-purple-400" />
                Account Expansion & Continuous Value Intelligence
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                AI opportunities identified from ticket recurrence, performance bottlenecks, and usage trends
              </p>
            </div>
            <button
              onClick={handleDetectOpportunities}
              className="px-3 py-1.5 bg-purple-600 hover:bg-purple-500 text-white rounded-lg text-xs font-semibold"
            >
              Re-scan Intelligence
            </button>
          </div>

          {opportunities.length === 0 ? (
            <div className="text-center py-10 border border-dashed border-slate-800 rounded-xl">
              <TrendingUp className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p className="text-xs text-slate-400">No expansion opportunities detected yet. Run scan to evaluate.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {opportunities.map((opp) => (
                <div key={opp.id} className="p-4 bg-slate-950 rounded-xl border border-purple-500/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/30">
                      {opp.opportunity_type}
                    </span>
                    <span className="text-[10px] font-mono text-emerald-400">
                      Confidence: {(opp.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-white">{opp.title}</h4>
                  <p className="text-xs text-slate-400 mt-1">{opp.description}</p>
                  <div className="mt-3 pt-2 border-t border-slate-800 text-[11px] text-slate-500 flex justify-between">
                    <span>Status: {opp.status}</span>
                    {opp.estimated_value && (
                      <span className="text-emerald-400 font-bold">
                        ${opp.estimated_value.toLocaleString()}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}


      {/* Submit Support Request Modal */}
      {showNewTicketModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <LifeBuoy className="w-5 h-5 text-cyan-400" />
              Submit Support Request
            </h3>
            <form onSubmit={handleCreateTicket} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Ticket Subject</label>
                <input
                  type="text"
                  required
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Export feature returns 500 error on PDF generation"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Detailed Description</label>
                <textarea
                  required
                  rows={4}
                  value={newDesc}
                  onChange={(e) => setNewDesc(e.target.value)}
                  placeholder="Provide steps to reproduce, expected vs actual behavior, error messages..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                />
              </div>
              <div className="flex justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowNewTicketModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submittingTicket}
                  className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg font-bold"
                >
                  {submittingTicket ? 'Submitting...' : 'Submit Ticket'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
