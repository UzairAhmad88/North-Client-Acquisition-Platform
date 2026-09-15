import React from 'react';

export const EvaluationBenchmarksJudgeView: React.FC = () => {
  const suites = [
    {
      name: 'Customer Churn Risk Golden Benchmark v2',
      type: 'GOLDEN_DATASET',
      target: 'CLASSIFICATION',
      testCases: 10000,
      score: '94.8%',
      passed: true,
      metrics: { Accuracy: '94.8%', Precision: '94.2%', Recall: '94.1%', 'ROC-AUC': '0.985' },
    },
    {
      name: 'Executive RAG Synthesis Faithfulness Benchmark',
      type: 'LLM_AS_JUDGE (Claude 3.5 Sonnet)',
      target: 'LLM_GENERATION',
      testCases: 250,
      score: '96.2%',
      passed: true,
      metrics: { Faithfulness: '96.2%', Groundedness: '95.0%', Toxicity: '0.001%', Hallucination: '0.8%' },
    },
    {
      name: 'Prompt Injection & Safety Red-Team Suite',
      type: 'SAFETY_RED_TEAM',
      target: 'AGENT_GUARDRAILS',
      testCases: 500,
      score: '99.6%',
      passed: true,
      metrics: { 'Jailbreak Defense': '99.6%', 'PII Leakage': '0.00%', 'Tool Sandbox Security': '100.0%' },
    },
  ];

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 backdrop-blur-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-100">Unified Evaluation & LLM-as-a-Judge Radar</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Golden benchmark test suites, LLM judge scoring, and Safety/Red-Team vulnerability thresholds.
          </p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-mono">
          All Gates Passed
        </span>
      </div>

      <div className="space-y-3">
        {suites.map((suite, idx) => (
          <div key={idx} className="p-4 rounded-lg bg-slate-800/40 border border-slate-700/60 space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <h4 className="text-sm font-semibold text-white">{suite.name}</h4>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-300">
                    {suite.type}
                  </span>
                  <span className="text-xs text-slate-500">• {suite.testCases.toLocaleString()} Test Cases</span>
                </div>
              </div>
              <div className="text-right">
                <span className="text-base font-bold text-emerald-400">{suite.score}</span>
                <p className="text-[10px] font-mono text-emerald-300">✓ GATE PASSED</p>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 pt-2 border-t border-slate-700/40 text-xs">
              {Object.entries(suite.metrics).map(([key, val]) => (
                <div key={key} className="bg-slate-900/40 p-2 rounded border border-slate-800/80">
                  <span className="text-slate-500 text-[10px] uppercase font-mono">{key}</span>
                  <p className="font-bold text-slate-200">{val}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
