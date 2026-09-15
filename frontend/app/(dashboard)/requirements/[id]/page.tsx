'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import {
  DiscoverySessionDetail,
  getDiscoverySessionDetail,
  analyzeDiscoverySession,
  confirmRequirement,
  answerQuestion,
} from '@/lib/api/requirements';
import { RequirementsWorkspace } from '@/components/requirements/RequirementsWorkspace';

export default function DiscoverySessionDetailPage() {
  const params = useParams();
  const id = params?.id as string;

  const [sessionDetail, setSessionDetail] = useState<DiscoverySessionDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      if (!id) return;
      setLoading(true);
      setError(null);
      try {
        const data = await getDiscoverySessionDetail(id);
        setSessionDetail(data);
      } catch (err: any) {
        setError(err?.message || 'Failed to load discovery session workspace');
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
      const updated = await analyzeDiscoverySession(id);
      setSessionDetail(updated);
    } catch (err: any) {
      alert(`Analysis failed: ${err?.message || err}`);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleConfirmRequirement = async (reqId: string) => {
    if (!id) return;
    try {
      await confirmRequirement(id, reqId);
      const updated = await getDiscoverySessionDetail(id);
      setSessionDetail(updated);
    } catch (err: any) {
      alert(`Confirmation failed: ${err?.message || err}`);
    }
  };

  const handleAnswerQuestion = async (qId: string, answerText: string) => {
    if (!id) return;
    try {
      await answerQuestion(id, qId, answerText);
      const updated = await getDiscoverySessionDetail(id);
      setSessionDetail(updated);
    } catch (err: any) {
      alert(`Answering failed: ${err?.message || err}`);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-xs text-zinc-400">Loading discovery workspace...</div>;
  }

  if (error || !sessionDetail) {
    return (
      <div className="p-8 text-center text-xs text-rose-400">
        {error || 'Discovery session workspace not found.'}
      </div>
    );
  }

  return (
    <div className="p-6">
      <RequirementsWorkspace
        sessionDetail={sessionDetail}
        onAnalyze={handleAnalyze}
        onConfirmRequirement={handleConfirmRequirement}
        onAnswerQuestion={handleAnswerQuestion}
        isAnalyzing={analyzing}
      />
    </div>
  );
}
