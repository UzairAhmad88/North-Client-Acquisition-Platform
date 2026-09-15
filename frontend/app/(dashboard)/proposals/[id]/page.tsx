'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import {
  ProposalDetail,
  getProposalDetail,
  generateProposal,
  approveProposal,
} from '@/lib/api/proposals';
import { ProposalWorkspace } from '@/components/proposals/ProposalWorkspace';

export default function ProposalDetailPage() {
  const params = useParams();
  const id = params?.id as string;

  const [proposalDetail, setProposalDetail] = useState<ProposalDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      if (!id) return;
      setLoading(true);
      setError(null);
      try {
        const data = await getProposalDetail(id);
        setProposalDetail(data);
      } catch (err: any) {
        setError(err?.message || 'Failed to load proposal workspace');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  const handleGenerate = async () => {
    if (!id) return;
    setGenerating(true);
    try {
      const updated = await generateProposal(id);
      setProposalDetail(updated);
    } catch (err: any) {
      alert(`Generation failed: ${err?.message || err}`);
    } finally {
      setGenerating(false);
    }
  };

  const handleApprove = async () => {
    if (!id) return;
    try {
      await approveProposal(id);
      const updated = await getProposalDetail(id);
      setProposalDetail(updated);
    } catch (err: any) {
      alert(`Approval failed: ${err?.message || err}`);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-xs text-zinc-400">Loading proposal workspace...</div>;
  }

  if (error || !proposalDetail) {
    return (
      <div className="p-8 text-center text-xs text-rose-400">
        {error || 'Proposal workspace not found.'}
      </div>
    );
  }

  return (
    <div className="p-6">
      <ProposalWorkspace
        proposalDetail={proposalDetail}
        onGenerate={handleGenerate}
        onApprove={handleApprove}
        isGenerating={generating}
      />
    </div>
  );
}
