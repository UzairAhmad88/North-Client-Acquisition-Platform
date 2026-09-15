'use client';

import React, { useState } from 'react';
import { ShieldCheck, Smartphone, Key, Lock, CheckCircle2, Copy } from 'lucide-react';
import { securityApi, MFASetupData } from '@/lib/api/security';

export default function MFAPolicyControl() {
  const [setupData, setSetupData] = useState<MFASetupData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  const handleStartSetup = async () => {
    try {
      setLoading(true);
      const res = await securityApi.setupMFA();
      if (res) {
        setSetupData(res);
      }
    } catch (err) {
      console.error('Failed to initiate MFA setup', err);
    } finally {
      setLoading(false);
    }
  };

  const copySecret = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-bold text-white">Multi-Factor & Step-Up Authentication Policy</h3>
        <p className="text-xs text-slate-400">
          Enforce TOTP multi-factor challenges and step-up verification windows for high-risk actions.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Policy Configuration Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <h4 className="text-sm font-semibold text-white flex items-center space-x-2">
            <Lock className="w-4 h-4 text-emerald-400" />
            <span>High-Risk Policy Rules</span>
          </h4>

          <div className="space-y-3 text-xs text-slate-300">
            <div className="flex items-center justify-between p-3 bg-slate-950 rounded-xl border border-slate-800">
              <div>
                <div className="font-medium text-white">Contract Signing Boundary</div>
                <div className="text-slate-400 text-[11px]">Requires recent MFA step-up re-authentication</div>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400">
                ENFORCED
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-slate-950 rounded-xl border border-slate-800">
              <div>
                <div className="font-medium text-white">Authoritative Price Changing</div>
                <div className="text-slate-400 text-[11px]">Requires active Step-Up JWT token (&lt; 15 mins)</div>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400">
                ENFORCED
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-slate-950 rounded-xl border border-slate-800">
              <div>
                <div className="font-medium text-white">AI Production Model Promotion</div>
                <div className="text-slate-400 text-[11px]">Requires dual-control security signoff + MFA</div>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400">
                ENFORCED
              </span>
            </div>
          </div>
        </div>

        {/* User Authenticator Setup */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
          <h4 className="text-sm font-semibold text-white flex items-center space-x-2">
            <Smartphone className="w-4 h-4 text-cyan-400" />
            <span>Configure Authenticator App</span>
          </h4>

          {!setupData ? (
            <div className="space-y-4">
              <p className="text-xs text-slate-400">
                Protect your account by setting up a TOTP authenticator (Google Authenticator, Authy, or 1Password).
              </p>
              <button
                onClick={handleStartSetup}
                disabled={loading}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold transition-colors"
              >
                {loading ? 'Generating...' : 'Setup TOTP Authenticator'}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
                <div className="text-[11px] font-semibold text-slate-400 uppercase mb-1">
                  Manual Secret Key
                </div>
                <div className="flex items-center justify-between font-mono text-xs text-emerald-400 break-all">
                  <span>{setupData.secret}</span>
                  <button
                    onClick={() => copySecret(setupData.secret)}
                    className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors"
                  >
                    {copied ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div>
                <div className="text-[11px] font-semibold text-slate-400 uppercase mb-1">
                  Backup Recovery Codes
                </div>
                <div className="grid grid-cols-2 gap-1.5 font-mono text-[11px] text-slate-300 bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                  {setupData.backup_codes.map((code) => (
                    <div key={code}>{code}</div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
