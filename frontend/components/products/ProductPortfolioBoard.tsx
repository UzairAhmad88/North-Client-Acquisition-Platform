'use client';

import React from 'react';
import { Layers, Activity, ShieldAlert, CheckCircle, ArrowUpRight, Plus, Box } from 'lucide-react';
import { ProductItem } from '../../lib/api/productManagement';

interface ProductPortfolioBoardProps {
  products: ProductItem[];
  selectedProductId?: string;
  onSelectProduct: (id: string) => void;
  onCreateProduct: () => void;
}

export const ProductPortfolioBoard: React.FC<ProductPortfolioBoardProps> = ({
  products,
  selectedProductId,
  onSelectProduct,
  onCreateProduct,
}) => {
  const getHealthBadge = (health: string) => {
    switch (health) {
      case 'healthy':
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-semibold">Healthy</span>;
      case 'stable':
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 uppercase font-semibold">Stable</span>;
      case 'watch':
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase font-semibold">Watch</span>;
      default:
        return <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 uppercase font-semibold">At Risk</span>;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
            <Box className="h-4 w-4 text-indigo-400" />
            Product Portfolio & Lifecycle Matrix
          </h2>
          <p className="text-xs text-slate-400">Total Products: {products.length}</p>
        </div>
        <button
          onClick={onCreateProduct}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium transition-colors"
        >
          <Plus className="h-3.5 w-3.5" />
          New Product
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {products.map((p) => {
          const isSelected = p.id === selectedProductId;
          return (
            <div
              key={p.id}
              onClick={() => onSelectProduct(p.id)}
              className={`cursor-pointer rounded-xl border p-4 transition-all duration-200 ${
                isSelected
                  ? 'border-indigo-500 bg-indigo-950/20 ring-1 ring-indigo-500/30'
                  : 'border-slate-800 bg-slate-900/60 hover:border-slate-700 hover:bg-slate-900/90'
              }`}
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 uppercase font-medium">
                  {p.type}
                </span>
                {getHealthBadge(p.health)}
              </div>
              <h3 className="text-sm font-bold text-white mb-1 flex items-center justify-between">
                {p.name}
                <ArrowUpRight className="h-3.5 w-3.5 text-slate-500" />
              </h3>
              <p className="text-xs text-slate-400 line-clamp-2 mb-3">
                {p.description || 'Enterprise grade intelligence solution.'}
              </p>
              <div className="flex items-center justify-between text-[11px] text-slate-400 border-t border-slate-800/80 pt-2">
                <div>
                  Stage: <span className="text-indigo-400 font-semibold uppercase font-mono">{p.lifecycle_stage}</span>
                </div>
                <div>Owner: {p.owner}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
