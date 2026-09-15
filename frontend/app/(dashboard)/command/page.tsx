import React from 'react';
import { CommandCenterWorkspace } from '@/components/command/CommandCenterWorkspace';

export const metadata = {
  title: 'Command Center | Uzaii',
  description: 'Global command center, keyboard shortcuts, and natural-language interaction.',
};

export default function CommandPage() {
  return (
    <div className="p-4 md:p-6 max-w-7xl mx-auto">
      <CommandCenterWorkspace />
    </div>
  );
}
