'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { getProjectDetail, updateProjectStatus, updateTaskStatus, ProjectDetail } from '@/lib/api/projects';
import { ProjectWorkspace } from '@/components/projects/ProjectWorkspace';

export default function ProjectDetailPage() {
  const params = useParams();
  const projectId = params.id as string;
  const [project, setProject] = useState<ProjectDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadProject() {
      try {
        const data = await getProjectDetail(projectId);
        setProject(data);
      } catch (err) {
        console.error('Failed to fetch project detail:', err);
      } finally {
        setLoading(false);
      }
    }
    if (projectId) loadProject();
  }, [projectId]);

  const handleStatusChange = async (newStatus: string) => {
    try {
      const updated = await updateProjectStatus(projectId, newStatus);
      setProject(updated);
    } catch (err) {
      console.error('Failed to update project status:', err);
    }
  };

  const handleTaskStatusChange = async (taskId: string, newStatus: string) => {
    try {
      await updateTaskStatus(taskId, { status: newStatus });
      const updated = await getProjectDetail(projectId);
      setProject(updated);
    } catch (err) {
      console.error('Failed to update task status:', err);
    }
  };

  if (loading) {
    return <div className="text-center py-12 text-xs text-slate-400">Loading project workspace...</div>;
  }

  if (!project) {
    return <div className="text-center py-12 text-xs text-red-500">Project not found.</div>;
  }

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      <ProjectWorkspace
        project={project}
        onStatusChange={handleStatusChange}
        onTaskStatusChange={handleTaskStatusChange}
      />
    </div>
  );
}
