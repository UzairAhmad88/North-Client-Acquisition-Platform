"use client";

import React from "react";
import Link from "next/link";
import { Building2, Target, Layers, PlusCircle, Sparkles } from "lucide-react";

export function QuickActionsBar() {
  const actions = [
    {
      label: "Add Business",
      icon: PlusCircle,
      href: "/businesses?action=new",
      color: "bg-[#0f4c3a] hover:bg-[#0b382b] text-white shadow-xs",
    },
    {
      label: "Create Lead",
      icon: Target,
      href: "/leads?action=new",
      color: "bg-[#0f4c3a] hover:bg-[#0b382b] text-white shadow-xs",
    },
    {
      label: "Run AI Agent",
      icon: Sparkles,
      href: "/agents",
      color: "bg-[#8b5cf6] hover:bg-[#7c3aed] text-white shadow-xs",
    },
    {
      label: "View Businesses",
      icon: Building2,
      href: "/businesses",
      color: "bg-white text-slate-700 border border-slate-300 hover:bg-slate-50",
    },
    {
      label: "Manage Services",
      icon: Layers,
      href: "/services",
      color: "bg-white text-slate-700 border border-slate-300 hover:bg-slate-50",
    },
  ];

  return (
    <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-2xs flex flex-wrap items-center justify-between gap-3">
      <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">
        Quick Action Shortcuts
      </div>
      <div className="flex flex-wrap items-center gap-2">
        {actions.map((act) => {
          const Icon = act.icon;
          return (
            <Link
              key={act.label}
              href={act.href}
              className={`inline-flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg transition-all ${act.color}`}
            >
              <Icon className="w-4 h-4" />
              <span>{act.label}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
