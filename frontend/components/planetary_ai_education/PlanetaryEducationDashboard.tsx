'use client';

import React, { useState } from 'react';

interface DashboardProps {
  initialTab?: string;
}

export default function PlanetaryEducationDashboard({ initialTab = 'command-center' }: DashboardProps) {
  const [activeTab, setActiveTab] = useState<string>(initialTab);
  const [tutorTopic, setTutorTopic] = useState('Kyber-768 Post-Quantum Key Exchange in Distributed Agent Networks');
  const [tutorMode, setTutorMode] = useState<string>('SOCRATIC');
  const [tutorOutput, setTutorOutput] = useState<any>(null);
  const [problemId, setProblemId] = useState('PROB-PQC-NTT-01');
  const [hintLevel, setHintLevel] = useState<number>(1);
  const [hintOutput, setHintOutput] = useState<any>(null);

  const stats = [
    { label: 'Active Amplified Learners', value: '12,450 Learners', change: 'Personalized Adaptive Paths', status: 'optimal' },
    { label: 'Mastery Completion Rate', value: '94.2% Mastery', change: 'Multi-Evidence Verified', status: 'optimal' },
    { label: 'Active Socratic Sessions', value: '1,840 Sessions', change: 'Active Recall & Spaced Repetition', status: 'optimal' },
    { label: 'Verified Competency Passports', value: '4,210 Proofs', change: 'Zero Fabricated Claims', status: 'optimal' },
    { label: 'Workforce Reskilling Index', value: '18.4 Low Gap', change: 'Future Skills Forecasted', status: 'optimal' },
    { label: 'Privacy & Minor Safety', value: '100% Governed', change: 'Data Minimization Enforced', status: 'optimal' },
  ];

  const profile = {
    targetRole: 'Principal AI & Autonomous Systems Architect',
    currentLevel: 'ADVANCED_PRACTITIONER',
    mode: 'SOCRATIC_INTERACTIVE',
    budget: '45 min / day',
    strengths: ['System Architecture', 'Zero-Trust Governance', 'Distributed Systems'],
    gaps: ['Post-Quantum Cryptographic Key Rotation', 'Sodium-Ion Battery Energy Kinetics']
  };

  const skills = [
    { id: 'skill-pqc-01', name: 'Post-Quantum Cryptography Key Migration', domain: 'SECURITY_CRYPTOGRAPHY', prerequisites: 'mTLS v1.3 Architecture, Key Exchange', knowledgeClaim: 'claim-pqc-kyber-01', difficulty: 8.8 },
    { id: 'skill-battery-kinetics-02', name: 'Solid-State Battery Energy Kinetics Modeling', domain: 'MATERIALS_SCIENCE', prerequisites: 'Molecular Dynamics, Electro-Thermo Dynamics', knowledgeClaim: 'claim-bio-901', difficulty: 8.5 },
  ];

  const passports = [
    { id: 'pass-01', skill: 'Planetary AI Systems Architecture', evidence: 'Phase 89 & 90 Production Infrastructure Deployment Proof', status: 'VERIFIED_PORTFOLIO_PROOF', issuer: 'Uzaii Learning Intelligence Fabric', aiGenerated: 'FALSE (Evidence-backed)' },
    { id: 'pass-02', skill: 'Autonomous B2B Commerce Protocol', evidence: 'Phase 87 & 88 M2M Settlement & Negotiation Logs', status: 'VERIFIED_PORTFOLIO_PROOF', issuer: 'Uzaii Learning Intelligence Fabric', aiGenerated: 'FALSE (Evidence-backed)' },
  ];

  const handleStartTutorSession = () => {
    let resp = '';
    if (tutorMode === 'SOCRATIC') {
      resp = `Let's explore ${tutorTopic}. Question: What primary performance bottleneck occurs when transitioning from mTLS v1.3 RSA keys to Kyber-768 Post-Quantum lattice keys in distributed agent networks?`;
    } else if (tutorMode === 'ANALOGY') {
      resp = `Think of ${tutorTopic} like exchanging signed passports at a border: lattice keys act like multi-dimensional holograms that quantum computers cannot counterfeit.`;
    } else {
      resp = `${tutorTopic} involves updating cryptographic key negotiation algorithms to lattice-based cryptography (e.g. CRYSTALS-Kyber), ensuring resistance against Shor's quantum factoring algorithm.`;
    }

    setTutorOutput({
      concept: tutorTopic,
      mode: tutorMode,
      response: resp,
      active_recall: "What is the key size difference between RSA-4096 and Kyber-768?",
      spaced_repetition: "3 Days"
    });
  };

  const handleGetHint = () => {
    const hints: Record<number, string> = {
      1: "Hint 1 (Conceptual): Inspect the key generation parameters in the lattice matrix initialization.",
      2: "Hint 2 (Implementation): Ensure polynomial multiplication uses Number Theoretic Transform (NTT) for O(n log n) efficiency.",
      3: "Hint 3 (Partial Guidance): Check if the error vector distribution follows the Discrete Gaussian noise distribution.",
      4: "Worked Solution: Review the complete NTT-accelerated Kyber keygen implementation in the verified crypto module."
    };

    setHintOutput({
      problem_id: problemId,
      level: hintLevel,
      content: hints[hintLevel] || hints[4],
      sandbox: "ISOLATED_CONTAINER_EVALUATION"
    });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Planetary AI Education & Human Capability Amplification OS
            </h1>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-950 text-blue-400 border border-blue-800">
              HUMAN AMPLIFICATION MESH ACTIVE
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Universal Learning Profiles • Skill Graph • Adaptive AI Tutor • STEM & Code Coaching • Competency Passports • Educator Copilot
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="px-3 py-1 bg-slate-900 border border-blue-800/60 rounded-lg text-xs font-medium text-blue-300">
            🛡️ Augmenting Human Agency (Zero Fabricated Qualifications)
          </span>
        </div>
      </div>

      {/* Stat Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
        {stats.map((s, idx) => (
          <div key={idx} className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between backdrop-blur-sm">
            <span className="text-xs font-medium text-slate-400">{s.label}</span>
            <div className="my-2">
              <span className="text-xl font-bold text-white">{s.value}</span>
            </div>
            <span className="text-xs text-blue-400">{s.change}</span>
          </div>
        ))}
      </div>

      {/* Tabs Navigation */}
      <div className="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
        {[
          { id: 'command-center', label: 'Human Amplification Command Center' },
          { id: 'profile', label: 'Universal Profile & Heatmap' },
          { id: 'skill-graph', label: 'Global Skill Graph' },
          { id: 'ai-tutor', label: 'Adaptive AI Tutor Workspace' },
          { id: 'stem-coaching', label: 'STEM & Code Coaching' },
          { id: 'passports', label: 'Competency Passports' },
          { id: 'teacher-copilot', label: 'Teacher Copilot & Lessons' },
          { id: 'workforce-reskilling', label: 'Workforce Reskilling' },
          { id: 'personal-rag', label: 'Personal Knowledge RAG' },
          { id: 'virtual-labs', label: 'Virtual Labs & Simulations' },
          { id: 'privacy-controls', label: 'Educational Privacy & Minor Safety' },
          { id: 'governance', label: 'Governance & Human Oversight' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white shadow-md shadow-blue-950'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Interactive Widgets Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Adaptive AI Tutor Workspace */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-blue-400">🎓</span> Adaptive AI Tutor (Socratic / Direct / Analogy)
            </h3>
            <div className="flex gap-1 text-[10px]">
              {['SOCRATIC', 'DIRECT_INSTRUCTION', 'ANALOGY'].map((m) => (
                <button
                  key={m}
                  onClick={() => setTutorMode(m)}
                  className={`px-2 py-0.5 rounded font-mono ${tutorMode === m ? 'bg-blue-600 text-white' : 'bg-slate-950 text-slate-400'}`}
                >
                  {m.split('_')[0]}
                </button>
              ))}
            </div>
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={tutorTopic}
              onChange={(e) => setTutorTopic(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleStartTutorSession}
              className="px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium rounded-lg transition-all"
            >
              Start Session
            </button>
          </div>

          {tutorOutput && (
            <div className="bg-slate-950 border border-blue-900/50 rounded-lg p-3 space-y-2 text-xs">
              <div className="flex justify-between text-blue-300 font-semibold border-b border-slate-800 pb-1">
                <span>Topic: {tutorOutput.concept}</span>
                <span className="text-cyan-400">{tutorOutput.mode}</span>
              </div>
              <p className="text-slate-300">{tutorOutput.response}</p>
              <div className="pt-2 border-t border-slate-900 text-slate-400 space-y-1">
                <p><strong className="text-slate-300">Active Recall Prompt:</strong> {tutorOutput.active_recall}</p>
                <p><strong className="text-slate-300">Spaced Repetition Review:</strong> {tutorOutput.spaced_repetition}</p>
              </div>
            </div>
          )}
        </div>

        {/* STEM & Code Coaching Hint Ladder */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <span className="text-cyan-400">💡</span> STEM & Code Coaching Hint Ladder
            </h3>
            <span className="text-xs text-slate-400">Progressive Scaffolding</span>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={problemId}
              onChange={(e) => setProblemId(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            />
            <select
              value={hintLevel}
              onChange={(e) => setHintLevel(Number(e.target.value))}
              className="bg-slate-950 border border-slate-800 rounded-lg px-2 py-2 text-xs text-slate-200"
            >
              <option value={1}>Hint 1</option>
              <option value={2}>Hint 2</option>
              <option value={3}>Hint 3</option>
              <option value={4}>Worked Solution</option>
            </select>
            <button
              onClick={handleGetHint}
              className="px-3 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-medium rounded-lg transition-all"
            >
              Get Hint
            </button>
          </div>

          {hintOutput ? (
            <div className="bg-slate-950 border border-cyan-900/50 rounded-lg p-3 space-y-1.5 text-xs">
              <div className="flex justify-between text-cyan-300 font-semibold border-b border-slate-800 pb-1">
                <span>Problem: {hintOutput.problem_id}</span>
                <span className="text-emerald-400">Level {hintOutput.level}</span>
              </div>
              <p className="text-slate-300 pt-1">{hintOutput.content}</p>
              <p className="text-slate-500 text-[10px] pt-1">Sandbox Isolation: {hintOutput.sandbox}</p>
            </div>
          ) : (
            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 text-center text-xs text-slate-500">
              Click &quot;Get Hint&quot; above to request progressive scaffolding or worked solutions.
            </div>
          )}
        </div>
      </div>

      {/* Main Tab Content Display */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 space-y-4">
        {activeTab === 'command-center' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Learner & Skill Overview</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2">
                <h4 className="text-xs font-semibold text-blue-400 uppercase tracking-wider">Learner Profile Summary</h4>
                <p className="text-xs text-slate-300"><strong className="text-slate-400">Target Role:</strong> {profile.targetRole}</p>
                <p className="text-xs text-slate-300"><strong className="text-slate-400">Current Level:</strong> {profile.currentLevel}</p>
                <p className="text-xs text-slate-300"><strong className="text-slate-400">Time Budget:</strong> {profile.budget}</p>
                <div className="pt-2 border-t border-slate-900">
                  <span className="text-xs font-semibold text-emerald-400">Strengths:</span>
                  <p className="text-xs text-slate-400">{profile.strengths.join(', ')}</p>
                </div>
              </div>

              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                <h4 className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-2">Verified Competency Passports</h4>
                <ul className="space-y-2 text-xs">
                  {passports.map((p) => (
                    <li key={p.id} className="flex justify-between items-center border-b border-slate-900 pb-1">
                      <span className="text-slate-200 font-medium">{p.skill}</span>
                      <span className="text-emerald-400 font-mono text-[10px]">{p.status}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'skill-graph' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Global Skill Graph (Connected to Phase 90 Knowledge Graph)</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Skill Name</th>
                    <th className="p-2.5">Domain</th>
                    <th className="p-2.5">Prerequisites</th>
                    <th className="p-2.5">Connected Knowledge Claim</th>
                    <th className="p-2.5">Difficulty</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {skills.map((s) => (
                    <tr key={s.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-semibold text-white">{s.name}</td>
                      <td className="p-2.5 font-mono text-blue-400">{s.domain}</td>
                      <td className="p-2.5 text-slate-300">{s.prerequisites}</td>
                      <td className="p-2.5 font-mono text-cyan-400 text-[10px]">{s.knowledgeClaim}</td>
                      <td className="p-2.5 font-bold text-amber-400">{s.difficulty} / 10</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'passports' && (
          <div className="space-y-4">
            <h3 className="text-base font-semibold text-white">Verified Competency Passports & Proof of Evidence</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="p-2.5">Skill Verified</th>
                    <th className="p-2.5">Demonstrated Evidence</th>
                    <th className="p-2.5">Issuer</th>
                    <th className="p-2.5">AI Attribution Status</th>
                    <th className="p-2.5">Verification</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {passports.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-800/40">
                      <td className="p-2.5 font-semibold text-white">{p.skill}</td>
                      <td className="p-2.5 text-slate-300 max-w-xs">{p.evidence}</td>
                      <td className="p-2.5 text-slate-400">{p.issuer}</td>
                      <td className="p-2.5 font-mono text-emerald-400 text-[10px]">{p.aiGenerated}</td>
                      <td className="p-2.5"><span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 text-[10px] font-bold">{p.status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {['profile', 'ai-tutor', 'stem-coaching', 'teacher-copilot', 'workforce-reskilling', 'personal-rag', 'virtual-labs', 'privacy-controls', 'governance'].includes(activeTab) && (
          <div className="space-y-3 py-4 text-center">
            <div className="inline-block p-3 rounded-full bg-slate-950 border border-slate-800 text-blue-400 mb-2 text-xl">
              🧠
            </div>
            <h4 className="text-sm font-semibold text-white capitalize">{activeTab.replace('-', ' ')} Suite Active</h4>
            <p className="text-xs text-slate-400 max-w-lg mx-auto">
              Human capability amplification, adaptive learning paths, and zero-trust educational privacy active for {activeTab}.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
