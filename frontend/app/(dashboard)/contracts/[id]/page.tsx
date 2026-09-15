'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import {
  ContractDetail,
  getContractDetail,
  generateContract,
  approveContract,
  acceptContract,
  signContract,
  lockBaseline,
} from '@/lib/api/contracts';
import { ContractWorkspace } from '@/components/contracts/ContractWorkspace';

export default function ContractDetailPage() {
  const params = useParams();
  const id = params?.id as string;

  const [contractDetail, setContractDetail] = useState<ContractDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      if (!id) return;
      setLoading(true);
      setError(null);
      try {
        const data = await getContractDetail(id);
        setContractDetail(data);
      } catch (err: any) {
        setError(err?.message || 'Failed to load contract workspace');
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
      const updated = await generateContract(id);
      setContractDetail(updated);
    } catch (err: any) {
      alert(`Generation failed: ${err?.message || err}`);
    } finally {
      setGenerating(false);
    }
  };

  const handleApprove = async () => {
    if (!id) return;
    try {
      await approveContract(id);
      const updated = await getContractDetail(id);
      setContractDetail(updated);
    } catch (err: any) {
      alert(`Approval failed: ${err?.message || err}`);
    }
  };

  const handleAccept = async (clientEmail: string, acceptanceStatement: string) => {
    if (!id) return;
    try {
      await acceptContract(id, { client_email: clientEmail, acceptance_statement: acceptanceStatement });
      const updated = await getContractDetail(id);
      setContractDetail(updated);
    } catch (err: any) {
      alert(`Client acceptance failed: ${err?.message || err}`);
    }
  };

  const handleSign = async () => {
    if (!id) return;
    try {
      await signContract(id);
      const updated = await getContractDetail(id);
      setContractDetail(updated);
    } catch (err: any) {
      alert(`Signature execution failed: ${err?.message || err}`);
    }
  };

  const handleLockBaseline = async () => {
    if (!id) return;
    try {
      await lockBaseline(id);
      const updated = await getContractDetail(id);
      setContractDetail(updated);
    } catch (err: any) {
      alert(`Baseline locking failed: ${err?.message || err}`);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-xs text-zinc-400">Loading contract workspace...</div>;
  }

  if (error || !contractDetail) {
    return (
      <div className="p-8 text-center text-xs text-rose-400">
        {error || 'Contract workspace not found.'}
      </div>
    );
  }

  return (
    <div className="p-6">
      <ContractWorkspace
        contractDetail={contractDetail}
        onGenerate={handleGenerate}
        onApprove={handleApprove}
        onAccept={handleAccept}
        onSign={handleSign}
        onLockBaseline={handleLockBaseline}
        isGenerating={generating}
      />
    </div>
  );
}
