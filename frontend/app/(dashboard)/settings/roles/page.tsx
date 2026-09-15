import React from 'react';
import RoleManagement from '@/components/security/RoleManagement';

export const metadata = {
  title: 'Roles & Permissions | Settings | Uzaii',
  description: 'Manage RBAC role hierarchy and granular permission assignments.',
};

export default function SettingsRolesPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white tracking-tight">Roles & Permissions Matrix</h1>
        <p className="text-sm text-slate-400">View and inspect authoritative role definitions and permission mappings.</p>
      </div>
      <RoleManagement />
    </div>
  );
}
