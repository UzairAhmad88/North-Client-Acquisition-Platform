"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth/auth-context";
import { getDashboardSummary, DashboardSummaryData } from "@/lib/api/dashboard";
import { DashboardHeader } from "@/components/dashboard/dashboard-header";
import { PrimaryKPIs } from "@/components/dashboard/primary-kpis";
import { AttentionPanel } from "@/components/dashboard/attention-panel";
import { PipelineSnapshot } from "@/components/dashboard/pipeline-snapshot";
import { RecentLeadsCard } from "@/components/dashboard/recent-leads-card";
import { RecentBusinessesCard } from "@/components/dashboard/recent-businesses-card";
import { UpcomingActionsCard } from "@/components/dashboard/upcoming-actions-card";
import { ServiceSnapshotCard } from "@/components/dashboard/service-snapshot-card";
import { QuickActionsBar } from "@/components/dashboard/quick-actions-bar";
import { DashboardSkeleton } from "@/components/dashboard/dashboard-skeleton";
import { AlertCircle, RefreshCw } from "lucide-react";

export default function DashboardPage() {
  const { user } = useAuth();
  const router = useRouter();

  const [data, setData] = useState<DashboardSummaryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = useCallback(async (isManualRefresh = false) => {
    try {
      if (isManualRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      setError(null);
      const res = await getDashboardSummary();
      setData(res);
    } catch (err: any) {
      if (err?.status === 401) {
        router.push("/login");
        return;
      }
      setError(err?.message || "Failed to load dashboard metrics.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [router]);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  if (loading) {
    return (
      <main className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto">
        <DashboardSkeleton />
      </main>
    );
  }

  if (error) {
    return (
      <main className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto">
        <div className="p-6 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/50 text-center">
          <AlertCircle className="w-8 h-8 text-rose-600 dark:text-rose-400 mx-auto mb-2" />
          <h2 className="text-lg font-bold text-rose-900 dark:text-rose-200">
            Dashboard Unavailable
          </h2>
          <p className="text-sm text-rose-700 dark:text-rose-300 mt-1 max-w-md mx-auto">
            {error}
          </p>
          <button
            onClick={() => fetchDashboardData(false)}
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold text-rose-900 dark:text-rose-100 bg-white dark:bg-gray-800 border border-rose-300 dark:border-rose-800 rounded-lg hover:bg-rose-100/50 transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry Loading</span>
          </button>
        </div>
      </main>
    );
  }

  if (!data) return null;

  return (
    <main className="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto space-y-6">
      {/* Welcome Header */}
      <DashboardHeader
        userName={user?.full_name}
        onRefresh={() => fetchDashboardData(true)}
        isRefreshing={refreshing}
      />

      {/* Primary KPI Summary Cards */}
      <PrimaryKPIs businesses={data.businesses} leads={data.leads} />

      {/* Quick Action Shortcuts Bar */}
      <QuickActionsBar />

      {/* Operational Attention Required */}
      <AttentionPanel attention={data.attention} overdueActions={data.overdue_actions} />

      {/* Lead Pipeline Lifecycle Snapshot */}
      <PipelineSnapshot pipeline={data.pipeline} />

      {/* Operational Grids: Recent Items */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentLeadsCard leads={data.recent_leads} />
        <RecentBusinessesCard businesses={data.recent_businesses} />
      </div>

      {/* Operational Grids: Actions & Services */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <UpcomingActionsCard actions={data.upcoming_actions} />
        <ServiceSnapshotCard services={data.services} />
      </div>
    </main>
  );
}
