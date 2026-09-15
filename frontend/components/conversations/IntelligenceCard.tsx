'use client';

import React, { useState } from 'react';
import { ConversationAnalysis, recordCorrection } from '@/lib/api/conversations';

interface IntelligenceCardProps {
  conversationId: string;
  analysis: ConversationAnalysis | null;
  onRefresh?: () => void;
}

export function IntelligenceCard({ conversationId, analysis, onRefresh }: IntelligenceCardProps) {
  const [showCorrectionModal, setShowCorrectionModal] = useState(false);
  const [correctedIntent, setCorrectedIntent] = useState('');
  const [correctedNextAction, setCorrectedNextAction] = useState('');
  const [reason, setReason] = useState('');
  const [loading, setLoading] = useState(false);

  if (!analysis) {
    return (
      <div className="p-4 rounded-xl bg-zinc-900 border border-zinc-800 text-xs text-zinc-400 text-center">
        No conversation intelligence analysis available yet.
      </div>
    );
  }

  const handleSaveCorrection = async () => {
    if (!reason.trim()) return;
    setLoading(true);
    try {
      await recordCorrection(conversationId, correctedIntent || undefined, correctedNextAction || undefined, reason);
      setShowCorrectionModal(false);
      setReason('');
      if (onRefresh) onRefresh();
    } catch (err) {
      console.error('Failed to record correction:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-5 rounded-xl bg-zinc-900 border border-zinc-800 space-y-4 text-xs">
      <div className="flex justify-between items-center pb-3 border-b border-zinc-800">
        <div>
          <h3 className="font-bold text-zinc-100 text-sm">Response & Conversation Intelligence</h3>
          <p className="text-zinc-400 text-[11px]">Stage: <span className="text-indigo-400 font-semibold">{analysis.conversation_stage}</span></p>
        </div>
        <button
          onClick={() => setShowCorrectionModal(true)}
          className="px-2.5 py-1 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-[11px] border border-zinc-700"
        >
          Correct Analysis
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="p-3 rounded-lg bg-zinc-950 border border-zinc-800 space-y-1">
          <span className="text-[10px] text-zinc-400 block uppercase font-bold">Detected Intent</span>
          <span className="font-bold text-emerald-400 text-xs">{analysis.primary_intent}</span>
          <p className="text-[10px] text-zinc-500">Confidence: {analysis.intent_confidence}</p>
        </div>

        <div className="p-3 rounded-lg bg-zinc-950 border border-zinc-800 space-y-1">
          <span className="text-[10px] text-zinc-400 block uppercase font-bold">Recommended Next Action</span>
          <span className="font-bold text-indigo-400 text-xs">{analysis.recommended_next_action}</span>
          {analysis.recommended_next_action_reason && (
            <p className="text-[10px] text-zinc-400 italic">{analysis.recommended_next_action_reason}</p>
          )}
        </div>
      </div>

      {analysis.buying_signal_level !== 'NONE' && (
        <div className="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300">
          <span className="font-bold">Buying Signal Level: {analysis.buying_signal_level}</span>
        </div>
      )}

      {analysis.objection_type && (
        <div className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300">
          <span className="font-bold">Detected Objection: {analysis.objection_type}</span>
        </div>
      )}

      {analysis.extracted_requirements && analysis.extracted_requirements.length > 0 && (
        <div className="space-y-1">
          <span className="text-[10px] font-bold text-zinc-400 uppercase">Extracted Requirements</span>
          <div className="flex flex-wrap gap-1.5">
            {analysis.extracted_requirements.map((req, idx) => (
              <span key={idx} className="px-2 py-0.5 rounded bg-zinc-800 border border-zinc-700 text-zinc-200 text-[11px]">
                {req.category}: {req.item}
              </span>
            ))}
          </div>
        </div>
      )}

      {analysis.human_correction && (
        <div className="p-2.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 space-y-1">
          <span className="font-bold">Human Operator Correction Applied</span>
          <p className="text-[11px]">Reason: "{analysis.human_correction.reason}"</p>
        </div>
      )}

      {showCorrectionModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-zinc-900 border border-zinc-800 p-5 rounded-xl max-w-md w-full space-y-3">
            <h4 className="text-sm font-bold text-zinc-100">Correct AI Intelligence Classification</h4>
            <div>
              <label className="text-[11px] text-zinc-400 block mb-1">Corrected Intent</label>
              <input
                type="text"
                value={correctedIntent}
                onChange={(e) => setCorrectedIntent(e.target.value)}
                placeholder="e.g. REQUEST_FOR_MEETING"
                className="w-full p-2 bg-zinc-950 border border-zinc-800 rounded text-xs text-zinc-200"
              />
            </div>
            <div>
              <label className="text-[11px] text-zinc-400 block mb-1">Corrected Next Action</label>
              <input
                type="text"
                value={correctedNextAction}
                onChange={(e) => setCorrectedNextAction(e.target.value)}
                placeholder="e.g. SCHEDULE_MEETING"
                className="w-full p-2 bg-zinc-950 border border-zinc-800 rounded text-xs text-zinc-200"
              />
            </div>
            <div>
              <label className="text-[11px] text-zinc-400 block mb-1">Correction Reason</label>
              <input
                type="text"
                required
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="Why is this correction necessary?"
                className="w-full p-2 bg-zinc-950 border border-zinc-800 rounded text-xs text-zinc-200"
              />
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setShowCorrectionModal(false)}
                className="px-3 py-1.5 rounded bg-zinc-800 text-zinc-300 text-xs"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveCorrection}
                disabled={loading || !reason.trim()}
                className="px-3 py-1.5 rounded bg-indigo-600 text-white text-xs hover:bg-indigo-500 disabled:opacity-50"
              >
                Save Correction
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
