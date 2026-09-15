"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  addDncEntry,
  DncEntry,
  listDncEntries,
  listOutreachDrafts,
  OutreachDraft,
} from "@/lib/api/outreach";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function OutreachPage() {
  const [activeTab, setActiveTab] = useState<"DRAFTS" | "DNC">("DRAFTS");
  const [drafts, setDrafts] = useState<OutreachDraft[]>([]);
  const [dncList, setDncList] = useState<DncEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>("PENDING_APPROVAL");

  // Add DNC Modal state
  const [dncScope, setDncScope] = useState("EMAIL");
  const [dncTarget, setDncTarget] = useState("");
  const [dncReason, setDncReason] = useState("");

  const fetchDrafts = async () => {
    setLoading(true);
    setError(null);
    try {
      if (activeTab === "DRAFTS") {
        const res = await listOutreachDrafts(filterStatus);
        setDrafts(res.data);
      } else {
        const res = await listDncEntries();
        setDncList(res.data);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load outreach data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDrafts();
  }, [filterStatus, activeTab]);

  const handleAddDnc = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!dncTarget.trim()) return;
    try {
      await addDncEntry(dncScope, dncTarget, dncReason);
      setDncTarget("");
      setDncReason("");
      fetchDrafts();
    } catch (err: any) {
      alert(err.message || "Failed to add DNC entry.");
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-black text-slate-900 dark:text-slate-100">Outreach Command Center</h1>
          <p className="text-xs text-slate-500 mt-1">
            Review evidence-backed communication drafts prepared by the Personalization Agent.
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant={activeTab === "DRAFTS" ? "default" : "outline"}
            size="sm"
            onClick={() => setActiveTab("DRAFTS")}
          >
            Outreach Drafts
          </Button>
          <Button
            variant={activeTab === "DNC" ? "default" : "outline"}
            size="sm"
            onClick={() => setActiveTab("DNC")}
          >
            Do-Not-Contact (DNC) Registry
          </Button>
        </div>
      </div>

      <div className="p-3 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-200 text-amber-900 dark:text-amber-200 text-xs font-semibold flex items-center justify-between">
        <span>🛡️ SAFETY BOUNDARY: Autonomous sending is strictly disabled. Drafts require human review & CommunicationGuard validation.</span>
        <span className="px-2 py-0.5 rounded bg-amber-200 dark:bg-amber-900 text-[10px] font-black">REAL_SEND = MOCK</span>
      </div>

      {error && (
        <div className="p-4 text-xs rounded-lg bg-rose-50 text-rose-700 border border-rose-200">
          {error}
        </div>
      )}

      {activeTab === "DRAFTS" ? (
        <>
          <div className="flex justify-between items-center text-xs">
            <span className="font-semibold text-slate-600 dark:text-slate-400">Filter Status:</span>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="p-1.5 rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs"
            >
              <option value="PENDING_APPROVAL">PENDING APPROVAL</option>
              <option value="APPROVED">APPROVED</option>
              <option value="ACCEPTED">SENT / ACCEPTED</option>
              <option value="DELIVERED">DELIVERED</option>
              <option value="REJECTED">REJECTED</option>
            </select>
          </div>

          {loading ? (
            <div className="p-8 text-center text-xs text-slate-400">Loading outreach drafts...</div>
          ) : drafts.length === 0 ? (
            <div className="p-12 text-center text-slate-500 border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-xl">
              No outreach drafts found matching filter &quot;{filterStatus}&quot;.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {drafts.map((d) => (
                <Card key={d.id} className="border border-slate-200 dark:border-slate-800 shadow-sm hover:border-slate-300 transition">
                  <CardHeader className="pb-2 flex flex-row items-center justify-between">
                    <div>
                      <CardTitle className="text-sm font-bold">
                        <Link href={`/outreach/${d.id}`} className="hover:underline text-indigo-600 dark:text-indigo-400">
                          {d.subject || "Untitled Draft"}
                        </Link>
                      </CardTitle>
                      <span className="text-[10px] text-slate-500">Channel: {d.channel} | Tone: {d.tone} | v{d.version}</span>
                    </div>
                    <span className="px-2 py-0.5 text-[10px] font-extrabold rounded bg-amber-100 text-amber-900 border border-amber-300">
                      {d.approval_status}
                    </span>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="p-2.5 bg-slate-50 dark:bg-slate-900 rounded text-xs text-slate-700 dark:text-slate-300 line-clamp-3 font-sans">
                      {d.body}
                    </div>
                    <div className="flex justify-between items-center text-[10px] text-slate-400">
                      <span>Risk Level: <strong className="text-slate-700 dark:text-slate-300">{d.risk_level}</strong></span>
                      <Link href={`/outreach/${d.id}`} className="text-indigo-600 hover:underline font-bold">
                        Inspect & Action &rarr;
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </>
      ) : (
        /* DNC Tab */
        <div className="space-y-6">
          <form onSubmit={handleAddDnc} className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 space-y-3 text-xs">
            <h3 className="font-bold text-slate-800 dark:text-slate-200">Add Entry to Do-Not-Contact (DNC) Registry</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <select
                value={dncScope}
                onChange={(e) => setDncScope(e.target.value)}
                className="p-2 rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800"
              >
                <option value="EMAIL">EMAIL</option>
                <option value="PHONE">PHONE</option>
                <option value="CONTACT">CONTACT UUID</option>
                <option value="BUSINESS">BUSINESS UUID</option>
                <option value="GLOBAL">GLOBAL</option>
              </select>
              <input
                type="text"
                required
                placeholder="Target value (e.g. email or phone)..."
                value={dncTarget}
                onChange={(e) => setDncTarget(e.target.value)}
                className="p-2 rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800"
              />
              <input
                type="text"
                placeholder="Reason..."
                value={dncReason}
                onChange={(e) => setDncReason(e.target.value)}
                className="p-2 rounded border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800"
              />
            </div>
            <Button type="submit" size="sm" className="bg-rose-600 text-white">Add DNC Entry</Button>
          </form>

          {loading ? (
            <div className="p-8 text-center text-xs text-slate-400">Loading DNC entries...</div>
          ) : dncList.length === 0 ? (
            <div className="p-8 text-center text-slate-400 border border-dashed rounded-xl text-xs">No entries in DNC registry.</div>
          ) : (
            <div className="space-y-2">
              {dncList.map((entry) => (
                <div key={entry.id} className="p-3 rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 flex justify-between items-center text-xs">
                  <div>
                    <span className="font-bold px-2 py-0.5 text-[10px] rounded bg-rose-100 text-rose-800 mr-2">{entry.scope}</span>
                    <span className="font-mono text-slate-800 dark:text-slate-200">{entry.target_value}</span>
                    {entry.reason && <span className="text-slate-500 ml-2">({entry.reason})</span>}
                  </div>
                  <span className="text-[10px] text-slate-400">{new Date(entry.created_at).toLocaleDateString()}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
