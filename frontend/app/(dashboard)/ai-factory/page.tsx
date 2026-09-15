import React from 'react';
import { Metadata } from 'next';
import { AiModelFactoryDashboard } from '@/components/ai_model_factory';

export const metadata: Metadata = {
  title: 'AI Model Factory & MLOps OS | Uzaii Develop By North\'s',
  description: 'Centralized AI/ML Model Factory, MLOps, LLMOps, Benchmarking, Inference Gateway, and Production AI Operating System.',
};

export default function AiModelFactoryPage() {
  return <AiModelFactoryDashboard />;
}
