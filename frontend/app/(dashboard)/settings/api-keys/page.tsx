import React from 'react';
import APIKeyManager from '@/components/security/APIKeyManager';

export const metadata = {
  title: 'API Keys | Settings | Uzaii',
  description: 'Manage scoped machine-to-machine integration credentials.',
};

export default function SettingsAPIKeysPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white tracking-tight">API Key Management</h1>
        <p className="text-sm text-slate-400">Create, inspect, and revoke scoped machine credentials for automated integrations.</p>
      </div>
      <APIKeyManager />
    </div>
  );
}
