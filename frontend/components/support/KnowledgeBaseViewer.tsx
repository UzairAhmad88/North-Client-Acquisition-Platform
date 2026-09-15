'use client';

import React, { useState } from 'react';
import {
  BookOpen,
  Search,
  Tag,
  ThumbsUp,
  Plus,
  FileText,
} from 'lucide-react';
import { KnowledgeArticle, supportApi } from '@/lib/api/support';

interface KnowledgeBaseViewerProps {
  articles: KnowledgeArticle[];
  onRefresh: () => void;
}

export const KnowledgeBaseViewer: React.FC<KnowledgeBaseViewerProps> = ({
  articles,
  onRefresh,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [selectedArticle, setSelectedArticle] = useState<KnowledgeArticle | null>(null);

  // New Article modal
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('TROUBLESHOOTING');
  const [summary, setSummary] = useState('');
  const [content, setContent] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const categories = ['ALL', 'TROUBLESHOOTING', 'CONFIGURATION', 'MAINTENANCE', 'FAQ', 'SECURITY'];

  const filteredArticles = articles.filter((a) => {
    const matchesSearch =
      a.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.content.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'ALL' || a.article_type === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleCreateArticle = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await supportApi.createKnowledgeArticle({
        title,
        article_type: category,
        content,
      });
      setShowCreateModal(false);
      setTitle('');
      setContent('');
      setSummary('');
      onRefresh();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };


  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-indigo-400" />
              Knowledge Base & Standard Operating Procedures
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Curated runbooks, troubleshooting guides, FAQs, and post-delivery maintenance manuals
            </p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 transition"
          >
            <Plus className="w-4 h-4" /> Publish Article
          </button>
        </div>

        {/* Search & Filter Bar */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search knowledge base articles, error codes, runbooks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>
          <div className="flex items-center gap-1 overflow-x-auto pb-1">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`text-[11px] px-3 py-1.5 rounded-lg font-medium transition shrink-0 ${
                  selectedCategory === cat
                    ? 'bg-indigo-600 text-white'
                    : 'bg-slate-950 text-slate-400 border border-slate-800 hover:text-slate-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Articles List / Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredArticles.map((article) => (
            <div
              key={article.id}
              onClick={() => setSelectedArticle(article)}
              className="p-4 bg-slate-950 rounded-xl border border-slate-800 hover:border-indigo-500/50 cursor-pointer transition flex flex-col justify-between"
            >
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                  {article.article_type || 'USER_GUIDE'}
                </span>
                <h4 className="text-sm font-bold text-white mt-2 line-clamp-1">{article.title}</h4>
                <p className="text-xs text-slate-400 mt-1 line-clamp-2">{article.content}</p>
              </div>
              <div className="mt-4 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500">
                <span className="flex items-center gap-1">
                  <ThumbsUp className="w-3 h-3 text-slate-400" /> By {article.author || 'System'}
                </span>
                <span>{new Date(article.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>

      </div>

      {/* Article Viewer Modal */}
      {selectedArticle && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 space-y-4 shadow-2xl max-h-[85vh] overflow-y-auto">
            <div className="flex items-start justify-between border-b border-slate-800 pb-3">
              <div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400">
                  {selectedArticle.article_type || 'USER_GUIDE'}
                </span>
                <h3 className="text-lg font-bold text-white mt-1">{selectedArticle.title}</h3>
              </div>
              <button
                onClick={() => setSelectedArticle(null)}
                className="text-xs text-slate-400 hover:text-white"
              >
                Close
              </button>
            </div>

            <div className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap font-sans bg-slate-950 p-4 rounded-xl border border-slate-800">
              {selectedArticle.content}
            </div>

            <div className="flex items-center justify-between pt-2 text-xs text-slate-400">
              <span className="flex items-center gap-1">
                <Tag className="w-3.5 h-3.5 text-indigo-400" />
                By {selectedArticle.author || 'System'}
              </span>
              <button
                onClick={() => setSelectedArticle(null)}
                className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg font-semibold"
              >
                Done
              </button>
            </div>
          </div>
        </div>

      )}

      {/* Publish Article Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <Plus className="w-5 h-5 text-indigo-400" />
              Publish Knowledge Article
            </h3>
            <form onSubmit={handleCreateArticle} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. How to restart ingestion background workers"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-400 mb-1 font-semibold">Category</label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                  >
                    <option value="TROUBLESHOOTING">TROUBLESHOOTING</option>
                    <option value="CONFIGURATION">CONFIGURATION</option>
                    <option value="MAINTENANCE">MAINTENANCE</option>
                    <option value="FAQ">FAQ</option>
                    <option value="SECURITY">SECURITY</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Summary</label>
                <input
                  type="text"
                  value={summary}
                  onChange={(e) => setSummary(e.target.value)}
                  placeholder="Brief 1-sentence summary..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 mb-1 font-semibold">Content (Markdown / Steps)</label>
                <textarea
                  required
                  rows={6}
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="Step 1: Check logs...&#10;Step 2: Run restart command..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white font-mono text-xs"
                />
              </div>
              <div className="flex justify-end gap-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-bold"
                >
                  {submitting ? 'Publishing...' : 'Publish Article'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
