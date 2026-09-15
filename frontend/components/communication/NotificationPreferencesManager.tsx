'use client';

import React, { useEffect, useState } from 'react';
import {
  CommunicationType,
  NotificationPreference,
  communicationApi,
} from '@/lib/api/communication';

const ALL_CATEGORIES: CommunicationType[] = [
  'NOTIFICATION',
  'CONVERSATION_MESSAGE',
  'CLIENT_MESSAGE',
  'SYSTEM_ALERT',
  'SECURITY_ALERT',
  'WORKFLOW_UPDATE',
  'APPROVAL_REQUEST',
];

export const NotificationPreferencesManager: React.FC = () => {
  const [preferences, setPreferences] = useState<Record<string, NotificationPreference>>({});
  const [loading, setLoading] = useState(true);
  const [savingCategory, setSavingCategory] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const loadPreferences = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await communicationApi.listPreferences();
      const mapped: Record<string, NotificationPreference> = {};
      (data || []).forEach((pref) => {
        mapped[pref.notification_type] = pref;
      });
      setPreferences(mapped);
    } catch (err: any) {
      setError(err.message || 'Failed to load preferences');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPreferences();
  }, []);

  const handleToggleChannel = async (
    category: CommunicationType,
    channelKey: 'in_app_enabled' | 'email_enabled' | 'sms_enabled' | 'webhook_enabled' | 'push_enabled'
  ) => {
    // Critical security alerts override protection
    if (category === 'SECURITY_ALERT' && (channelKey === 'in_app_enabled' || channelKey === 'email_enabled')) {
      setError('Security alert core delivery channels cannot be disabled for compliance.');
      setTimeout(() => setError(null), 4000);
      return;
    }

    const current = preferences[category] || {
      notification_type: category,
      in_app_enabled: true,
      email_enabled: true,
      sms_enabled: false,
      webhook_enabled: false,
      push_enabled: true,
      timezone: 'UTC',
    };

    const updated = {
      ...current,
      [channelKey]: !current[channelKey],
    };

    setSavingCategory(category);
    try {
      const res = await communicationApi.updatePreference({
        notification_type: category,
        in_app_enabled: updated.in_app_enabled,
        email_enabled: updated.email_enabled,
        sms_enabled: updated.sms_enabled,
        webhook_enabled: updated.webhook_enabled,
        push_enabled: updated.push_enabled,
        quiet_hours_start: updated.quiet_hours_start,
        quiet_hours_end: updated.quiet_hours_end,
        timezone: updated.timezone || 'UTC',
      });
      setPreferences((prev) => ({ ...prev, [category]: res }));
      setSuccessMessage(`Updated preferences for ${category}`);
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err: any) {
      setError(err.message || 'Failed to save preference');
    } finally {
      setSavingCategory(null);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl flex flex-col space-y-6">
      <div>
        <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
          Notification & Quiet Hours Preferences
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Customize delivery channels, recipient filters, and quiet hours schedules for each communication category.
        </p>
      </div>

      {/* Mandatory Security Guardrail Banner */}
      <div className="p-4 bg-amber-950/40 border border-amber-600/40 rounded-lg flex items-start space-x-3">
        <span className="text-amber-400 text-lg">🛡️</span>
        <div>
          <h4 className="text-xs font-semibold text-amber-200">Security Override Policy Active</h4>
          <p className="text-[11px] text-amber-300/80 mt-0.5">
            Safety-critical alerts (Security Incidents, MFA changes, Account Lockouts) bypass Quiet Hours and cannot be disabled.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-950/60 border border-red-800 rounded-lg text-red-200 text-xs">
          {error}
        </div>
      )}

      {successMessage && (
        <div className="p-3 bg-emerald-950/50 border border-emerald-800 rounded-lg text-emerald-200 text-xs">
          {successMessage}
        </div>
      )}

      {/* Preferences Table */}
      <div className="border border-slate-800 rounded-lg overflow-hidden">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-950/60 text-slate-400 border-b border-slate-800 font-semibold">
              <th className="p-3">Category</th>
              <th className="p-3 text-center">In-App</th>
              <th className="p-3 text-center">Email</th>
              <th className="p-3 text-center">SMS</th>
              <th className="p-3 text-center">Webhook</th>
              <th className="p-3 text-center">Push</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {loading ? (
              <tr>
                <td colSpan={6} className="text-center py-8 text-slate-500 animate-pulse">
                  Loading preferences...
                </td>
              </tr>
            ) : (
              ALL_CATEGORIES.map((cat) => {
                const pref = preferences[cat] || {
                  in_app_enabled: true,
                  email_enabled: true,
                  sms_enabled: false,
                  webhook_enabled: false,
                  push_enabled: true,
                };
                const isSaving = savingCategory === cat;
                const isSecurity = cat === 'SECURITY_ALERT';

                return (
                  <tr key={cat} className="hover:bg-slate-800/30 transition-colors">
                    <td className="p-3">
                      <div className="font-semibold text-slate-200 font-mono text-[11px]">{cat}</div>
                      {isSecurity && (
                        <span className="text-[10px] text-amber-400 font-medium">Critical Security Bypasses Quiet Hours</span>
                      )}
                    </td>

                    {/* In-App */}
                    <td className="p-3 text-center">
                      <input
                        type="checkbox"
                        checked={pref.in_app_enabled}
                        disabled={isSaving || isSecurity}
                        onChange={() => handleToggleChannel(cat, 'in_app_enabled')}
                        className="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-0 disabled:opacity-60 cursor-pointer"
                      />
                    </td>

                    {/* Email */}
                    <td className="p-3 text-center">
                      <input
                        type="checkbox"
                        checked={pref.email_enabled}
                        disabled={isSaving || isSecurity}
                        onChange={() => handleToggleChannel(cat, 'email_enabled')}
                        className="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-0 disabled:opacity-60 cursor-pointer"
                      />
                    </td>

                    {/* SMS */}
                    <td className="p-3 text-center">
                      <input
                        type="checkbox"
                        checked={pref.sms_enabled}
                        disabled={isSaving}
                        onChange={() => handleToggleChannel(cat, 'sms_enabled')}
                        className="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-0 cursor-pointer"
                      />
                    </td>

                    {/* Webhook */}
                    <td className="p-3 text-center">
                      <input
                        type="checkbox"
                        checked={pref.webhook_enabled}
                        disabled={isSaving}
                        onChange={() => handleToggleChannel(cat, 'webhook_enabled')}
                        className="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-0 cursor-pointer"
                      />
                    </td>

                    {/* Push */}
                    <td className="p-3 text-center">
                      <input
                        type="checkbox"
                        checked={pref.push_enabled}
                        disabled={isSaving}
                        onChange={() => handleToggleChannel(cat, 'push_enabled')}
                        className="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-0 cursor-pointer"
                      />
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
