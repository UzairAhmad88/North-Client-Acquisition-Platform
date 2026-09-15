'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { listProjects, ProjectDetail } from '@/lib/api/projects';

export default function ProjectsDirectoryPage() {
  const [projects, setProjects] = useState<ProjectDetail[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProjects() {
      try {
        const res = await listProjects();
        setProjects(res?.items ?? []);
      } catch (err: any) {
        console.error('Failed to load projects:', err);
        setError(err?.message || 'Unable to load projects');
        setProjects([]);
      } finally {
        setLoading(false);
      }
    }
    fetchProjects();
  }, []);

  return (
    <div className="container mx-auto p-6 max-w-7xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Projects Command Center</h1>
          <p className="text-xs text-slate-500">Manage initiation, delivery WBS, tasks, and project health</p>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12 text-xs text-slate-400">Loading delivery projects...</div>
      ) : projects.length === 0 ? (
        <div className="bg-white dark:bg-slate-800 rounded-xl p-12 text-center border border-slate-200 dark:border-slate-700">
          <p className="text-sm text-slate-500 mb-2">No active projects found.</p>
          <p className="text-xs text-slate-400">Projects are automatically created upon signing a contract baseline.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <Link
              key={project.id}
              href={`/projects/${project.id}`}
              className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 hover:border-indigo-500 hover:shadow-md transition-all block"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300">
                  {project.project_number}
                </span>
                <span
                  className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    project.health === 'HEALTHY'
                      ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                      : 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300'
                  }`}
                >
                  {project.health}
                </span>
              </div>

              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 mb-1 line-clamp-1">{project.name}</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-2 mb-4">{project.description}</p>

              <div className="flex items-center justify-between text-xs text-slate-500 pt-3 border-t border-slate-100 dark:border-slate-700/50">
                <span>Status: <strong className="text-slate-700 dark:text-slate-300">{project.status}</strong></span>
                <span className="font-bold text-indigo-600 dark:text-indigo-400">{project.progress_percent}%</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
