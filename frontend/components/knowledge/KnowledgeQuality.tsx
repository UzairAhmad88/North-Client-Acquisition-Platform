'use client';

import React, { useState, useEffect } from 'react';
import { getKnowledgeQuality } from '@/lib/api/knowledge';
import {
  CheckCircle2,
  ShieldCheck,
  Clock,
  Layers,
  FileCheck,
  AlertTriangle,
  GitPullRequest,
  Sparkles,
} from 'lucide-react';

export default function KnowledgeQualityComponent() {
  const [quality, setQuality] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadQuality() {
      setLoading(true);
      try {
        const data = await getKnowledgeQuality();
        setQuality(data);
      } catch (err) {
        console.error('Failed to load knowledge quality:', err);
      } finally {
        setLoading(false);
      }
    }
    loadQuality();
  }, []);

  if (loading || !quality) {
    return (
      <div className="p-8 text-center text-slate-500 animate-pulse bg-white rounded-xl border border-slate-200">
        Evaluating organizational knowledge quality metrics...
      </div>
    );
  }

  const m = quality.metrics || {};

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            Knowledge Quality & Integrity Scorecard
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Section 39 & 72: Continuous measurement across Completeness, Authority, Freshness, Provenance, Consistency, and Uniqueness.
          </p>
        </div>

        <div className="text-right px-4 py-2 bg-emerald-50 rounded-xl border border-emerald-200">
          <div className="text-xs font-semibold text-emerald-800 uppercase">Composite Quality</div>
          <div className="text-2xl font-extrabold text-emerald-700">{quality.overall_quality_score}%</div>
        </div>
      </div>

      {/* Metrics Grid (Section 72) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200">
          <span className="text-xs text-slate-400 font-semibold block">Verified / Authoritative</span>
          <span className="text-2xl font-bold text-emerald-600">{m.verified_count ?? 0}</span>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200">
          <span className="text-xs text-slate-400 font-semibold block">Human Confirmed</span>
          <span className="text-2xl font-bold text-blue-600">{m.human_confirmed_count ?? 0}</span>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200">
          <span className="text-xs text-slate-400 font-semibold block">AI Inferred (Drafts)</span>
          <span className="text-2xl font-bold text-amber-600">{m.inferred_count ?? 0}</span>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200">
          <span className="text-xs text-slate-400 font-semibold block">Stale / Aging Items</span>
          <span className="text-2xl font-bold text-rose-600">{m.stale_count ?? 0}</span>
        </div>
      </div>

      {/* Quality Dimensions Detailed Bars */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <h4 className="text-sm font-bold text-slate-800 uppercase tracking-wider">Quality Dimension Scores</h4>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4 text-xs">
            <div>
              <div className="flex justify-between font-semibold text-slate-700 mb-1">
                <span>Completeness</span>
                <span>{quality.completeness_score}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                <div className="bg-indigo-600 h-2.5 rounded-full" style={{ width: `${quality.completeness_score}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between font-semibold text-slate-700 mb-1">
                <span>Authority & Verification</span>
                <span>{quality.authority_score}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                <div className="bg-emerald-600 h-2.5 rounded-full" style={{ width: `${quality.authority_score}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between font-semibold text-slate-700 mb-1">
                <span>Provenance Traceability</span>
                <span>{quality.provenance_score}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${quality.provenance_score}%` }} />
              </div>
            </div>
          </div>

          <div className="space-y-4 text-xs">
            <div>
              <div className="flex justify-between font-semibold text-slate-700 mb-1">
                <span>Freshness & Lifespan</span>
                <span>{quality.freshness_score}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                <div className="bg-teal-600 h-2.5 rounded-full" style={{ width: `${quality.freshness_score}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between font-semibold text-slate-700 mb-1">
                <span>Consistency (Absence of Contradictions)</span>
                <span>{quality.consistency_score}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                <div className="bg-amber-500 h-2.5 rounded-full" style={{ width: `${quality.consistency_score}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between font-semibold text-slate-700 mb-1">
                <span>Uniqueness (Hash Deduplication)</span>
                <span>{quality.uniqueness_score}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
                <div className="bg-purple-600 h-2.5 rounded-full" style={{ width: `${quality.uniqueness_score}%` }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
