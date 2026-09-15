'use client';

import React, { useState } from 'react';
import { DiscoveryQuestion } from '@/lib/api/requirements';

interface DiscoveryQuestionsProps {
  questions: DiscoveryQuestion[];
  onAnswerQuestion?: (questionId: string, answerText: string) => void;
}

export function DiscoveryQuestions({ questions, onAnswerQuestion }: DiscoveryQuestionsProps) {
  const [activeQuestionId, setActiveQuestionId] = useState<string | null>(null);
  const [answerInput, setAnswerInput] = useState('');

  if (!questions || questions.length === 0) {
    return (
      <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-6 text-center text-xs text-slate-400">
        No discovery questions active.
      </div>
    );
  }

  const handleAnswerSubmit = (qId: string) => {
    if (!answerInput.trim() || !onAnswerQuestion) return;
    onAnswerQuestion(qId, answerInput.trim());
    setActiveQuestionId(null);
    setAnswerInput('');
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-md">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-300">
        Prioritized Discovery Questions ({questions.length})
      </h3>
      <div className="space-y-4">
        {questions.map((q) => {
          const isAnswered = q.status === 'ANSWERED';
          return (
            <div key={q.id} className="rounded-lg border border-slate-800 bg-slate-950/40 p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`rounded px-2 py-0.5 text-[10px] font-semibold uppercase ${
                        q.priority === 'CRITICAL'
                          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                          : 'bg-amber-500/20 text-amber-300'
                      }`}
                    >
                      {q.priority}
                    </span>
                    <span className="text-[10px] text-slate-400">Category: {q.category}</span>
                  </div>
                  <h4 className="mt-2 text-sm font-semibold text-slate-100">{q.question}</h4>
                  {q.reason && <p className="mt-1 text-xs text-slate-400 italic">Why: {q.reason}</p>}
                </div>

                <span
                  className={`shrink-0 rounded px-2.5 py-1 text-[10px] font-semibold uppercase ${
                    isAnswered ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-300'
                  }`}
                >
                  {q.status}
                </span>
              </div>

              {isAnswered && q.answer_text && (
                <div className="mt-3 rounded border border-emerald-500/30 bg-emerald-950/20 p-2.5 text-xs text-emerald-200">
                  <strong>Answer:</strong> {q.answer_text}
                </div>
              )}

              {!isAnswered && (
                <div className="mt-3">
                  {activeQuestionId === q.id ? (
                    <div className="space-y-2">
                      <textarea
                        value={answerInput}
                        onChange={(e) => setAnswerInput(e.target.value)}
                        placeholder="Type client answer here..."
                        rows={2}
                        className="w-full rounded border border-slate-700 bg-slate-900 p-2 text-xs text-slate-200 focus:border-indigo-500 focus:outline-none"
                      />
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => setActiveQuestionId(null)}
                          className="rounded bg-slate-800 px-3 py-1 text-xs text-slate-400 hover:bg-slate-700"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={() => handleAnswerSubmit(q.id)}
                          className="rounded bg-indigo-600 px-3 py-1 text-xs font-semibold text-white hover:bg-indigo-500"
                        >
                          Save Answer
                        </button>
                      </div>
                    </div>
                  ) : (
                    <button
                      onClick={() => {
                        setActiveQuestionId(q.id);
                        setAnswerInput('');
                      }}
                      className="rounded bg-slate-800 px-3 py-1 text-xs font-medium text-slate-300 hover:bg-slate-700 transition-colors"
                    >
                      Answer Question
                    </button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
