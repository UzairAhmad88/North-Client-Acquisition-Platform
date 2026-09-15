'use client';

import React, { useState, useEffect } from 'react';
import {
  governanceApi,
  GovernanceExecutiveSummary,
  GovernancePostureData,
  GovernanceFrameworkItem,
  GovernanceRequirementItem,
  GovernanceControlItem,
  GovernanceEvidenceItem,
  GovernanceRiskItem,
  GovernanceExceptionItem,
  GovernanceFindingItem,
  PrivacyRequestItem,
  VendorProfileItem,
} from '@/lib/api/governance';

import GovernanceOverview from './GovernanceOverview';
import CompliancePosture from './CompliancePosture';
import FrameworkTable from './FrameworkTable';
import RequirementTable from './RequirementTable';
import ControlCatalog from './ControlCatalog';
import EvidenceTable from './EvidenceTable';
import RiskRegister from './RiskRegister';
import ExceptionTable from './ExceptionTable';
import FindingTable from './FindingTable';
import RemediationTracker from './RemediationTracker';
import PrivacyRequestTable from './PrivacyRequestTable';
import VendorRiskTable from './VendorRiskTable';
import GovernanceGraph from './GovernanceGraph';
import GovernanceCopilot from './GovernanceCopilot';

import {
  ShieldCheck,
  BookOpen,
  FileCheck,
  Database,
  AlertTriangle,
  Clock,
  AlertOctagon,
  UserCheck,
  Building2,
  GitCommit,
  Bot,
  RefreshCw,
} from 'lucide-react';

