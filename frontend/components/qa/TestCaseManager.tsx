'use client';

import React, { useState } from 'react';
import { TestPlan, TestCase, generateAITestCases, createTestRun } from '@/lib/api/qa';
import { FileCode, Sparkles, Play, Plus, CheckCircle2, Shield } from 'lucide-react';

interface TestCaseManagerProps {
  testPlans: TestPlan[];
  projectId: string;
  onRefresh: () => void;
}

export const TestCaseManager: React.FC<TestCaseManagerProps> = ({ testPlans, projectId, onRefresh }) => {
  const [selectedPlanId, setSelectedPlanId] = useState<string>(testPlans[0]?.id || '');
  const [generating, setGenerating] = useState(false);
  const [startingRun, setStartingRun] = useState(false);

  const activePlan = testPlans.find((p) => p.id === selectedPlanId) || testPlans[0];

  const handleGenerateCases = async () => {
    if (!activePlan) return;
    setGenerating(true);
    try {
      await generateAITestCases(activePlan.id);
      onRefresh();
    } catch (err: any) {
      alert(err?.message || 'Failed to generate AI test cases.');
    } finally {
      setGenerating(false);
    }
  };

  const handleStartRun = async () => {
    if (!activePlan) return;
    setStartingRun(true);
    try {
      await createTestRun(projectId, {
        test_plan_id: activePlan.id,
        name: `Automated Execution - ${new Date().toLocaleDateString()}`,
        environment: 'STAGING',
      });
      onRefresh();
      alert('Test run initiated successfully.');
    } catch (err: any) {
      alert(err?.message || 'Failed to start test run.');
    } finally {
      setStartingRun(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-blue-500/10 border border-blue-500/20 rounded-lg text-blue-400">
            <FileCode className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Test Plans & Suite Governance</h2>
            <p className="text-xs text-slate-400">Manage QA test suites, regression test cases, and AI generation</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleGenerateCases}
            disabled={generating || !activePlan}
            className="px-3.5 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-lg text-xs font-semibold shadow-lg transition flex items-center space-x-1.5 disabled:opacity-50"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>{generating ? 'Generating...' : 'AI Generate Cases'}</span>
          </button>

          <button
            onClick={handleStartRun}
            disabled={startingRun || !activePlan}
            className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-lg transition flex items-center space-x-1.5 disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>{startingRun ? 'Starting...' : 'Run Test Suite'}</span>
          </button>
        </div>
      </div>

      {/* Plan Selector Tabs */}
      {testPlans.length > 0 && (
        <div className="flex items-center space-x-2 overflow-x-auto pb-2">
          {testPlans.map((plan) => (
            <button
              key={plan.id}
              onClick={() => setSelectedPlanId(plan.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition border ${
                (activePlan?.id === plan.id)
                  ? 'bg-blue-600/20 border-blue-500 text-blue-300'
                  : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {plan.title} ({plan.test_cases?.length || 0})
            </button>
          ))}
        </div>
      )}

      {/* Test Cases Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
              <th className="py-2.5 px-3">Code</th>
              <th className="py-2.5 px-3">Title & Description</th>
              <th className="py-2.5 px-3">Category</th>
              <th className="py-2.5 px-3">Priority</th>
              <th className="py-2.5 px-3">Execution</th>
              <th className="py-2.5 px-3">Regression</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {activePlan?.test_cases && activePlan.test_cases.length > 0 ? (
              activePlan.test_cases.map((tc) => (
                <tr key={tc.id} className="hover:bg-slate-800/40 transition">
                  <td className="py-3 px-3 font-mono text-blue-400 font-semibold">{tc.code}</td>
                  <td className="py-3 px-3">
                    <div className="font-semibold text-slate-100">{tc.title}</div>
                    <div className="text-[10px] text-slate-400 mt-0.5 line-clamp-1">{tc.description}</div>
                  </td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-300 border border-slate-700">
                      {tc.category}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <span
                      className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        tc.priority === 'CRITICAL'
                          ? 'bg-red-500/10 text-red-400 border border-red-500/20'
                          : tc.priority === 'HIGH'
                          ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                          : 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                      }`}
                    >
                      {tc.priority}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-400 font-mono text-[10px]">{tc.execution_type}</td>
                  <td className="py-3 px-3">
                    {tc.is_regression ? (
                      <span className="text-emerald-400 text-[10px] font-semibold flex items-center space-x-1">
                        <CheckCircle2 className="w-3 h-3" /> <span>Yes</span>
                      </span>
                    ) : (
                      <span className="text-slate-500 text-[10px]">No</span>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={6} className="py-8 text-center text-slate-500">
                  No test cases drafted yet. Click <strong>AI Generate Cases</strong> to populate test suite.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
