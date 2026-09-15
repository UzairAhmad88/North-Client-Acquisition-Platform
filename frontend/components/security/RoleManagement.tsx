'use client';

import React, { useState, useEffect } from 'react';
import { Lock, Shield, Check, Search, Filter, AlertCircle } from 'lucide-react';
import { securityApi, SystemRoleItem, SystemPermissionItem } from '@/lib/api/security';

export default function RoleManagement() {
  const [roles, setRoles] = useState<SystemRoleItem[]>([]);
  const [permissions, setPermissions] = useState<SystemPermissionItem[]>([]);
  const [selectedRole, setSelectedRole] = useState<string>('DEVELOPER');
  const [loading, setLoading] = useState<boolean>(true);
  const [searchFilter, setSearchFilter] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [rolesRes, permsRes] = await Promise.all([
          securityApi.listRoles(),
          securityApi.listPermissions(),
        ]);
        if (rolesRes) setRoles(rolesRes);
        if (permsRes) setPermissions(permsRes);
      } catch (err) {
        console.error('Failed to load roles and permissions', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const activeRoleObj = roles.find((r) => r.name === selectedRole);
  const activePermissionsSet = new Set(activeRoleObj ? activeRoleObj.permissions : []);

  const filteredPermissions = permissions.filter(
    (p) =>
      p.name.toLowerCase().includes(searchFilter.toLowerCase()) ||
      p.resource.toLowerCase().includes(searchFilter.toLowerCase()) ||
      p.description.toLowerCase().includes(searchFilter.toLowerCase())
  );

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Roles List */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center space-x-2">
          <Shield className="w-5 h-5 text-emerald-400" />
          <span>System Roles</span>
        </h3>
        <p className="text-xs text-slate-400">
          Predefined internal responsibilities & client workspace boundaries.
        </p>

        <div className="space-y-1.5 max-h-[550px] overflow-y-auto pr-1">
          {roles.map((r) => (
            <button
              key={r.name}
              onClick={() => setSelectedRole(r.name)}
              className={`w-full text-left px-3.5 py-2.5 rounded-xl text-sm font-medium transition-colors flex items-center justify-between ${
                selectedRole === r.name
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  : 'text-slate-300 hover:bg-slate-800/60'
              }`}
            >
              <span>{r.name}</span>
              <span className="text-xs text-slate-500">{r.permissions.length} perms</span>
            </button>
          ))}
        </div>
      </div>

      {/* Permission Matrix for Selected Role */}
      <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-bold text-white">{selectedRole}</span>
              <span className="px-2 py-0.5 rounded text-xs font-semibold bg-slate-800 text-slate-300">
                {activeRoleObj?.is_internal ? 'INTERNAL TEAM' : 'EXTERNAL CLIENT'}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">{activeRoleObj?.description}</p>
          </div>

          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Filter permissions..."
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
            />
          </div>
        </div>

        {/* Matrix List */}
        <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
          {filteredPermissions.map((p) => {
            const isGranted = activePermissionsSet.has(p.name);
            return (
              <div
                key={p.name}
                className={`p-3 rounded-xl border flex items-center justify-between transition-colors ${
                  isGranted
                    ? 'bg-emerald-950/20 border-emerald-500/20'
                    : 'bg-slate-950/40 border-slate-800/60 opacity-60'
                }`}
              >
                <div className="space-y-0.5">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-xs font-semibold text-white">{p.name}</span>
                    <span
                      className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                        p.risk_level === 'CRITICAL'
                          ? 'bg-rose-500/10 text-rose-400'
                          : p.risk_level === 'HIGH'
                          ? 'bg-amber-500/10 text-amber-400'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {p.risk_level}
                    </span>
                  </div>
                  <div className="text-xs text-slate-400">{p.description}</div>
                </div>

                <div className="pl-4">
                  {isGranted ? (
                    <div className="w-7 h-7 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
                      <Check className="w-4 h-4" />
                    </div>
                  ) : (
                    <div className="w-7 h-7 rounded-lg bg-slate-800 text-slate-600 flex items-center justify-center font-mono text-xs">
                      -
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
