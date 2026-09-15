"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  approveOutreachDraft,
  getOutreachDraft,
  getOutreachEvents,
  OutreachDraft,
  OutreachEventItem,
  rejectOutreachDraft,
  sendOutreachDraft,
} from "@/lib/api/outreach";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { getOutreachDraftRisk, RiskAssessment } from "@/lib/api/risk";
import { RiskPanel } from "@/components/risk/RiskPanel";

export default function OutreachDetailPage() {
  const params = useParams();
  const draftId = params.id as string;

  const [draft, setDraft] = useState<OutreachDraft | null>(null);
  const [events, setEvents] = useState<OutreachEventItem[]>([]);
  const [riskAssessment, setRiskAssessment] = useState<RiskAssessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Reject Modal
  const [rejectOpen, setRejectOpen] = useState(false);
  const [rejectReason, setRejectReason] = useState("");

  const fetchDetail = useCallback(async () => {
    if (!draftId) return;
    setLoading(true);
    setError(null);
    try {
      const d = await getOutreachDraft(draftId);
      setDraft(d);
      const evs = await getOutreachEvents(draftId);
      setEvents(evs);
      try {
        const r = await getOutreachDraftRisk(draftId);
        setRiskAssessment(r);
      } catch {
        setRiskAssessment(null);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load outreach draft detail.");
    } finally {
      setLoading(false);
    }
  }, [draftId]);

  useEffect(() => {
    fetchDetail();
  }, [fetchDetail]);

  const handleApprove = async () => {
    setActionLoading(true);
    setError(null);
    try {
      const res = await approveOutreachDraft(draftId);
      setDraft(res);
      fetchDetail();
    } catch (err: any) {
      setError(err.message || "Failed to approve draft.");
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!rejectReason.trim()) return;
    setActionLoading(true);
    setError(null);
    try {
      const res = await rejectOutreachDraft(draftId, rejectReason);
      setDraft(res);
      setRejectOpen(false);
      fetchDetail();
    } catch (err: any) {
      setError(err.message || "Failed to reject draft.");
    } finally {
      setActionLoading(false);
    }
  };

  const handleSend = async () => {
    if (!confirm("Are you sure you want to invoke CommunicationGuard and send this outreach?")) return;
    setActionLoading(true);
    setError(null);
    try {
      const res = await sendOutreachDraft(draftId);
      setDraft(res);
      fetchDetail();
    } catch (err: any) {
      setError(err.message || "Guarded send failed.");
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-xs text-slate-500">Loading draft details...</div>;
  }

  if (error && !draft) {
    return <div className="p-8 text-center text-xs text-rose-600 bg-rose-50 border border-rose-200">{error}</div>;
  }

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <div className="flex justify-between items-center border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <Link href="/outreach" className="hover:underline">Outreach Command Center</Link>
            <span>/</span>
            <span>Draft Inspector</span>
          </div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-slate-100 mt-1">
            Outreach Draft: {draft?.subject || "Untitled Draft"}
          </h1>
        </div>
        <div className="flex gap-2">
          {draft?.approval_status === "PENDING_APPROVAL" && (
            <>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setRejectOpen(!rejectOpen)}
                disabled={actionLoading}
                className="text-rose-600 border-rose-300 hover:bg-rose-50"
              >
                Reject
              </Button>
              <Button
                size="sm"
                onClick={handleApprove}
                disabled={actionLoading}
                className="bg-emerald-600 hover:bg-emerald-700 text-white"
              >
                Approve (Bind Content Hash)
              </Button>
            </>
          )}
          {draft?.approval_status === "APPROVED" && (
            <Button
              size="sm"
              onClick={handleSend}
              disabled={actionLoading}
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold"
            >
              {actionLoading ? "Sending..." : "Send Approved Outreach (Guarded)"}
            </Button>
          )}
        </div>
      </div>

      {error && (
        <div className="p-3 text-xs rounded bg-rose-50 text-rose-700 border border-rose-200">
          {error}
        </div>
      )}

      {rejectOpen && (
        <form onSubmit={handleReject} className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3 text-xs">
          <h4 className="font-bold text-slate-800">Reject Outreach Draft</h4>
          <input
            type="text"
            required
            placeholder="Reason for rejection..."
            value={rejectReason}
            onChange={(e) => setRejectReason(e.target.value)}
            className="w-full p-2 text-xs rounded border border-slate-300"
          />
          <div className="flex justify-end gap-2">
            <Button type="button" variant="outline" size="sm" onClick={() => setRejectOpen(false)}>Cancel</Button>
            <Button type="submit" size="sm" className="bg-rose-600 text-white">Confirm Reject</Button>
          </div>
        </form>
      )}

      {/* Metadata & Status Card */}
      <Card>
        <CardContent className="pt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div>
            <span className="text-slate-400 block">Approval Status</span>
            <span className="font-extrabold text-indigo-700 dark:text-indigo-300">{draft?.approval_status}</span>
          </div>
          <div>
            <span className="text-slate-400 block">Draft Version</span>
            <span className="font-bold">v{draft?.version}</span>
          </div>
          <div>
            <span className="text-slate-400 block">Channel & Tone</span>
            <span className="font-semibold">{draft?.channel} ({draft?.tone})</span>
          </div>
          <div>
            <span className="text-slate-400 block">Risk Rating</span>
            <span className="font-bold text-emerald-600">{draft?.risk_level}</span>
          </div>
          {draft?.content_hash && (
            <div className="col-span-2 md:col-span-4 pt-2 border-t border-slate-100 dark:border-slate-800">
              <span className="text-[10px] text-slate-400 block font-mono">Bound Content Hash (SHA-256):</span>
              <span className="text-[11px] font-mono text-slate-700 dark:text-slate-300 select-all">{draft.content_hash}</span>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Risk & Quality Engine Inspector Panel */}
      <RiskPanel draftId={draftId} assessment={riskAssessment} onRefresh={fetchDetail} />

      {/* Draft Content Card */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-bold">Draft Content</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-xs">
          {draft?.subject && (
            <div>
              <span className="font-bold text-slate-500 block mb-1">Subject</span>
              <div className="p-2.5 bg-slate-50 dark:bg-slate-900 rounded font-semibold text-slate-800 dark:text-slate-200">
                {draft.subject}
              </div>
            </div>
          )}
          <div>
            <span className="font-bold text-slate-500 block mb-1">Body</span>
            <div className="p-3 bg-slate-50 dark:bg-slate-900 rounded text-slate-800 dark:text-slate-200 font-sans whitespace-pre-wrap leading-relaxed">
              {draft?.body}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Event Timeline */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-bold">Audit Event Timeline ({events.length})</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {events.length === 0 ? (
            <div className="text-xs text-slate-400 p-3">No timeline events logged yet.</div>
          ) : (
            events.map((ev) => (
              <div key={ev.id} className="p-2.5 rounded bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800 text-xs flex justify-between items-center">
                <div>
                  <span className="font-bold text-indigo-600 dark:text-indigo-400 mr-2">{ev.event_type}</span>
                  <span className="text-slate-600 dark:text-slate-400">{JSON.stringify(ev.details)}</span>
                </div>
                <span className="text-[10px] text-slate-400">{new Date(ev.created_at).toLocaleString()}</span>
              </div>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
}
