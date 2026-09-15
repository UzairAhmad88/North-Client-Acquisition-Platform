'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';

interface ResponseDraftEditorProps {
  conversationId: string;
  onGenerateDraft?: () => void;
}

export function ResponseDraftEditor({ conversationId, onGenerateDraft }: ResponseDraftEditorProps) {
  const [draftSubject, setDraftSubject] = useState('');
  const [draftBody, setDraftBody] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      if (onGenerateDraft) onGenerateDraft();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-5 rounded-xl bg-zinc-900 border border-zinc-800 space-y-3 text-xs">
      <div className="flex justify-between items-center pb-2 border-b border-zinc-800">
        <h3 className="font-bold text-zinc-100 text-sm">Response Draft & Human Review</h3>
        <Button size="sm" onClick={handleGenerate} disabled={loading} className="bg-indigo-600 hover:bg-indigo-500 text-white">
          {loading ? 'Generating...' : 'Generate AI Response Draft'}
        </Button>
      </div>

      <div>
        <label className="text-[11px] text-zinc-400 block mb-1">Subject</label>
        <input
          type="text"
          value={draftSubject}
          onChange={(e) => setDraftSubject(e.target.value)}
          placeholder="Response Subject..."
          className="w-full p-2 bg-zinc-950 border border-zinc-800 rounded text-xs text-zinc-200"
        />
      </div>

      <div>
        <label className="text-[11px] text-zinc-400 block mb-1">Message Body</label>
        <textarea
          value={draftBody}
          onChange={(e) => setDraftBody(e.target.value)}
          placeholder="Compose or review response draft..."
          rows={5}
          className="w-full p-2.5 bg-zinc-950 border border-zinc-800 rounded text-xs text-zinc-200 font-sans leading-relaxed"
        />
      </div>

      <div className="p-3 rounded-lg bg-zinc-950 border border-zinc-800 text-[11px] text-zinc-400 flex justify-between items-center">
        <span>Drafts must pass Risk & Quality evaluation and Human Approval before send dispatch.</span>
        <Button size="sm" variant="outline" className="text-zinc-200 border-zinc-700">
          Save Draft
        </Button>
      </div>
    </div>
  );
}
