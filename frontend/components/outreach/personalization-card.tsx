"use client";

import React, { useState } from "react";
import {
  OutreachDraft,
  runPersonalizationAgent,
  updateOutreachDraft,
} from "@/lib/api/outreach";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface PersonalizationCardProps {
  leadId: string;
  initialDraft?: OutreachDraft | null;
  onUpdated?: (draft: OutreachDraft) => void;
}

export function PersonalizationCard({
  leadId,
  initialDraft,
  onUpdated,
}: PersonalizationCardProps) {
  const [draft, setDraft] = useState<OutreachDraft | null>(initialDraft || null);
  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);

  // Configuration options
  const [channel, setChannel] = useState<string>("EMAIL");
  const [tone, setTone] = useState<string>("PROFESSIONAL");
  const [depth, setDepth] = useState<string>("STANDARD");

  // Form states
  const [editSubject, setEditSubject] = useState("");
  const [editBody, setEditBody] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleRunPersonalization = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await runPersonalizationAgent(leadId, {
        channel,
        tone,
        personalization_depth: depth,
      });
      setDraft(res);
      setEditSubject(res.subject || "");
      setEditBody(res.body || "");
      if (onUpdated) onUpdated(res);
    } catch (err: any) {
      setError(err.message || "Failed to execute Personalization Agent");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!draft) return;
    setLoading(true);
    setError(null);
    try {
      const res = await updateOutreachDraft(draft.id, {
        subject: editSubject,
        body: editBody,
      });
      setDraft(res);
      setEditing(false);
      if (onUpdated) onUpdated(res);
    } catch (err: any) {
      setError(err.message || "Failed to update draft");
    } finally {
      setLoading(false);
    }
  };

  const getRiskBadge = (r: string) => {
    switch (r) {
      case "LOW":
        return <span className="px-2 py-0.5 text-[10px] font-bold rounded bg-emerald-100 text-emerald-800 border border-emerald-200">LOW RISK</span>;
      case "MEDIUM":
        return <span className="px-2 py-0.5 text-[10px] font-bold rounded bg-amber-100 text-amber-800 border border-amber-200">MEDIUM RISK</span>;
      case "HIGH":
        return <span className="px-2 py-0.5 text-[10px] font-bold rounded bg-rose-100 text-rose-800 border border-rose-200">HIGH RISK</span>;
      case "BLOCKED":
      default:
        return <span className="px-2 py-0.5 text-[10px] font-bold rounded bg-slate-200 text-slate-800 border border-slate-300">BLOCKED</span>;
    }
  };

  return (
    <Card className="shadow-md border border-slate-200 dark:border-slate-800">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3 border-b border-slate-100 dark:border-slate-800">
        <div>
          <CardTitle className="text-lg font-bold">Personalization & Communication Draft</CardTitle>
          <p className="text-xs text-slate-500 mt-1">
            AI-assisted, evidence-backed outreach context prepared for human review
          </p>
        </div>
        <div className="flex gap-2">
          {draft && !editing && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setEditing(true);
                setEditSubject(draft.subject || "");
                setEditBody(draft.body || "");
              }}
            >
              Edit Draft
            </Button>
          )}
          <Button
            size="sm"
            onClick={handleRunPersonalization}
            disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 text-white"
          >
            {loading ? "Generating..." : draft ? "Regenerate Draft" : "Run Personalization Agent"}
          </Button>
        </div>
      </CardHeader>

      <CardContent className="pt-4 space-y-4">
        {error && (
          <div className="p-3 text-xs rounded-lg bg-rose-50 text-rose-700 border border-rose-200 dark:bg-rose-950 dark:text-rose-300">
            {error}
          </div>
        )}

        {/* Configuration Bar */}
        <div className="flex flex-wrap gap-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 items-center justify-between">
          <div className="flex gap-2 items-center text-xs">
            <span className="font-semibold text-slate-600 dark:text-slate-400">Channel:</span>
            <select
              value={channel}
              onChange={(e) => setChannel(e.target.value)}
              className="rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 p-1 text-xs"
            >
              <option value="EMAIL">EMAIL</option>
              <option value="WHATSAPP">WHATSAPP</option>
              <option value="SMS">SMS</option>
              <option value="LINKEDIN">LINKEDIN</option>
            </select>

            <span className="font-semibold text-slate-600 dark:text-slate-400 ml-2">Tone:</span>
            <select
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              className="rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 p-1 text-xs"
            >
              <option value="PROFESSIONAL">PROFESSIONAL</option>
              <option value="FRIENDLY">FRIENDLY</option>
              <option value="CONCISE">CONCISE</option>
              <option value="CONSULTATIVE">CONSULTATIVE</option>
              <option value="LOCAL_BUSINESS">LOCAL_BUSINESS</option>
            </select>

            <span className="font-semibold text-slate-600 dark:text-slate-400 ml-2">Depth:</span>
            <select
              value={depth}
              onChange={(e) => setDepth(e.target.value)}
              className="rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 p-1 text-xs"
            >
              <option value="LIGHT">LIGHT</option>
              <option value="STANDARD">STANDARD</option>
              <option value="DEEP">DEEP</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
              SAFETY GUARANTEED: ZERO AUTONOMOUS SENDING
            </span>
          </div>
        </div>

        {!draft ? (
          <div className="p-6 text-center text-slate-500 text-sm border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-xl">
            No personalized outreach draft has been generated for this lead yet.
            <br />
            <span className="text-xs text-slate-400">
              Select desired channel and tone above, then click &quot;Run Personalization Agent&quot;.
            </span>
          </div>
        ) : (
          <>
            {/* Status Header */}
            <div className="flex items-center justify-between gap-4 p-3 rounded-lg bg-slate-100 dark:bg-slate-900">
              <div className="flex items-center gap-3">
                <span className="px-2.5 py-1 text-xs font-bold rounded bg-amber-100 text-amber-900 border border-amber-300 dark:bg-amber-950 dark:text-amber-200">
                  STATUS: {draft.approval_status}
                </span>
                <span className="text-xs text-slate-600 dark:text-slate-400">
                  Version: <strong className="text-slate-900 dark:text-white">v{draft.version}</strong>
                </span>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span>Risk Rating:</span>
                {getRiskBadge(draft.risk_level)}
              </div>
            </div>

            {/* Primary Communication Angle */}
            {draft.primary_angle && (
              <div className="p-3 rounded-lg bg-indigo-50/50 dark:bg-indigo-950/30 border border-indigo-100 dark:border-indigo-900/40">
                <h4 className="text-xs font-bold uppercase text-indigo-900 dark:text-indigo-300 mb-1">
                  Primary Angle: {draft.primary_angle.title || draft.primary_angle.angle_type}
                </h4>
                <p className="text-xs text-indigo-800 dark:text-indigo-200">
                  {draft.primary_angle.problem_statement}
                </p>
                <span className="block text-[11px] font-semibold text-indigo-700 dark:text-indigo-400 mt-1">
                  Value Prop: {draft.primary_angle.value_proposition}
                </span>
              </div>
            )}

            {/* Draft Content / Editor */}
            {editing ? (
              <form onSubmit={handleSaveEdit} className="space-y-3 p-4 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-950">
                <h4 className="text-xs font-bold uppercase text-slate-600 dark:text-slate-400">Edit Communication Draft</h4>
                {draft.channel === "EMAIL" && (
                  <div>
                    <label className="text-[11px] font-semibold block text-slate-600 mb-1">Subject</label>
                    <input
                      type="text"
                      value={editSubject}
                      onChange={(e) => setEditSubject(e.target.value)}
                      className="w-full p-2 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800"
                    />
                  </div>
                )}
                <div>
                  <label className="text-[11px] font-semibold block text-slate-600 mb-1">Body Content</label>
                  <textarea
                    rows={6}
                    value={editBody}
                    onChange={(e) => setEditBody(e.target.value)}
                    className="w-full p-2 text-xs rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 font-mono"
                  />
                </div>
                <div className="flex gap-2 justify-end">
                  <Button type="button" variant="outline" size="sm" onClick={() => setEditing(false)}>
                    Cancel
                  </Button>
                  <Button type="submit" size="sm" disabled={loading} className="bg-emerald-600 text-white">
                    Save Changes (Increments Version)
                  </Button>
                </div>
              </form>
            ) : (
              <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 space-y-3">
                {draft.subject && (
                  <div>
                    <span className="text-[11px] font-bold uppercase text-slate-400 tracking-wider">Subject</span>
                    <div className="text-sm font-bold text-slate-900 dark:text-slate-100">{draft.subject}</div>
                  </div>
                )}
                <div>
                  <span className="text-[11px] font-bold uppercase text-slate-400 tracking-wider">Draft Body ({draft.channel})</span>
                  <div className="text-xs text-slate-800 dark:text-slate-200 whitespace-pre-wrap leading-relaxed mt-1 font-sans p-3 bg-slate-50 dark:bg-slate-900 rounded-lg">
                    {draft.body}
                  </div>
                </div>
              </div>
            )}

            {/* Evidence & Claims Traceability */}
            {draft.evidence && draft.evidence.length > 0 && (
              <div>
                <h4 className="text-xs font-bold uppercase text-slate-500 tracking-wider mb-2">Supporting Evidence ({draft.evidence.length})</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {draft.evidence.map((ev, i) => (
                    <div key={i} className="p-2 text-[11px] rounded border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900">
                      <span className="font-bold text-slate-700 dark:text-slate-300">{ev.title || ev.type}: </span>
                      <span className="text-slate-600 dark:text-slate-400">{ev.description}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}
