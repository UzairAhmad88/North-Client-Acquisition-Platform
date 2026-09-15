import React from 'react';
import { AssistantPanel } from '@/components/assistant/AssistantPanel';
import { CommandPalette } from '@/components/command/CommandPalette';

export const metadata = {
  title: 'Platform Assistant | Uzaii',
  description: 'AI platform assistant with grounded provenance citations and query planning.',
};

export default function AssistantPage() {
  return (
    <div className="p-4 md:p-6 max-w-5xl mx-auto space-y-6">
      <AssistantPanel />
      <CommandPalette />
    </div>
  );
}
