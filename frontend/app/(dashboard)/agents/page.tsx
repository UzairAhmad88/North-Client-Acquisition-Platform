"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  AgentSpec,
  AgentRun,
  listAgents,
  listAgentRuns,
} from "@/lib/api/agents";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Bot, Shield, Activity, Clock, CheckCircle2, AlertCircle, Play } from "lucide-react";

export default function AgentsDashboardPage() {
  const [agents, setAgents] = useState<AgentSpec[]>([]);
  const [runs, setRuns] = useState<AgentRun[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [agentsData, runsRes] = await Promise.all([
        listAgents(),
        listAgentRuns({ limit: 20 }),
      ]);
      setAgents(agentsData);
      setRuns(runsRes.data);
    } catch (err: any) {
      setError(err?.message || "Failed to load agent runtime data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "COMPLETED":
        return "bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300";
      case "RUNNING":
        return "bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 animate-pulse";
      case "WAITING_FOR_APPROVAL":
        return "bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300";
      case "FAILED":
        return "bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300";
      case "CANCELLED":
        return "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300";
      default:
        return "bg-slate-100 text-slate-700";
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex items-center justify-center">
        <Loader2 className="w-6 h-6 animate-spin text-slate-400" />
        <span className="ml-2 text-sm text-slate-500">Loading Agent Core Runtime...</span>
      </div>
    );
  }

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Bot className="w-7 h-7 text-purple-600" />
            Agent Core & Orchestration Runtime
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Controlled AI agent execution framework, tool sandbox permissions, budget boundaries, and workflow state inspector.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-700 rounded-lg text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Registered Agents</div>
          <div className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{agents.length}</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Runtime Specifications</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Recent Executions</div>
          <div className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{runs.length}</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Total Tracked Runs</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Communication Authority</div>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">DENIED</div>
          <div className="text-[11px] text-slate-400 mt-0.5">Deny-By-Default Enforced</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Kill Switch Status</div>
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">ACTIVE</div>
          <div className="text-[11px] text-slate-400 mt-0.5">AGENTS_ENABLED=true</div>
        </Card>
      </div>

      {/* Registered Agent Runtime Specifications */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-slate-900 dark:text-white">Registered Agents & Permissions</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {agents.map((agent) => (
            <Card key={agent.name} className="overflow-hidden border border-slate-200 dark:border-slate-800">
              <CardHeader className="bg-slate-50/50 dark:bg-slate-900/50 pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <Bot className="w-4 h-4 text-purple-600" />
                    {agent.name}
                  </CardTitle>
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300">
                    v{agent.version}
                  </span>
                </div>
                <CardDescription className="text-xs mt-1">{agent.description}</CardDescription>
              </CardHeader>
              <CardContent className="pt-3 space-y-3">
                <div>
                  <span className="text-[11px] font-bold text-slate-600 dark:text-slate-400 block mb-1 flex items-center gap-1">
                    <Shield className="w-3.5 h-3.5 text-blue-500" />
                    Granted Sandbox Permissions:
                  </span>
                  <div className="flex flex-wrap gap-1">
                    {agent.permissions.length > 0 ? (
                      agent.permissions.map((perm) => (
                        <span key={perm} className="px-1.5 py-0.5 text-[10px] font-mono bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded border border-slate-200/50">
                          {perm}
                        </span>
                      ))
                    ) : (
                      <span className="text-[11px] text-slate-400 italic">No permissions granted (Deny by default)</span>
                    )}
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-500 grid grid-cols-3 gap-2 text-center">
                  <div>
                    <span className="block text-[10px] uppercase font-semibold text-slate-400">Max Steps</span>
                    <span className="font-bold text-slate-700 dark:text-slate-300">{agent.max_steps}</span>
                  </div>
                  <div>
                    <span className="block text-[10px] uppercase font-semibold text-slate-400">Max Tools</span>
                    <span className="font-bold text-slate-700 dark:text-slate-300">{agent.max_tool_calls}</span>
                  </div>
                  <div>
                    <span className="block text-[10px] uppercase font-semibold text-slate-400">Timeout</span>
                    <span className="font-bold text-slate-700 dark:text-slate-300">{agent.max_runtime_seconds}s</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Recent Agent Execution Runs */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-slate-900 dark:text-white">Recent Execution Runs</h2>
        {runs.length === 0 ? (
          <Card className="p-8 text-center bg-slate-50 dark:bg-slate-900/50 border-dashed">
            <Activity className="w-8 h-8 text-slate-400 mx-auto mb-2" />
            <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300">No Agent Execution Runs Logged</h3>
            <p className="text-xs text-slate-500 mt-1">
              Agent execution runs will appear here as workflows execute.
            </p>
          </Card>
        ) : (
          <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 uppercase font-semibold text-[10px]">
                  <tr>
                    <th className="p-3">Run ID / Workflow</th>
                    <th className="p-3">Agent</th>
                    <th className="p-3">Status</th>
                    <th className="p-3">Steps / Tools</th>
                    <th className="p-3">Started</th>
                    <th className="p-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {runs.map((run) => (
                    <tr key={run.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/50 transition">
                      <td className="p-3 font-mono font-semibold text-slate-900 dark:text-white">
                        <Link href={`/agents/runs/${run.id}`} className="hover:underline text-blue-600 dark:text-blue-400">
                          {run.workflow_id}
                        </Link>
                        <div className="text-[10px] text-slate-400 font-sans">{run.task_id}</div>
                      </td>
                      <td className="p-3 font-medium text-slate-800 dark:text-slate-200">
                        {run.agent_name} <span className="text-[10px] text-slate-400">v{run.agent_version}</span>
                      </td>
                      <td className="p-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${getStatusBadge(run.status)}`}>
                          {run.status}
                        </span>
                      </td>
                      <td className="p-3 text-slate-600 dark:text-slate-400">
                        {run.steps_count} steps · {run.tool_calls_count} tools
                      </td>
                      <td className="p-3 text-slate-500">
                        {run.started_at ? new Date(run.started_at).toLocaleString() : "N/A"}
                      </td>
                      <td className="p-3 text-right">
                        <Link href={`/agents/runs/${run.id}`}>
                          <Button size="sm" variant="ghost" className="text-xs">
                            View Trace →
                          </Button>
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
