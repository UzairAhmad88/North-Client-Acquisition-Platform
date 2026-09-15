"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  AgentRunDetail,
  getAgentRunDetail,
  cancelAgentRun,
} from "@/lib/api/agents";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, ArrowLeft, Bot, Shield, AlertCircle, CheckCircle2, Clock, Ban } from "lucide-react";

export default function AgentRunDetailPage() {
  const params = useParams();
  const runId = params.id as string;

  const [run, setRun] = useState<AgentRunDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [cancelling, setCancelling] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRunDetail = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getAgentRunDetail(runId);
      setRun(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load agent run detail.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (runId) {
      fetchRunDetail();
    }
  }, [runId]);

  const handleCancel = async () => {
    if (!confirm("Are you sure you want to cancel this agent run?")) return;
    try {
      setCancelling(true);
      const updated = await cancelAgentRun(runId);
      setRun((prev) => (prev ? { ...prev, ...updated } : null));
    } catch (err: any) {
      alert("Error cancelling run: " + (err?.message || "Unknown error"));
    } finally {
      setCancelling(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex items-center justify-center">
        <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
        <span className="ml-2 text-sm text-slate-500">Loading Execution Trace...</span>
      </div>
    );
  }

  if (error || !run) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-4">
        <Link href="/agents" className="text-xs text-slate-500 hover:text-slate-900 flex items-center gap-1">
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Agents Dashboard
        </Link>
        <div className="p-4 bg-red-50 text-red-700 rounded-lg text-sm">
          {error || "Agent run not found."}
        </div>
      </div>
    );
  }

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Breadcrumb */}
      <Link href="/agents" className="text-xs text-slate-500 hover:text-slate-900 flex items-center gap-1">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Agents Dashboard
      </Link>

      {/* Header Banner */}
      <div className="bg-white dark:bg-slate-900 p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <h1 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <Bot className="w-6 h-6 text-purple-600" />
              {run.agent_name} Execution Trace
            </h1>
            <span className="px-2 py-0.5 text-xs font-bold rounded bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300">
              v{run.agent_version}
            </span>
            <span className="px-2 py-0.5 text-xs font-bold rounded bg-slate-800 text-white">
              {run.status}
            </span>
          </div>
          <p className="text-xs text-slate-500 font-mono">
            Workflow: {run.workflow_id} · Task: {run.task_id} · Run: {run.agent_run_id}
          </p>
        </div>

        {run.status === "RUNNING" && (
          <Button
            onClick={handleCancel}
            disabled={cancelling}
            variant="destructive"
            size="sm"
            className="gap-1 text-xs"
          >
            {cancelling ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Ban className="w-3.5 h-3.5" />}
            Cancel Agent Run
          </Button>
        )}
      </div>

      {/* Metrics Banner */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card className="p-3 text-center">
          <div className="text-[10px] font-semibold text-slate-400 uppercase">Steps Executed</div>
          <div className="text-xl font-bold text-slate-900 dark:text-white mt-0.5">{run.steps_count}</div>
        </Card>
        <Card className="p-3 text-center">
          <div className="text-[10px] font-semibold text-slate-400 uppercase">Tool Calls</div>
          <div className="text-xl font-bold text-slate-900 dark:text-white mt-0.5">{run.tool_calls_count}</div>
        </Card>
        <Card className="p-3 text-center">
          <div className="text-[10px] font-semibold text-slate-400 uppercase">Token Usage</div>
          <div className="text-xl font-bold text-slate-900 dark:text-white mt-0.5">{run.estimated_tokens}</div>
        </Card>
        <Card className="p-3 text-center">
          <div className="text-[10px] font-semibold text-slate-400 uppercase">Confidence</div>
          <div className="text-xl font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">{run.confidence}</div>
        </Card>
      </div>

      {/* Event Trace Timeline */}
      <Card>
        <CardHeader className="border-b border-slate-100 dark:border-slate-800 py-3">
          <CardTitle className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Clock className="w-4 h-4 text-blue-500" />
            Execution Event Timeline ({run.events.length} events)
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-4">
          {run.events.length === 0 ? (
            <p className="text-xs text-slate-400 italic">No event logs recorded for this run.</p>
          ) : (
            <div className="space-y-3">
              {run.events.map((evt) => (
                <div key={evt.id} className="p-3 bg-slate-50 dark:bg-slate-900/50 rounded-lg border border-slate-200 dark:border-slate-800 text-xs space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold font-mono text-purple-700 dark:text-purple-400 uppercase text-[10px]">
                      [{evt.event_type}]
                    </span>
                    <span className="text-[10px] text-slate-400">
                      {new Date(evt.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-slate-800 dark:text-slate-200">{evt.message}</p>
                  {Object.keys(evt.payload).length > 0 && (
                    <pre className="p-2 bg-slate-100 dark:bg-slate-950 rounded text-[10px] font-mono text-slate-600 dark:text-slate-400 overflow-x-auto mt-1">
                      {JSON.stringify(evt.payload, null, 2)}
                    </pre>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </main>
  );
}
