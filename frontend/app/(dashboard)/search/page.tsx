import React from 'react';
import { GlobalSearch } from '@/components/search/GlobalSearch';
import { CommandPalette } from '@/components/command/CommandPalette';

export const metadata = {
  title: 'Global Search | Uzaii',
  description: 'Unified cross-entity discovery across leads, projects, proposals, contracts, and knowledge.',
};

export default function SearchPage() {
  return (
    <div className="p-4 md:p-6 max-w-7xl mx-auto space-y-6">
      <GlobalSearch />
      <CommandPalette />
    </div>
  );
}
