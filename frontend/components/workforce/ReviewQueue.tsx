'use client';

import React, { useState } from 'react';
import { UserCheck, ShieldAlert, CheckCircle2, XCircle, AlertTriangle, FileText } from 'lucide-react';

interface ReviewItem {
  review_id: string;
  task_code: string;
  objective: string;
  worker_code?: string;
  supervision_level: number;
  triggers: string[];
  status: string;
  created_at: string;
}

interface ReviewQueueProps {
  pendingReviews: ReviewItem[];
  onResolveReview?: (reviewId: string, approved: boolean, rationale: string) => Promise<void>;
}

export const ReviewQueue: React.FC<ReviewQueueProps> = ({ pendingReviews, onResolveReview }) => {
  const [selectedReviewId, setSelectedReviewId] = useState<string | null>(null);
  const [rationale, setRationale] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleResolve = async (reviewId: string, approved: boolean) => {
    if (!onResolveReview) return;
    setIsSubmitting(true);
    try {
      await onResolveReview(reviewId, approved, rationale || 'Executive review completed.');
      setSelectedReviewId(null);
      setRationale('');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-xl border border-amber-500/20 bg-gradient-to-r from-slate-900/90 via-amber-950/20 to-slate-900/90">
        <div>
          <div className="flex items-center gap-2">
            <UserCheck className="h-5 w-5 text-amber-400" />
            <h2 className="text-lg font-bold text-white tracking-tight">AI Workforce Human Review Queue</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Supervision Level 4 & 5 gates. Tasks with low confidence, elevated risk, external communications, or sensitive scope require explicit executive ratification.
          </p>
        </div>
        <div className="px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-xs font-bold text-amber-300">
          {pendingReviews.length} Pending Actions
        </div>
      </div>

      {/* Review Queue Items */}
      {pendingReviews.length === 0 ? (
        <div className="p-10 text-center rounded-xl border border-dashed border-slate-700/60 bg-slate-900/40 text-slate-500 text-xs">
          <CheckCircle2 className="mx-auto h-8 w-8 text-emerald-500 mb-2" />
          <span>All workforce tasks are clear. No pending human review items.</span>
        </div>
      ) : (
        <div className="space-y-4">
          {pendingReviews.map((item) => (
            <div
              key={item.review_id}
              className="p-5 rounded-xl border border-amber-500/30 bg-slate-900/70 space-y-3"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <span className="text-[10px] font-mono text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                    Review ID: {item.review_id}
                  </span>
                  <h3 className="text-sm font-bold text-white mt-1">{item.objective}</h3>
                </div>
                <div className="text-xs text-slate-400">
                  Worker: <span className="text-indigo-300 font-semibold">{item.worker_code}</span> (L{item.supervision_level})
                </div>
              </div>

              {/* Triggers */}
              <div className="p-3 rounded-lg bg-amber-950/20 border border-amber-500/20 text-xs space-y-1">
                <div className="text-[10px] uppercase font-bold text-amber-400 flex items-center gap-1">
                  <AlertTriangle className="h-3 w-3" />
                  Review Triggers:
                </div>
                {item.triggers.map((trig, idx) => (
                  <div key={idx} className="text-amber-200/90 text-xs">
                    • {trig}
                  </div>
                ))}
              </div>

              {/* Action Box */}
              <div className="pt-2 border-t border-slate-800 space-y-2">
                <textarea
                  value={selectedReviewId === item.review_id ? rationale : ''}
                  onChange={(e) => {
                    setSelectedReviewId(item.review_id);
                    setRationale(e.target.value);
                  }}
                  placeholder="Enter approval rationale or feedback instructions..."
                  className="w-full h-16 rounded-lg bg-slate-950/80 border border-slate-700/80 p-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />

                <div className="flex justify-end gap-2">
                  <button
                    disabled={isSubmitting}
                    onClick={() => handleResolve(item.review_id, false)}
                    className="px-3.5 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-300 text-xs font-semibold flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
                  >
                    <XCircle className="h-3.5 w-3.5" />
                    Reject / Request Rework
                  </button>
                  <button
                    disabled={isSubmitting}
                    onClick={() => handleResolve(item.review_id, true)}
                    className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold flex items-center gap-1.5 shadow-md shadow-emerald-600/20 cursor-pointer disabled:opacity-50"
                  >
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Authorize Execution
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
