import React from 'react';
import UserManagement from '@/components/security/UserManagement';

export const metadata = {
  title: 'User Management | Settings | Uzaii',
  description: 'Manage internal team and client user access, roles, and status.',
};

export default function SettingsUsersPage() {
  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white tracking-tight">User Management</h1>
        <p className="text-sm text-slate-400">Invite, configure, and manage organization user accounts and permissions.</p>
      </div>
      <UserManagement />
    </div>
  );
}
