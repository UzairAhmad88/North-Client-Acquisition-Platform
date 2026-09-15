'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import {
  SolutionDesignDetail,
  getSolutionDesignDetail,
  analyzeSolutionDesign,
  approveSolutionDesign,
} from '@/lib/api/solutions';
import { SolutionWorkspace } from '@/components/solution/SolutionWorkspace';

export default function SolutionDetailPage() {
  const params = useParams();
  const id = params?.id as string;

  const [solutionDetail, setSolutionDetail] = useState<SolutionDesignDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      if (!id) return;
      setLoading(true);
      setError(null);
      try {
        const data = await getSolutionDesignDetail(id);
        setSolutionDetail(data);
      } catch (err: any) {
        setError(err?.message || 'Failed to load solution design workspace');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  const handleAnalyze = async () => {
    if (!id) return;
    setAnalyzing(true);
    try {
      const updated = await analyzeSolutionDesign(id);
      setSolutionDetail(updated);
    } catch (err: any) {
      alert(`Analysis failed: ${err?.message || err}`);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleApprove = async () => {
    if (!id) return;
    try {
      await approveSolutionDesign(id);
      const updated = await getSolutionDesignDetail(id);
      setSolutionDetail(updated);
    } catch (err: any) {
      alert(`Approval failed: ${err?.message || err}`);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-xs text-zinc-400">Loading solution workspace...</div>;
  }

  if (error || !solutionDetail) {
    return (
      <div className="p-8 text-center text-xs text-rose-400">
        {error || 'Solution design workspace not found.'}
      </div>
    );
  }

  return (
    <div className="p-6">
      <SolutionWorkspace
        solutionDetail={solutionDetail}
        onAnalyze={handleAnalyze}
        onApprove={handleApprove}
        isAnalyzing={analyzing}
      />
    </div>
  );
}