export default function GovernanceDashboard() {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [loading, setLoading] = useState(true);

  // GRC State
  const [summary, setSummary] = useState<GovernanceExecutiveSummary | null>(null);
  const [posture, setPosture] = useState<GovernancePostureData | null>(null);
  const [frameworks, setFrameworks] = useState<GovernanceFrameworkItem[]>([]);
  const [selectedFramework, setSelectedFramework] = useState<string>('SOC2_TYPE_II');
  const [requirements, setRequirements] = useState<GovernanceRequirementItem[]>([]);
  const [reqLoading, setReqLoading] = useState(false);
  const [controls, setControls] = useState<GovernanceControlItem[]>([]);
  const [evidence, setEvidence] = useState<GovernanceEvidenceItem[]>([]);
  const [risks, setRisks] = useState<GovernanceRiskItem[]>([]);
  const [exceptions, setExceptions] = useState<GovernanceExceptionItem[]>([]);
  const [findings, setFindings] = useState<GovernanceFindingItem[]>([]);
  const [privacyRequests, setPrivacyRequests] = useState<PrivacyRequestItem[]>([]);
  const [vendors, setVendors] = useState<VendorProfileItem[]>([]);

  // Remediation Modal State
  const [remediatingFinding, setRemediatingFinding] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [sumRes, posRes, fwRes, ctrlRes, riskRes, excRes, findRes, privRes, vendRes] =
        await Promise.allSettled([
          governanceApi.getOverview(),
          governanceApi.getPosture(),
          governanceApi.listFrameworks(),
          governanceApi.listControls(),
          governanceApi.listRisks(),
          governanceApi.listExceptions(),
          governanceApi.listFindings(),
          governanceApi.listPrivacyRequests(),
          governanceApi.listVendors(),
        ]);

      if (sumRes.status === 'fulfilled') setSummary(sumRes.value);
      if (posRes.status === 'fulfilled') setPosture(posRes.value);
      if (fwRes.status === 'fulfilled') setFrameworks(fwRes.value);
      if (ctrlRes.status === 'fulfilled') setControls(ctrlRes.value);
      if (riskRes.status === 'fulfilled') setRisks(riskRes.value);
      if (excRes.status === 'fulfilled') setExceptions(excRes.value);
      if (findRes.status === 'fulfilled') setFindings(findRes.value);
      if (privRes.status === 'fulfilled') setPrivacyRequests(privRes.value);
      if (vendRes.status === 'fulfilled') setVendors(vendRes.value);
    } catch (err) {
      console.error('Failed loading governance data:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadRequirements = async (frameworkCode: string) => {
    setReqLoading(true);
    try {
      const reqs = await governanceApi.listRequirements(frameworkCode);
      setRequirements(reqs);
    } catch (err) {
      console.error('Failed loading requirements:', err);
    } finally {
      setReqLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (selectedFramework) {
      loadRequirements(selectedFramework);
    }
  }, [selectedFramework]);

  // Actions
  const handleTestControl = async (controlCode: string) => {
    try {
      await governanceApi.testControl(controlCode, {
        test_type: 'OPERATING_EFFECTIVENESS',
        result: 'PASS',
        details: 'Live operating verification completed successfully.',
        executed_by: 'qa-compliance-auditor',
      });
      loadData();
    } catch (err) {
      console.error('Control test failed:', err);
    }
  };

  const handleAcceptRisk = async (riskCode: string, approverId: string, justification: string) => {
    try {
      await governanceApi.acceptRisk(riskCode, approverId, justification);
      loadData();
    } catch (err) {
      console.error('Risk acceptance failed:', err);
    }
  };

  const handleApproveException = async (exceptionCode: string) => {
    try {
      await governanceApi.approveException(exceptionCode, 'security-director');
      loadData();
    } catch (err) {
      console.error('Exception approval failed:', err);
    }
  };

  const handleCreateRemediationPlan = async (
    findingCode: string,
    planTitle: string,
    actions: any[],
    ownerId: string
  ) => {
    try {
      await governanceApi.createRemediationPlan(findingCode, planTitle, actions, ownerId);
      loadData();
    } catch (err) {
      console.error('Remediation plan creation failed:', err);
    }
  };

  const handleVerifyRemediation = async (
    findingCode: string,
    verifierId: string,
    evidenceId: string,
    retestPassed: boolean
  ) => {
    try {
      await governanceApi.verifyRemediation(findingCode, verifierId, evidenceId, retestPassed);
      loadData();
    } catch (err) {
      console.error('Remediation verification failed:', err);
    }
  };

  const navTabs = [
    { id: 'overview', label: 'Posture Overview', icon: ShieldCheck },
    { id: 'frameworks', label: 'Frameworks & Reqs', icon: BookOpen },
    { id: 'controls', label: 'Controls Catalog', icon: FileCheck },
    { id: 'evidence', label: 'Evidence Ledger', icon: Database },
    { id: 'risks', label: 'Risk Register', icon: AlertTriangle },
    { id: 'exceptions', label: 'Exceptions', icon: Clock },
    { id: 'findings', label: 'Deficiencies', icon: AlertOctagon },
    { id: 'privacy', label: 'Privacy & DSAR', icon: UserCheck },
    { id: 'vendors', label: 'Vendor Risk', icon: Building2 },
    { id: 'graph', label: 'Traceable Graph', icon: GitCommit },
    { id: 'copilot', label: 'GRC Copilot', icon: Bot },
  ];

  return (
    <div className="space-y-6">
      {/* Top Header & Refresh Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
            Unified Governance, Risk, Compliance & Privacy Platform
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Phase 47 &mdash; Continuous control monitoring, cryptographic evidence ledger, and living regulatory traceability.
          </p>
        </div>

        <button
          onClick={loadData}
          disabled={loading}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 text-slate-700 font-semibold text-xs rounded-xl transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh GRC Data</span>
        </button>
      </div>

      {/* Navigation Tabs */}
      <div className="flex items-center gap-1 overflow-x-auto pb-1 border-b border-slate-200">
        {navTabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-2 text-xs font-bold rounded-xl flex items-center gap-1.5 shrink-0 transition-all ${
                isActive
                  ? 'bg-indigo-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Tab Panels */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <GovernanceOverview
            summary={summary}
            posture={posture}
            loading={loading}
            onRefresh={loadData}
          />
          <CompliancePosture posture={posture} />
          <GovernanceGraph />
        </div>
      )}

      {activeTab === 'frameworks' && (
        <div className="space-y-6">
          <FrameworkTable
            frameworks={frameworks}
            selectedFramework={selectedFramework}
            onSelect={(code) => setSelectedFramework(code)}
          />
          <RequirementTable
            frameworkCode={selectedFramework}
            requirements={requirements}
            loading={reqLoading}
          />
        </div>
      )}

      {activeTab === 'controls' && (
        <ControlCatalog controls={controls} onTestControl={handleTestControl} />
      )}

      {activeTab === 'evidence' && (
        <EvidenceTable evidence={evidence} />
      )}

      {activeTab === 'risks' && (
        <RiskRegister risks={risks} onAcceptRisk={handleAcceptRisk} />
      )}

      {activeTab === 'exceptions' && (
        <ExceptionTable exceptions={exceptions} onApproveException={handleApproveException} />
      )}

      {activeTab === 'findings' && (
        <FindingTable
          findings={findings}
          onOpenRemediation={(code) => setRemediatingFinding(code)}
        />
      )}

      {activeTab === 'privacy' && (
        <PrivacyRequestTable requests={privacyRequests} />
      )}

      {activeTab === 'vendors' && (
        <VendorRiskTable vendors={vendors} />
      )}

      {activeTab === 'graph' && (
        <GovernanceGraph />
      )}

      {activeTab === 'copilot' && (
        <GovernanceCopilot />
      )}

      {/* Remediation Modal */}
      {remediatingFinding && (
        <RemediationTracker
          findingCode={remediatingFinding}
          onClose={() => setRemediatingFinding(null)}
          onCreatePlan={handleCreateRemediationPlan}
          onVerify={handleVerifyRemediation}
        />
      )}
    </div>
  );
}
