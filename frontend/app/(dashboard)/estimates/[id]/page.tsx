'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import {
  ProjectEstimateDetail,
  getEstimateDetail,
  calculateEstimate,
  approveEstimate,
} from '@/lib/api/estimates';
import { EstimateWorkspace } from '@/components/estimation/EstimateWorkspace';

export default function EstimateDetailPage() {
  const params = useParams();
  const id = params?.id as string;

  const [estimateDetail, setEstimateDetail] = useState<ProjectEstimateDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [calculating, setCalculating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      if (!id) return;
      setLoading(true);
      setError(null);
      try {
        const data = await getEstimateDetail(id);
        setEstimateDetail(data);
      } catch (err: any) {
        setError(err?.message || 'Failed to load estimate workspace');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  const handleCalculate = async () => {
    if (!id) return;
    setCalculating(true);
    try {
      const updated = await calculateEstimate(id);
      setEstimateDetail(updated);
    } catch (err: any) {
      alert(`Calculation failed: ${err?.message || err}`);
    } finally {
      setCalculating(false);
    }
  };

  const handleApprove = async () => {
    if (!id) return;
    try {
      await approveEstimate(id);
      const updated = await getEstimateDetail(id);
      setEstimateDetail(updated);
    } catch (err: any) {
      alert(`Approval failed: ${err?.message || err}`);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-xs text-zinc-400">Loading estimate workspace...</div>;
  }

  if (error || !estimateDetail) {
    return (
      <div className="p-8 text-center text-xs text-rose-400">
        {error || 'Estimate workspace not found.'}
      </div>
    );
  }

  return (
    <div className="p-6">
      <EstimateWorkspace
        estimateDetail={estimateDetail}
        onCalculate={handleCalculate}
        onApprove={handleApprove}
        isCalculating={calculating}
      />
    </div>
  );
}
