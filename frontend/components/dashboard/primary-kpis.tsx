"use client";

import React from "react";
import Link from "next/link";
import { Building2, Target, CheckCircle2, DollarSign, ArrowRight } from "lucide-react";
import { BusinessMetricsSummary, LeadMetricsSummary } from "@/lib/api/dashboard";

interface PrimaryKPIsProps {
  businesses: BusinessMetricsSummary;
  leads: LeadMetricsSummary;
}

export function PrimaryKPIs({ businesses, leads }: PrimaryKPIsProps) {
  const cards = [
    {
      title: "Active Businesses",
      value: businesses.active_count,
      subtext: `Total registered: ${businesses.total_count}`,
      icon: Building2,
      href: "/businesses",
      category: "forest",
      color: "text-[#0f4c3a]",
      bg: "bg-[#f2f9f6]",
      border: "border-[#c2e6d8]",
      label: "Brand Active",
    },
    {
      title: "Open Opportunities",
      value: leads.open_count,
      subtext: `Total leads: ${leads.total_count}`,
      icon: Target,
      href: "/leads",
      category: "purple",
      color: "text-[#7c3aed]",
      bg: "bg-[#f3e8ff]",
      border: "border-[#e9d5ff]",
      label: "AI Intelligence",
    },
    {
      title: "Validated Fit",
      value: leads.qualified_count,
      subtext: "Qualified market leads",
      icon: CheckCircle2,
      href: "/leads?qualification_status=QUALIFIED",
      category: "forest",
      color: "text-[#0f4c3a]",
      bg: "bg-[#f2f9f6]",
      border: "border-[#c2e6d8]",
      label: "Qualified State",
    },
    {
      title: "Financial Ledger Value",
      value: `$${(businesses.active_count * 12500).toLocaleString()}`,
      subtext: "Estimated MRR volume",
      icon: DollarSign,
      href: "/finance",
      category: "gold",
      color: "text-[#b45309]",
      bg: "bg-[#fef3c7]",
      border: "border-[#fde68a]",
      label: "Financial Value",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((c) => {
        const Icon = c.icon;
        return (
          <div
            key={c.title}
            className={`p-5 rounded-xl bg-white border border-slate-200/90 shadow-2xs flex flex-col justify-between hover:shadow-md transition-all ${
              c.category === "gold"
                ? "border-l-4 border-l-[#c59b27]"
                : c.category === "purple"
                ? "border-l-4 border-l-[#8b5cf6]"
                : "border-l-4 border-l-[#0f4c3a]"
            }`}
          >
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                  {c.title}
                </span>
                <div className={`p-2 rounded-lg ${c.bg} ${c.color} border ${c.border}`}>
                  <Icon className="w-5 h-5" />
                </div>
              </div>
              <div className="text-3xl font-extrabold text-slate-900 mt-3 font-mono tracking-tight">
                {c.value}
              </div>
              <p className="text-xs text-slate-500 font-medium mt-1">{c.subtext}</p>
            </div>

            <Link
              href={c.href}
              className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-slate-600 hover:text-[#0f4c3a] transition-colors group"
            >
              <span>{c.label}</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
            </Link>
          </div>
        );
      })}
    </div>
  );
}
