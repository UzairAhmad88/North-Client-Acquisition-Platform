'use client';

import React, { useState, useEffect } from 'react';
import {
  processIntelligenceApi,
  ProcessOverview,
  ProcessDefinition,
  ProcessVariant,
  ProcessMap,
  ConformanceViolation,
  BottleneckRecord,
  ReworkRecord,
  AutomationCandidate,
  OptimizationProposal,
} from '@/lib/api/processIntelligence';
import ProcessOverviewComponent from './ProcessOverview';
import ProcessMapComponent from './ProcessMap';
import ProcessVariantTable from './ProcessVariantTable';
import ConformancePanel from './ConformancePanel';
import BottleneckTable from './BottleneckTable';
import CycleTimeChart from './CycleTimeChart';
import ReworkAnalysis from './ReworkAnalysis';
import AutomationCandidateTable from './AutomationCandidateTable';
import OptimizationProposalComponent from './OptimizationProposal';
import SimulationPanel from './SimulationPanel';
import DeploymentRollout from './DeploymentRollout';
import ProcessCopilot from './ProcessCopilot';
import {
  Layers,
  GitBranch,
  Repeat,
  AlertTriangle,
  Clock,
  Zap,
  Sliders,
  Cpu,
  GitPullRequest,
  Bot,
  RefreshCw,
} from 'lucide-react';

export default function ProcessDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [overview, setOverview] = useState<ProcessOverview | null>(null);
  const [processes, setProcesses] = useState<ProcessDefinition[]>([]);
  const [selectedProcessId, setSelectedProcessId] = useState<string>('');
  const [variants, setVariants] = useState<ProcessVariant[]>([]);
  const [processMap, setProcessMap] = useState<ProcessMap | null>(null);
  const [violations, setViolations] = useState<ConformanceViolation[]>([]);
  const [bottlenecks, setBottlenecks] = useState<BottleneckRecord[]>([]);
  const [reworkRecords, setReworkRecords] = useState<ReworkRecord[]>([]);
  const [candidates, setCandidates] = useState<AutomationCandidate[]>([]);
  const [proposals, setProposals] = useState<OptimizationProposal[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchInitialData = async () => {
    setLoading(true);
    try {
      const [ovData, procList] = await Promise.all([
        processIntelligenceApi.getOverview(),
        processIntelligenceApi.listProcesses(),
      ]);
      setOverview(ovData);
      setProcesses(procList);

      let targetId = selectedProcessId;
      if (!targetId && procList.length > 0) {
        targetId = procList[0].id;
        setSelectedProcessId(targetId);
      }

      if (targetId) {
        await fetchProcessDetails(targetId);
      }
    } catch (err) {
      console.error('Failed to load process intelligence data:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchProcessDetails = async (processId: string) => {
    try {
      const [vData, mapData, violData, btnData, rwkData, autoData, propData] = await Promise.all([
        processIntelligenceApi.getVariants(processId),
        processIntelligenceApi.getProcessMap(processId),
        processIntelligenceApi.getConformanceViolations(processId),
        processIntelligenceApi.getBottlenecks(processId),
        processIntelligenceApi.getReworkRecords(processId),
        processIntelligenceApi.getAutomationCandidates(processId),
        processIntelligenceApi.listOptimizationProposals(processId),
      ]);

      setVariants(vData);
      setProcessMap(mapData);
      setViolations(violData);
      setBottlenecks(btnData);
      setReworkRecords(rwkData);
      setCandidates(autoData);
      setProposals(propData);
    } catch (err) {
      console.error('Failed to fetch process details:', err);
    }
  };

  useEffect(() => {
    fetchInitialData();
  }, []);

  const handleProcessChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const pId = e.target.value;
    setSelectedProcessId(pId);
    if (pId) {
      await fetchProcessDetails(pId);
    }
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Layers },
    { id: 'map', label: 'Process Map', icon: GitBranch },
    { id: 'variants', label: 'Variants', icon: Repeat },
    { id: 'conformance', label: 'Conformance', icon: AlertTriangle },
    { id: 'bottlenecks', label: 'Bottlenecks', icon: Clock },
    { id: 'cycletime', label: 'Cycle-Time', icon: Clock },
    { id: 'rework', label: 'Rework Loops', icon: Repeat },
    { id: 'automation', label: 'Automation', icon: Zap },
    { id: 'optimization', label: 'Optimization', icon: Sliders },
    { id: 'simulation', label: 'What-If Simulation', icon: Cpu },
    { id: 'deployments', label: 'Canary Deployments', icon: GitPullRequest },
    { id: 'copilot', label: 'Copilot', icon: Bot },
  ];

  return (
    <div className="space-y-6">
      {/* Top Header & Process Selector */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2.5">
            <Layers className="w-7 h-7 text-indigo-400" /> Unified Process Intelligence & Mining
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Observe real execution traces &bull; Detect bottlenecks &bull; Simulate & optimize workflows under controlled governance
          </p>
        </div>

        <div className="flex items-center gap-3">
          {processes.length > 0 && (
            <select
              value={selectedProcessId}
              onChange={handleProcessChange}
              className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
            >
              {processes.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({p.domain})
                </option>
              ))}
            </select>
          )}

          <button
            onClick={fetchInitialData}
            className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition"
            title="Refresh Data"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="flex overflow-x-auto gap-2 border-b border-slate-800 pb-2">
        {tabs.map((t) => {
          const Icon = t.icon;
          const isActive = activeTab === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium whitespace-nowrap transition ${
                isActive
                  ? 'bg-indigo-600 text-white'
                  : 'bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800'
              }`}
            >
              <Icon className="w-4 h-4" />
              {t.label}
            </button>
          );
        })}
      </div>

      {/* Tab Panels */}
      {activeTab === 'overview' && <ProcessOverviewComponent overview={overview} />}
      {activeTab === 'map' && <ProcessMapComponent processMap={processMap} loading={loading} />}
      {activeTab === 'variants' && <ProcessVariantTable variants={variants} />}
      {activeTab === 'conformance' && <ConformancePanel violations={violations} />}
      {activeTab === 'bottlenecks' && <BottleneckTable bottlenecks={bottlenecks} />}
      {activeTab === 'cycletime' && <CycleTimeChart />}
      {activeTab === 'rework' && <ReworkAnalysis reworkRecords={reworkRecords} />}
      {activeTab === 'automation' && <AutomationCandidateTable candidates={candidates} />}
      {activeTab === 'optimization' && <OptimizationProposalComponent proposals={proposals} />}
      {activeTab === 'simulation' && <SimulationPanel processId={selectedProcessId} />}
      {activeTab === 'deployments' && <DeploymentRollout processId={selectedProcessId} />}
      {activeTab === 'copilot' && <ProcessCopilot processId={selectedProcessId} />}
    </div>
  );
}
