'use client';

import React, { useState } from 'react';
import { GitCommit, ArrowRight, ShieldCheck, Database, CheckCircle2, Wrench, Layers, AlertTriangle } from 'lucide-react';

export default function GovernanceGraph() {
  const [activeNode, setActiveNode] = useState<number>(0);

  const steps = [
    {
      title: '1. Regulatory Requirement',
      code: 'CC6.1 / Art. 32',
      desc: 'Mandates strict logical access restrictions & multi-factor protection across tenant boundaries.',
      domain: 'REGULATION',
    },
    {
      title: '2. Governance Policy',
      code: 'POL-ACCESS-001',
      desc: 'Enterprise Identity & Logical Access Control Policy v2.1 approved by CISO and Legal counsel.',
      domain: 'POLICY',
    },
    {
      title: '3. Technical Control',
      code: 'CTRL-IAM-MFA',
      desc: 'Multi-factor authentication enforced for all administrative and programmatic operations.',
      domain: 'CONTROL',
    },
    {
      title: '4. System Implementation',
      code: 'Phase 35 IAM / RBAC',
      desc: 'Implemented in backend/app/auth/rbac.py & OAuth/WebAuthn session verification middleware.',
      domain: 'CODE_IMPLEMENTATION',
    },
    {
      title: '5. Cryptographic Evidence',
      code: 'EVD-AUTH-DAILY-001',
      desc: 'Immutable audit telemetry digest (SHA-256) proving 100% MFA compliance over past 24 hours.',
      domain: 'EVIDENCE',
    },
    {
      title: '6. Automated Test',
      code: 'TEST-IAM-OPERATING',
      desc: 'Operating effectiveness test run evaluating 1,240 session handshakes without bypass.',
      domain: 'TESTING',
    },
    {
      title: '7. Deficiency / Finding',
      code: 'FND-TENANT-LEAK-01',
      desc: 'Occasional legacy endpoint query missing explicit tenant filter; flagged for priority fix.',
      domain: 'FINDINGS',
    },
    {
      title: '8. Remediation & Retest',
      code: 'REM-PATCH-VERIFY',
      desc: 'Strict query scope applied; independent QA retest verification succeeds (Rule 20 satisfied).',
      domain: 'REMEDIATION',
    },
  ];

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Layers className="w-5 h-5 text-indigo-600" />
            <span>Cross-System Traceable Governance Graph</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Living, auditable relationship from high-level statutory obligation to code execution & verified remediation.
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-indigo-50 text-indigo-700 rounded-lg">
          End-to-End Traceability
        </span>
      </div>

      {/* Interactive Traceability Ribbon */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
        {steps.map((step, idx) => {
          const isSelected = activeNode === idx;
          return (
            <button
              key={idx}
              onClick={() => setActiveNode(idx)}
              className={`p-3 rounded-xl border text-left transition-all ${
                isSelected
                  ? 'bg-indigo-600 text-white border-indigo-700 shadow-sm scale-102'
                  : 'bg-slate-50 border-slate-200 hover:bg-indigo-50/50 text-slate-800'
              }`}
            >
              <div className={`text-[10px] font-bold uppercase tracking-wider ${isSelected ? 'text-indigo-200' : 'text-slate-400'}`}>
                {step.domain}
              </div>
              <div className="text-xs font-bold mt-1 line-clamp-1">{step.code}</div>
            </button>
          );
        })}
      </div>

      {/* Selected Step Detail Panel */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-slate-900 to-indigo-950 text-white border border-slate-800 space-y-2">
        <div className="flex items-center gap-2 text-xs text-indigo-300 font-bold uppercase">
          <span>Node {activeNode + 1} of {steps.length}</span>
          <span>&bull;</span>
          <span>{steps[activeNode].domain}</span>
        </div>
        <div className="text-lg font-bold">{steps[activeNode].title} &mdash; <span className="text-indigo-400 font-mono">{steps[activeNode].code}</span></div>
        <p className="text-xs text-slate-300 max-w-3xl leading-relaxed">
          {steps[activeNode].desc}
        </p>
      </div>
    </div>
  );
}
