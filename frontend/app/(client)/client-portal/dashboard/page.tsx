'use client';

import React from 'react';
import Link from 'next/link';
import { Building2, ArrowRight, ShieldCheck, FileCheck, MessageSquare, FolderGit2 } from 'lucide-react';

export default function ClientDashboardPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-8">
      {/* Header */}
      <div className="max-w-7xl mx-auto bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-blue-600/10 border border-blue-500/20 rounded-xl text-blue-400">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-black text-white tracking-tight">Client Portal Dashboard</h1>
              <p className="text-xs text-slate-400 mt-1">
                Uzaii Develop By North’s — Secure Collaboration & Transparent Delivery Workspace
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <Link
            href="/client-portal/projects"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-xl text-xs font-semibold text-white flex items-center space-x-2 shadow-lg shadow-blue-600/20 transition"
          >
            <span>View Client Projects</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* Main Grid */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Active Projects Widget */}
        <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 className="text-lg font-bold text-white flex items-center space-x-2">
              <Building2 className="w-5 h-5 text-blue-400" />
              <span>Active Client Engagements</span>
            </h2>
            <span className="text-xs text-slate-400">1 Active Project</span>
          </div>

          <div className="bg-slate-950 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-white text-base">Enterprise Customer Portal System</h3>
                <p className="text-xs text-slate-400 mt-0.5">Acme Global Corp • Delivery Phase: Sprint 3 Execution</p>
              </div>
              <Link
                href="/client-portal/projects/proj-001"
                className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs font-semibold text-slate-200 border border-slate-700 flex items-center space-x-1.5"
              >
                <span>Open Workspace</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-slate-800 text-xs">
              <div>
                <span className="text-slate-400 block">Deliverables</span>
                <span className="font-semibold text-emerald-400">1 Pending Review</span>
              </div>
              <div>
                <span className="text-slate-400 block">Discussions</span>
                <span className="font-semibold text-blue-400">3 Active Threads</span>
              </div>
              <div>
                <span className="text-slate-400 block">Action Items</span>
                <span className="font-semibold text-amber-400">2 Actions Required</span>
              </div>
            </div>
          </div>
        </div>

        {/* Security & Access Info Widget */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
          <h2 className="text-base font-bold text-white flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <span>Client Security Guarantees</span>
          </h2>
          <div className="space-y-3 text-xs text-slate-300">
            <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
              <strong className="text-white block">Strict Data Isolation</strong>
              <p className="text-slate-400 text-[11px]">
                Internal engineering costs, labor margins, developer notes, and raw AI prompts remain strictly hidden.
              </p>
            </div>

            <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
              <strong className="text-white block">SHA-256 Sign-Off Audit</strong>
              <p className="text-slate-400 text-[11px]">
                Deliverable approvals record canonical content hashes and cryptographic audit logs.
              </p>
            </div>

            <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
              <strong className="text-white block">AI Agent Guardrails</strong>
              <p className="text-slate-400 text-[11px]">
                Client AI agents assist communication but possess zero permission to modify baseline contracts or budgets.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
