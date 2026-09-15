'use client';

import React, { useState, useEffect } from 'react';
import { listLessons, LessonItem } from '@/lib/api/knowledge';
import { Sparkles, CheckCircle, XCircle, AlertCircle, Search, Lightbulb } from 'lucide-react';

export default function LessonLibraryComponent() {
  const [lessons, setLessons] = useState<LessonItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    async function loadLessons() {
      setLoading(true);
      try {
        const data = await listLessons();
        setLessons(data);
      } catch (err) {
        console.error('Failed to load lessons:', err);
      } finally {
        setLoading(false);
      }
    }
    loadLessons();
  }, []);

  const filtered = lessons.filter(
    (l) =>
      l.title.toLowerCase().includes(filter.toLowerCase()) ||
      l.problem.toLowerCase().includes(filter.toLowerCase()) ||
      l.recommendation.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-amber-500" />
            Organizational Lessons Learned & Retrospectives
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Section 30: Captured operational insights from completed projects and incident postmortems feeding future estimation and risk controls.
          </p>
        </div>

        <div className="relative w-full md:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Filter lessons..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-500 animate-pulse bg-white rounded-xl border border-slate-200">
          Loading organizational lessons library...
        </div>
      ) : filtered.length === 0 ? (
        <div className="p-8 text-center bg-white rounded-xl border border-slate-200 text-slate-500 text-sm">
          No matching lessons found.
        </div>
      ) : (
        <div className="space-y-4">
          {filtered.map((l) => (
            <div key={l.lesson_code} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-xs font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded">
                      {l.lesson_code}
                    </span>
                    <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                      {l.applicability_domain}
                    </span>
                    <span className="text-xs text-slate-400">Scope: {l.context_scope}</span>
                  </div>
                  <h4 className="text-base font-bold text-slate-900">{l.title}</h4>
                </div>
                <div className="text-xs font-semibold text-slate-500">
                  Confidence: {Math.round(l.confidence * 100)}%
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="bg-rose-50/60 p-3 rounded-xl border border-rose-100 space-y-1">
                  <span className="font-bold text-rose-800 flex items-center gap-1">
                    <XCircle className="w-3.5 h-3.5 text-rose-600" />
                    Problem & Root Cause
                  </span>
                  <p className="text-rose-900">{l.problem}</p>
                  <p className="text-rose-700 italic text-[11px] mt-1">Cause: {l.root_cause}</p>
                </div>

                <div className="bg-emerald-50/60 p-3 rounded-xl border border-emerald-100 space-y-1">
                  <span className="font-bold text-emerald-800 flex items-center gap-1">
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                    What Worked & Resolution
                  </span>
                  <p className="text-emerald-900">{l.what_worked}</p>
                </div>
              </div>

              <div className="p-3.5 bg-indigo-50/70 border border-indigo-100 rounded-xl text-xs space-y-1">
                <span className="font-bold text-indigo-900 flex items-center gap-1.5">
                  <Lightbulb className="w-3.5 h-3.5 text-indigo-600" />
                  Canonical Recommendation for Future Projects
                </span>
                <p className="text-indigo-950 font-medium leading-relaxed">{l.recommendation}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
