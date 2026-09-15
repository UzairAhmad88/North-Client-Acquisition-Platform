"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth/auth-context";
import { Lock, Mail, Eye, EyeOff, ShieldCheck, Sparkles, ArrowRight, AlertCircle, Award } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email || !password) {
      setError("Please enter both email and password.");
      return;
    }

    setSubmitting(true);
    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (err: any) {
      const msg = err?.message || "Unable to connect to the authentication server. Please check your credentials.";
      setError(msg);
    } finally {
      setSubmitting(false);
    }
  };

  const fillDemoCredentials = () => {
    setEmail("imuzairahmad8@gmail.com");
    setPassword("SecurePassword123!");
    setError(null);
  };

  return (
    <main className="min-h-screen flex flex-col justify-center items-center bg-[#faf9f6] text-slate-900 p-4 relative overflow-hidden font-sans">
      {/* Subtle Warm Ivory & Soft Purple Glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[300px] bg-gradient-to-tr from-[#0f4c3a]/5 via-[#8b5cf6]/5 to-[#c59b27]/5 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md z-10">
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#f3e8ff] border border-[#e9d5ff] text-xs font-bold text-[#7c3aed] mb-4 shadow-2xs">
            <Sparkles className="w-3.5 h-3.5 text-[#7c3aed]" />
            <span>Digital Civilization Platform</span>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Uzaii Develop By North&apos;s
          </h1>
          <p className="text-sm text-slate-500 mt-2 font-medium">
            Sign in to access your Enterprise AI & Command Platform
          </p>
        </div>

        {/* Card Panel */}
        <div className="bg-white border border-slate-200/90 rounded-2xl p-8 shadow-xl shadow-slate-200/40">
          {error && (
            <div className="mb-6 p-3.5 bg-rose-50 border border-rose-200 text-rose-800 text-xs rounded-xl flex items-start gap-2.5 leading-relaxed">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold block mb-0.5">Authentication Failure</span>
                {error}
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="operator@uzaii.com"
                  required
                  className="w-full bg-[#faf9f6] border border-slate-300 focus:border-[#0f4c3a] rounded-xl pl-10 pr-4 py-2.5 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#0f4c3a]/15 transition-all font-semibold"
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                  Password
                </label>
                <span className="text-xs text-slate-500 hover:text-[#0f4c3a] transition-colors cursor-pointer font-semibold">
                  Forgot?
                </span>
              </div>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  required
                  className="w-full bg-[#faf9f6] border border-slate-300 focus:border-[#0f4c3a] rounded-xl pl-10 pr-10 py-2.5 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#0f4c3a]/15 transition-all font-semibold"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-[#0f4c3a] hover:bg-[#0b382b] text-white font-bold py-3 px-4 rounded-xl text-sm transition-all shadow-md shadow-[#0f4c3a]/20 flex items-center justify-center gap-2 group disabled:opacity-50 cursor-pointer"
            >
              {submitting ? (
                <span>Authenticating Session...</span>
              ) : (
                <>
                  <span>Sign In to Operator Console</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                </>
              )}
            </button>
          </form>

          {/* Quick Demo Assist & Antique Gold Sovereign Badge */}
          <div className="mt-6 pt-5 border-t border-slate-100 flex items-center justify-between text-xs">
            <span className="flex items-center gap-1.5 font-bold text-[#b45309] bg-[#fef3c7] border border-[#fde68a] px-2.5 py-1 rounded-full text-[11px]">
              <Award className="w-3.5 h-3.5 text-[#b45309]" />
              Sovereign Auth Ready
            </span>
            <button
              type="button"
              onClick={fillDemoCredentials}
              className="text-[#7c3aed] hover:text-[#6b21a8] font-bold underline underline-offset-4 cursor-pointer"
            >
              Fill Demo Credentials
            </button>
          </div>
        </div>

        {/* Footer info */}
        <p className="text-center text-xs text-slate-400 mt-6 font-mono font-medium">
          Uzaii Develop By North&apos;s &bull; 5-Color HCI Certified System &bull; 100% Encrypted
        </p>
      </div>
    </main>
  );
}
