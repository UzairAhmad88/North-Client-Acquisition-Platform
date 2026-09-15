'use client';

import React, { useState, useEffect } from 'react';
import {
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Activity,
  Play,
  TrendingUp,
  ShieldAlert,
  Search,
  Sparkles,
  RotateCcw,
} from 'lucide-react';
import { dataApi, DataQualityRun, DataConflict } from '@/lib/api/data';

export default function DataQualityDashboard() {
  const [runs, setRuns] = useState<DataQualityRun[]>([]);
  const [conflicts, setConflicts] = useState<DataConflict[]>([]);
  const [loading, setLoading] = useState(true);
  const [evaluating, setEvaluating] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState<DataQualityRun | null>(null);

  // Sample data to test live evaluation
  const [samplePayload, setSamplePayload] = useState(
    JSON.stringify(
      [
        { id: 'REC-101', name: 'Acme Corp', email: 'contact@acme.com', confidence_score: 0.95 },
        { id: 'REC-102', name: 'Beta Tech', email: 'beta@tech.io', confidence_score: 0.88 },
        { id: 'REC-103', name: '', email: 'invalid-email', confidence_score: 0.2 },
      ],
      null,
      2
    )
  );

  const loadData = async () => {
    try {
      setLoading(true);
      const [runsData, conflictsData] = await Promise.all([
        dataApi.listQualityRuns(),
        dataApi.listConflicts(),
      ]);
      setRuns(runsData || []);
      setConflicts(conflictsData || []);
    } catch (err) {
      console.error('Failed to load quality data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRunEvaluation = async () => {
    try {
      setEvaluating(true);
      const parsedRecords = JSON.parse(samplePayload);
      const res = await dataApi.evaluateQuality({
        records: parsedRecords,
      });
      setEvaluationResult(res);
      loadData();
    } catch (err) {
      console.error('Evaluation failed', err);
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Data Quality, Integrity & Contradiction Monitor
          </h2>
          <p className="text-sm text-slate-400">
            Multi-dimensional data scoring, automated duplicate detection, and source contradiction resolution.
          </p>
        </div>

        <button
          onClick={loadData}
          className="inline-flex items-center px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-lg border border-slate-700"
        >
          <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
          Refresh Stats
        </button>
      </div>

      {/* 7 Quality Dimensions Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        {[
          { name: 'Completeness', score: '98%', status: 'optimal' },
          { name: 'Accuracy', score: '95%', status: 'optimal' },
          { name: 'Consistency', score: '92%', status: 'warning' },
          { name: 'Freshness', score: '99%', status: 'optimal' },
          { name: 'Validity', score: '94%', status: 'optimal' },
          { name: 'Uniqueness', score: '97%', status: 'optimal' },
          { name: 'Provenance', score: '100%', status: 'optimal' },
        ].map((dim) => (
          <div
            key={dim.name}
            className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center shadow-md"
          >
            <span className="text-xs text-slate-400 font-medium block truncate">{dim.name}</span>
            <span className="text-lg font-bold text-white mt-1 block">{dim.score}</span>
            <span
              className={`inline-block w-2 h-2 rounded-full mt-2 ${
                dim.status === 'optimal' ? 'bg-emerald-400' : 'bg-amber-400'
              }`}
            />
          </div>
        ))}
      </div>

      {/* Interactive Quality Evaluator */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <h3 className="text-base font-bold text-white">Live Data Quality Evaluation Sandbox</h3>
          </div>
          <button
            onClick={handleRunEvaluation}
            disabled={evaluating}
            className="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-semibold rounded-xl shadow transition-all"
          >
            <Play className="w-3.5 h-3.5 mr-1.5" />
            {evaluating ? 'Evaluating...' : 'Run Quality Audit'}
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              JSON Records Input:
            </label>
            <textarea
              rows={7}
              value={samplePayload}
              onChange={(e) => setSamplePayload(e.target.value)}
              className="w-full font-mono text-xs p-3 bg-slate-950 border border-slate-800 rounded-xl text-slate-300 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
            {evaluationResult ? (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-400">Calculated Overall Score:</span>
                  <span
                    className={`text-sm font-bold px-2 py-0.5 rounded ${
                      evaluationResult.overall_score >= 0.85
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                    }`}
                  >
                    {(evaluationResult.overall_score * 100).toFixed(1)}% (
                    {evaluationResult.status})
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div className="bg-slate-900 p-2 rounded border border-slate-800 text-center">
                    <span className="text-slate-500 block">Evaluated</span>
                    <span className="font-bold text-white">
                      {evaluationResult.total_records_evaluated}
                    </span>
                  </div>
                  <div className="bg-slate-900 p-2 rounded border border-slate-800 text-center">
                    <span className="text-slate-500 block">Passed</span>
                    <span className="font-bold text-emerald-400">
                      {evaluationResult.passed_records}
                    </span>
                  </div>
                  <div className="bg-slate-900 p-2 rounded border border-slate-800 text-center">
                    <span className="text-slate-500 block">Failed</span>
                    <span className="font-bold text-rose-400">
                      {evaluationResult.failed_records}
                    </span>
                  </div>
                </div>

                <div>
                  <span className="text-xs text-slate-400 font-medium block mb-1">
                    Violations Detected:
                  </span>
                  {evaluationResult.violations && evaluationResult.violations.length > 0 ? (
                    <div className="space-y-1 max-h-24 overflow-y-auto pr-1">
                      {evaluationResult.violations.map((v: any, idx: number) => (
                        <div
                          key={idx}
                          className="text-xs p-1.5 bg-rose-500/10 border border-rose-500/20 rounded text-rose-300 flex items-center gap-1.5"
                        >
                          <AlertTriangle className="w-3 h-3 text-rose-400 flex-shrink-0" />
                          <span>{v.message || JSON.stringify(v)}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-emerald-400 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5" /> No schema or quality violations found!
                    </p>
                  )}
                </div>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-slate-500 text-xs text-center py-6">
                <Activity className="w-8 h-8 text-slate-700 mb-2" />
                <p>Click &quot;Run Quality Audit&quot; to test real-time validation.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Contradictions & Conflicts Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-bold text-white">Source Contradictions & Conflicts</h3>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-medium">
            {conflicts.length} Pending Resolution
          </span>
        </div>

        {conflicts.length === 0 ? (
          <div className="p-6 bg-slate-950/50 border border-slate-800/80 rounded-xl text-center text-slate-400 text-xs">
            <CheckCircle2 className="w-6 h-6 text-emerald-400 mx-auto mb-1.5" />
            No active data contradictions or unmerged conflicts detected across domains.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider">
                <tr>
                  <th className="p-3">Entity Domain / ID</th>
                  <th className="p-3">Type</th>
                  <th className="p-3">Conflicting Fields</th>
                  <th className="p-3">Status</th>
                  <th className="p-3">Detected At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {conflicts.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-800/50">
                    <td className="p-3 font-mono font-medium text-white">
                      {c.domain} / {c.entity_id}
                    </td>
                    <td className="p-3">{c.conflict_type}</td>
                    <td className="p-3">
                      {c.conflicting_fields.map((f, i) => (
                        <span
                          key={i}
                          className="mr-1 px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]"
                        >
                          {f}
                        </span>
                      ))}
                    </td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 text-[10px] font-semibold">
                        {c.status}
                      </span>
                    </td>
                    <td className="p-3 text-slate-500">
                      {new Date(c.detected_at).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
