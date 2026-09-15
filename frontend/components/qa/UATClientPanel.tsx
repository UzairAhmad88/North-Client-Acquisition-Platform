'use client';

import React, { useState } from 'react';
import { UATSession, submitUATFeedback, signoffUATSession } from '@/lib/api/qa';
import { ShieldCheck, MessageSquare, CheckCircle2, Sparkles, KeyRound } from 'lucide-react';

interface UATClientPanelProps {
  uatSessions: UATSession[];
  projectId: string;
  onRefresh: () => void;
}

export const UATClientPanel: React.FC<UATClientPanelProps> = ({ uatSessions, projectId, onRefresh }) => {
  const activeSession = uatSessions[0];
  const [comments, setComments] = useState('');
  const [feedbackType, setFeedbackType] = useState('COMMENT');
  const [submittingFeedback, setSubmittingFeedback] = useState(false);

  const [signerId, setSignerId] = useState('Client Representative');
  const [statement, setStatement] = useState('I hereby grant formal User Acceptance Testing (UAT) sign-off for the delivered deliverables.');
  const [signingOff, setSigningOff] = useState(false);

  const handleFeedback = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeSession || !comments) return;
    setSubmittingFeedback(true);
    try {
      await submitUATFeedback(activeSession.id, {
        comments,
        feedback_type: feedbackType,
        create_defect_if_issue: feedbackType === 'ISSUE',
      });
      setComments('');
      onRefresh();
      alert('UAT feedback submitted successfully.');
    } catch (err: any) {
      alert(err?.message || 'Failed to submit feedback.');
    } finally {
      setSubmittingFeedback(false);
    }
  };

  const handleSignoff = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeSession || !statement) return;
    setSigningOff(true);
    try {
      await signoffUATSession(activeSession.id, {
        client_signer_id: signerId,
        signoff_statement: statement,
      });
      onRefresh();
      alert('Formal UAT sign-off recorded with SHA-256 hash.');
    } catch (err: any) {
      alert(err?.message || 'Failed to record sign-off.');
    } finally {
      setSigningOff(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Client User Acceptance Testing (UAT) Portal</h2>
            <p className="text-xs text-slate-400">Submit UAT feedback, report issues, and grant SHA-256 verified acceptance</p>
          </div>
        </div>

        {activeSession?.approved_by_client && (
          <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-bold flex items-center space-x-1.5">
            <CheckCircle2 className="w-4 h-4" />
            <span>UAT APPROVED BY CLIENT</span>
          </span>
        )}
      </div>

      {activeSession ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left Column: Feedback Form */}
          <div className="bg-slate-950 border border-slate-800 rounded-lg p-5 space-y-4">
            <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
              <MessageSquare className="w-4 h-4 text-blue-400" />
              <span>Submit UAT Feedback or Issue</span>
            </h3>

            <form onSubmit={handleFeedback} className="space-y-3">
              <div>
                <label className="text-xs text-slate-400 block mb-1">Feedback Type</label>
                <select
                  value={feedbackType}
                  onChange={(e) => setFeedbackType(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
                >
                  <option value="COMMENT">General Comment</option>
                  <option value="ISSUE">Report Issue (Auto-creates Defect)</option>
                  <option value="APPROVAL">Deliverable Approval Note</option>
                </select>
              </div>

              <div>
                <label className="text-xs text-slate-400 block mb-1">Feedback Comments</label>
                <textarea
                  required
                  rows={3}
                  value={comments}
                  onChange={(e) => setComments(e.target.value)}
                  placeholder="Enter acceptance observations or defect details..."
                  className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
                />
              </div>

              <button
                type="submit"
                disabled={submittingFeedback}
                className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs font-semibold shadow-lg"
              >
                {submittingFeedback ? 'Submitting...' : 'Submit Feedback'}
              </button>
            </form>
          </div>

          {/* Right Column: Formal Sign-off Form */}
          <div className="bg-slate-950 border border-slate-800 rounded-lg p-5 space-y-4">
            <h3 className="text-sm font-bold text-slate-200 flex items-center space-x-2">
              <KeyRound className="w-4 h-4 text-emerald-400" />
              <span>Formal Client UAT Sign-off</span>
            </h3>

            {activeSession.approved_by_client ? (
              <div className="bg-emerald-950/30 border border-emerald-800/40 rounded-lg p-4 space-y-2 text-xs text-emerald-300">
                <p className="font-semibold">Sign-off Granted & Verified</p>
                <p className="text-[11px] text-slate-400">Signed on {new Date(activeSession.client_signoff_at || '').toLocaleString()}</p>
                <p className="font-mono text-[10px] bg-slate-900 p-2 rounded text-emerald-400 border border-slate-800">
                  SHA-256 Content Verification Active
                </p>
              </div>
            ) : (
              <form onSubmit={handleSignoff} className="space-y-3">
                <div>
                  <label className="text-xs text-slate-400 block mb-1">Signer Name / Title</label>
                  <input
                    type="text"
                    required
                    value={signerId}
                    onChange={(e) => setSignerId(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="text-xs text-slate-400 block mb-1">Formal Acceptance Statement</label>
                  <textarea
                    required
                    rows={3}
                    value={statement}
                    onChange={(e) => setStatement(e.target.value)}
                    className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none"
                  />
                </div>

                <button
                  type="submit"
                  disabled={signingOff}
                  className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-semibold shadow-lg"
                >
                  {signingOff ? 'Signing off...' : 'Submit Formal UAT Acceptance'}
                </button>
              </form>
            )}
          </div>
        </div>
      ) : (
        <div className="py-8 text-center text-xs text-slate-500">
          No active UAT session initiated for this project.
        </div>
      )}
    </div>
  );
};
