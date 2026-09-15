"use client";

import React, { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth/auth-context";
import {
  LayoutDashboard,
  Briefcase,
  Building2,
  DollarSign,
  Microscope,
  BookOpen,
  Bot,
  Zap,
  BarChart3,
  Shield,
  Scale,
  Settings,
  Search,
  Bell,
  LogOut,
  ChevronDown,
  Menu,
  X,
  CheckCircle2,
  Cpu,
  Sparkles,
  Award
} from "lucide-react";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, isLoading, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#faf9f6] text-slate-600 text-sm font-sans space-y-3">
        <div className="w-8 h-8 border-2 border-[#0f4c3a] border-t-transparent rounded-full animate-spin" />
        <span className="font-semibold text-slate-800">Authenticating Sovereign Session...</span>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const primaryNav = [
    { name: "Command Center", href: "/dashboard", icon: LayoutDashboard, category: "base" },
    { name: "Work & Projects", href: "/projects", icon: Briefcase, category: "base" },
    { name: "Business & CRM", href: "/businesses", icon: Building2, category: "base" },
    { name: "Finance & Ledger", href: "/finance", icon: DollarSign, category: "gold" },
    { name: "Research & Science", href: "/research", icon: Microscope, category: "brown" },
    { name: "Knowledge Commons", href: "/knowledge", icon: BookOpen, category: "brown" },
    { name: "AI & Agent Fleet", href: "/agents", icon: Bot, category: "purple" },
    { name: "Automations", href: "/orchestration", icon: Zap, category: "purple" },
    { name: "Final Integration", href: "/final-integration", icon: Cpu, category: "purple" },
  ];

  const systemNav = [
    { name: "Analytics", href: "/analytics", icon: BarChart3 },
    { name: "Security SOC", href: "/security", icon: Shield },
    { name: "Governance & GRC", href: "/governance", icon: Scale },
    { name: "Settings & Admin", href: "/administration", icon: Settings },
  ];

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-[#faf9f6] text-slate-900 flex flex-col font-sans antialiased">
      {/* Top Application Header */}
      <header className="h-14 border-b border-slate-200/80 bg-white sticky top-0 z-40 px-4 flex items-center justify-between gap-4 shadow-2xs">
        {/* Left: Brand & Mobile Toggle */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-slate-600 hover:text-slate-900 p-1.5 rounded-lg hover:bg-slate-100"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
          <Link href="/dashboard" className="flex items-center gap-2.5 group">
            <div className="w-7 h-7 rounded-lg bg-[#0f4c3a] flex items-center justify-center font-black text-white text-xs shadow-xs">
              N
            </div>
            <div>
              <span className="font-extrabold text-[#0f4c3a] text-sm tracking-tight group-hover:text-[#0b382b] transition-colors">
                NORTH&apos;S
              </span>
              <span className="text-[10px] text-slate-500 font-mono block -mt-1 font-medium">
                Uzaii OS
              </span>
            </div>
          </Link>
        </div>

        {/* Center: Global Intelligent Command Bar */}
        <div className="hidden md:flex flex-1 max-w-xl relative">
          <Sparkles className="w-4 h-4 text-[#8b5cf6] absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Ask anything or run a task... [Cmd+K]"
            className="w-full bg-[#faf9f6] border border-slate-200/90 rounded-xl pl-10 pr-12 py-1.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#8b5cf6] focus:ring-2 focus:ring-[#8b5cf6]/20 transition-all font-medium"
          />
          <kbd className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] font-mono text-slate-400 bg-white border border-slate-200 px-1.5 py-0.5 rounded shadow-2xs">
            ⌘K
          </kbd>
        </div>

        {/* Right: Status & Profile */}
        <div className="flex items-center gap-3">
          {/* Muted Antique Gold Health Badge */}
          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#fef3c7] border border-[#fde68a] text-[11px] font-mono text-[#b45309] font-bold">
            <Award className="w-3.5 h-3.5 text-[#b45309]" />
            <span>99.8% Optimal</span>
          </div>

          <button className="text-slate-500 hover:text-slate-800 p-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 transition-colors relative">
            <Bell className="w-4 h-4" />
            <span className="w-2 h-2 rounded-full bg-[#8b5cf6] absolute top-1 right-1" />
          </button>

          {/* User Dropdown */}
          <div className="relative">
            <button
              onClick={() => setUserDropdownOpen(!userDropdownOpen)}
              className="flex items-center gap-2 p-1.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 transition-all text-xs"
            >
              <div className="w-6 h-6 rounded-lg bg-[#f2f9f6] border border-[#c2e6d8] text-[#0f4c3a] font-bold flex items-center justify-center text-xs uppercase">
                {user.full_name?.[0] || "U"}
              </div>
              <span className="hidden md:inline-block font-semibold text-slate-800 max-w-[100px] truncate">
                {user.full_name || user.email}
              </span>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
            </button>

            {userDropdownOpen && (
              <div className="absolute right-0 mt-2 w-60 bg-white border border-slate-200 rounded-xl shadow-xl py-2 z-50 text-xs">
                <div className="px-3 py-2 border-b border-slate-100">
                  <p className="font-bold text-slate-900 truncate">{user.full_name}</p>
                  <p className="text-slate-500 text-[11px] truncate">{user.email}</p>
                  <span className="mt-1.5 inline-block text-[10px] font-mono text-[#0f4c3a] bg-[#f2f9f6] border border-[#c2e6d8] px-2 py-0.5 rounded-md font-bold uppercase">
                    Role: {user.role}
                  </span>
                </div>
                <Link
                  href="/final-integration"
                  className="px-3 py-2 text-slate-700 hover:bg-slate-50 flex items-center gap-2 font-semibold"
                  onClick={() => setUserDropdownOpen(false)}
                >
                  <Cpu className="w-3.5 h-3.5 text-[#8b5cf6]" />
                  System Certification Matrix
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-3 py-2 text-rose-600 hover:bg-rose-50 flex items-center gap-2 border-t border-slate-100 mt-1 font-semibold"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Body Shell (Sidebar + Content Workspace) */}
      <div className="flex-1 flex overflow-hidden">
        {/* Desktop Sidebar */}
        <aside className="hidden md:flex w-64 border-r border-slate-200/80 bg-white p-4 flex-col justify-between overflow-y-auto">
          <div className="space-y-6">
            <div>
              <div className="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider px-2.5 mb-2">
                Command Center
              </div>
              <nav className="space-y-1">
                {primaryNav.map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={`flex items-center justify-between px-3 py-2 rounded-lg text-xs font-semibold transition-all ${
                        isActive
                          ? "bg-[#0f4c3a] text-white shadow-xs"
                          : "text-slate-600 hover:text-slate-900 hover:bg-[#faf9f6]"
                      }`}
                    >
                      <div className="flex items-center gap-2.5">
                        <item.icon
                          className={`w-4 h-4 ${
                            isActive
                              ? "text-white"
                              : item.category === "purple"
                              ? "text-[#8b5cf6]"
                              : item.category === "gold"
                              ? "text-[#b45309]"
                              : item.category === "brown"
                              ? "text-[#78350f]"
                              : "text-slate-500"
                          }`}
                        />
                        <span>{item.name}</span>
                      </div>
                      {!isActive && item.category === "purple" && (
                        <span className="w-1.5 h-1.5 rounded-full bg-[#8b5cf6]" title="AI Powered" />
                      )}
                      {!isActive && item.category === "gold" && (
                        <span className="w-1.5 h-1.5 rounded-full bg-[#c59b27]" title="Financial Value" />
                      )}
                      {!isActive && item.category === "brown" && (
                        <span className="w-1.5 h-1.5 rounded-full bg-[#78350f]" title="Knowledge Context" />
                      )}
                    </Link>
                  );
                })}
              </nav>
            </div>

            <div>
              <div className="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider px-2.5 mb-2">
                System Ops
              </div>
              <nav className="space-y-1">
                {systemNav.map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-semibold transition-all ${
                        isActive
                          ? "bg-[#0f4c3a] text-white shadow-xs"
                          : "text-slate-600 hover:text-slate-900 hover:bg-[#faf9f6]"
                      }`}
                    >
                      <item.icon className={`w-4 h-4 ${isActive ? "text-white" : "text-slate-500"}`} />
                      <span>{item.name}</span>
                    </Link>
                  );
                })}
              </nav>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-100 text-[11px] text-slate-500 font-mono flex items-center justify-between px-2">
            <span className="font-semibold text-slate-600">5-Color HCI System Active</span>
            <span className="w-2 h-2 rounded-full bg-[#0f4c3a]" />
          </div>
        </aside>

        {/* Mobile Sidebar Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden fixed inset-0 z-50 bg-white/95 backdrop-blur-md p-6 flex flex-col justify-between overflow-y-auto">
            <div>
              <div className="flex justify-between items-center mb-6 border-b border-slate-100 pb-4">
                <span className="font-extrabold text-[#0f4c3a] text-lg">Menu Navigation</span>
                <button onClick={() => setMobileMenuOpen(false)} className="text-slate-500 hover:text-slate-800">
                  <X className="w-6 h-6" />
                </button>
              </div>
              <nav className="space-y-1.5">
                {[...primaryNav, ...systemNav].map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex items-center justify-between px-3.5 py-3 rounded-xl text-sm font-semibold text-slate-700 hover:bg-slate-100"
                  >
                    <div className="flex items-center gap-3">
                      <item.icon className="w-5 h-5 text-[#0f4c3a]" />
                      <span>{item.name}</span>
                    </div>
                  </Link>
                ))}
              </nav>
            </div>
            <button
              onClick={handleLogout}
              className="mt-8 text-rose-600 flex items-center gap-2 font-semibold text-sm p-3 bg-rose-50 rounded-xl border border-rose-200"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </div>
        )}

        {/* Main Workspace Area (Warm Ivory Base) */}
        <main className="flex-1 overflow-y-auto p-4 md:p-8 bg-[#faf9f6]">
          {children}
        </main>
      </div>
    </div>
  );
}
