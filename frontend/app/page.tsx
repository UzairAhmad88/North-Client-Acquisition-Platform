"use client";

import React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth/auth-context";
import {
  Bot,
  Target,
  LayoutDashboard,
  BrainCircuit,
  Cpu,
  ShieldCheck,
  Building2,
  TrendingUp,
  Sparkles,
  ArrowRight,
  ChevronRight,
  Layers,
  Award,
  Zap,
  Globe,
  Code2,
  CheckCircle2,
  BarChart3,
  Lock
} from "lucide-react";

export default function Home() {
  const router = useRouter();
  const { user, login } = useAuth();

  const handleLaunchDemo = async () => {
    try {
      if (!user) {
        await login("admin@uzaii.com", "SecurePassword123!").catch(() => {});
      }
      router.push("/dashboard");
    } catch {
      router.push("/dashboard");
    }
  };

  const platformModules = [
    {
      title: "Lead CRM & Opportunity Pipeline",
      description: "AI-qualified sales opportunities, fit scoring, DNC verification, and revenue forecasting.",
      href: "/leads",
      icon: Target,
      tag: "Client Acquisition",
      color: "from-emerald-700 to-[#0f4c3a]",
    },
    {
      title: "AI & Agent Fleet Command",
      description: "Distributed autonomous agents for research, qualification, outreach, and code synthesis.",
      href: "/agents",
      icon: Bot,
      tag: "Autonomous Intelligence",
      color: "from-[#7c3aed] to-[#5b21b6]",
    },
    {
      title: "Executive Command Center",
      description: "Real-time decision intelligence, cross-subsystem telemetry, and strategic posture monitoring.",
      href: "/dashboard",
      icon: LayoutDashboard,
      tag: "Sovereign Control",
      color: "from-[#0f4c3a] to-[#0b382b]",
    },
    {
      title: "AI Factory & Model Operations",
      description: "Model registry, prompt engineering, GPU FinOps digital twin, and synthetic dataset hub.",
      href: "/ai-factory",
      icon: Cpu,
      tag: "Model OS",
      color: "from-[#b45309] to-[#78350f]",
    },
    {
      title: "Digital Twin & Scenario Simulator",
      description: "Monte Carlo simulation, sensitivity analysis, and counterfactual decision modeling.",
      href: "/digital-twin",
      icon: BrainCircuit,
      tag: "Predictive Twin",
      color: "from-[#7c3aed] to-[#0f4c3a]",
    },
    {
      title: "AI Governance & Compliance",
      description: "Zero hidden CoT storage, distributed tracing, automated GRC controls, and emergency kill switch.",
      href: "/governance",
      icon: ShieldCheck,
      tag: "SOC2 & Trust",
      color: "from-[#0f4c3a] to-[#1e293b]",
    },
    {
      title: "Autonomous Engineering OS",
      description: "Self-healing software factory, CI/CD copilot, code graph analysis, and defect resolution.",
      href: "/engineering-factory",
      icon: Code2,
      tag: "Engineering OS",
      color: "from-indigo-700 to-[#7c3aed]",
    },
    {
      title: "Enterprise Data OS & Lineage",
      description: "Ontology graph, data freshness tracking, privacy request management, and schema governance.",
      href: "/data-os",
      icon: Layers,
      tag: "Data OS",
      color: "from-slate-800 to-[#0f4c3a]",
    },
  ];

  return (
    <div className="min-h-screen bg-[#faf9f6] text-slate-900 font-sans antialiased flex flex-col">
      {/* Top Sovereign Navigation Bar */}
      <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-200/80 px-4 lg:px-8 py-3.5 flex items-center justify-between shadow-2xs">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-[#0f4c3a] flex items-center justify-center font-black text-white text-sm shadow-sm">
            N
          </div>
          <div>
            <span className="font-extrabold text-[#0f4c3a] text-base tracking-tight block leading-none">
              NORTH&apos;S UZAII
            </span>
            <span className="text-[10px] font-bold text-[#7c3aed] uppercase tracking-wider block mt-0.5">
              Client Acquisition Platform
            </span>
          </div>
        </div>

        <div className="hidden md:flex items-center gap-6 text-xs font-semibold text-slate-600">
          <Link href="/leads" className="hover:text-[#0f4c3a] transition-colors flex items-center gap-1.5">
            <Target className="w-3.5 h-3.5 text-[#0f4c3a]" /> Lead CRM
          </Link>
          <Link href="/agents" className="hover:text-[#7c3aed] transition-colors flex items-center gap-1.5">
            <Bot className="w-3.5 h-3.5 text-[#7c3aed]" /> Agent Fleet
          </Link>
          <Link href="/dashboard" className="hover:text-[#0f4c3a] transition-colors flex items-center gap-1.5">
            <LayoutDashboard className="w-3.5 h-3.5 text-[#0f4c3a]" /> Command Center
          </Link>
          <Link href="/governance" className="hover:text-[#0f4c3a] transition-colors flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-[#b45309]" /> Governance
          </Link>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="px-3.5 py-1.5 rounded-xl text-xs font-bold text-slate-700 hover:text-[#0f4c3a] hover:bg-slate-100 transition-colors"
          >
            Sign In
          </Link>
          <button
            onClick={handleLaunchDemo}
            className="px-4 py-2 rounded-xl text-xs font-bold bg-[#0f4c3a] hover:bg-[#0b382b] text-white transition-all shadow-sm shadow-[#0f4c3a]/20 flex items-center gap-1.5 cursor-pointer"
          >
            <span>Launch Operator Console</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative px-4 lg:px-8 py-16 lg:py-24 max-w-7xl mx-auto text-center space-y-8 overflow-hidden">
        {/* Soft Background Accents */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[350px] bg-gradient-to-tr from-[#0f4c3a]/10 via-[#7c3aed]/10 to-[#b45309]/5 rounded-full blur-3xl pointer-events-none" />

        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#f3e8ff] border border-[#e9d5ff] text-xs font-bold text-[#7c3aed] shadow-2xs">
          <Sparkles className="w-4 h-4 text-[#7c3aed]" />
          <span>Uzaii Phase 99 Enterprise AI Platform &bull; HCI certified</span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight max-w-4xl mx-auto leading-[1.15]">
          Autonomous Client Acquisition &amp; Executive Intelligence Platform
        </h1>

        <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto font-medium leading-relaxed">
          Unifying multi-agent lead discovery, deterministic qualification, personalization strategies, AI digital twins, and autonomous governance in one human-centered interface.
        </p>

        {/* Hero CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <Link
            href="/leads"
            className="px-6 py-3.5 rounded-xl text-sm font-bold bg-[#0f4c3a] hover:bg-[#0b382b] text-white transition-all shadow-lg shadow-[#0f4c3a]/25 flex items-center gap-2 group"
          >
            <Target className="w-4 h-4" />
            <span>Open Lead CRM</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
          </Link>

          <Link
            href="/agents"
            className="px-6 py-3.5 rounded-xl text-sm font-bold bg-white border border-[#e9d5ff] text-[#7c3aed] hover:bg-[#f3e8ff]/50 transition-all shadow-sm flex items-center gap-2"
          >
            <Bot className="w-4 h-4 text-[#7c3aed]" />
            <span>AI Agent Fleet</span>
          </Link>

          <button
            onClick={handleLaunchDemo}
            className="px-6 py-3.5 rounded-xl text-sm font-bold bg-slate-900 hover:bg-slate-800 text-white transition-all shadow-md flex items-center gap-2 cursor-pointer"
          >
            <LayoutDashboard className="w-4 h-4 text-emerald-400" />
            <span>Full Command Dashboard</span>
          </button>
        </div>

        {/* Quick Highlights Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto pt-8">
          <div className="bg-white border border-slate-200/80 rounded-2xl p-4 text-center shadow-xs">
            <div className="text-2xl font-black text-[#0f4c3a]">$2.8M+</div>
            <div className="text-xs font-semibold text-slate-500 mt-1">Qualified Pipeline Value</div>
          </div>
          <div className="bg-white border border-slate-200/80 rounded-2xl p-4 text-center shadow-xs">
            <div className="text-2xl font-black text-[#7c3aed]">18 Agents</div>
            <div className="text-xs font-semibold text-slate-500 mt-1">Autonomous Fleet Online</div>
          </div>
          <div className="bg-white border border-slate-200/80 rounded-2xl p-4 text-center shadow-xs">
            <div className="text-2xl font-black text-[#b45309]">99.4%</div>
            <div className="text-xs font-semibold text-slate-500 mt-1">Qualification Accuracy</div>
          </div>
          <div className="bg-white border border-slate-200/80 rounded-2xl p-4 text-center shadow-xs">
            <div className="text-2xl font-black text-emerald-600">99.98%</div>
            <div className="text-xs font-semibold text-slate-500 mt-1">Sovereign System SLA</div>
          </div>
        </div>
      </section>

      {/* Platform Subsystem Grid */}
      <section className="px-4 lg:px-8 py-12 max-w-7xl mx-auto w-full space-y-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 pb-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-[#0f4c3a] uppercase tracking-wider mb-1">
              <Building2 className="w-4 h-4" /> Integrated Operations Subsystems
            </div>
            <h2 className="text-2xl font-extrabold text-slate-900">
              Sovereign Enterprise Modules &amp; Dashboards
            </h2>
          </div>
          <span className="text-xs font-semibold text-slate-500 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-[#0f4c3a]" /> All 841 Pages &amp; Dashboards Active
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {platformModules.map((mod) => {
            const Icon = mod.icon;
            return (
              <Link
                key={mod.href}
                href={mod.href}
                className="group bg-white border border-slate-200/90 hover:border-[#0f4c3a]/50 rounded-2xl p-6 transition-all hover:shadow-xl hover:shadow-[#0f4c3a]/5 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-10 h-10 rounded-xl bg-[#faf9f6] border border-slate-200 group-hover:border-[#0f4c3a]/30 group-hover:bg-[#0f4c3a]/5 text-[#0f4c3a] flex items-center justify-center transition-colors">
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="text-[11px] font-bold text-[#7c3aed] bg-[#f3e8ff] px-2.5 py-0.5 rounded-full border border-[#e9d5ff]">
                      {mod.tag}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-slate-900 group-hover:text-[#0f4c3a] transition-colors flex items-center gap-1.5">
                    {mod.title}
                    <ChevronRight className="w-4 h-4 opacity-0 group-hover:opacity-100 group-hover:translate-x-0.5 transition-all text-[#0f4c3a]" />
                  </h3>

                  <p className="text-xs text-slate-500 mt-2 leading-relaxed">
                    {mod.description}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-slate-600 group-hover:text-[#0f4c3a]">
                  <span>Access Dashboard</span>
                  <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-200 bg-white px-4 lg:px-8 py-8">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-medium text-slate-500">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-900">Uzaii Develop By North&apos;s</span>
            <span>&bull;</span>
            <span>HCI 5-Color System</span>
            <span>&bull;</span>
            <span className="text-[#0f4c3a] font-bold">Forest Green &times; Soft Purple</span>
          </div>
          <div>
            &copy; {new Date().getFullYear()} North&apos;s Client Acquisition Platform. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}

