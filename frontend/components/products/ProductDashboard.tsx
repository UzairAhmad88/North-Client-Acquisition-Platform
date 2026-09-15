'use client';

import React, { useState, useEffect } from 'react';
import {
  Layers,
  Compass,
  Link2,
  ListFilter,
  Activity,
  Bot,
  Rocket,
  ShieldCheck,
  Sparkles,
  RefreshCw,
} from 'lucide-react';
import { productApi, ProductItem, ProductDashboardData, TraceabilityMatrix } from '../../lib/api/productManagement';
import { ProductPortfolioBoard } from './ProductPortfolioBoard';
import { VisionStrategyPanel } from './VisionStrategyPanel';
import { RequirementsTraceabilityMatrix } from './RequirementsTraceabilityMatrix';
import { BacklogPrioritizer } from './BacklogPrioritizer';
import { ProductHealthGauge } from './ProductHealthGauge';
import { ProductCopilot } from './ProductCopilot';

export const ProductDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'portfolio' | 'strategy' | 'traceability' | 'backlog' | 'copilot'>('portfolio');
  const [products, setProducts] = useState<ProductItem[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<string>('prod-demo-001');
  const [dashboardData, setDashboardData] = useState<ProductDashboardData | null>(null);
  const [traceability, setTraceability] = useState<TraceabilityMatrix | null>(null);
  const [backlog, setBacklog] = useState<{ epics: any[]; features: any[]; items: any[] }>({ epics: [], features: [], items: [] });
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const portfolio = await productApi.getPortfolio();
      setProducts(portfolio.products || []);
      if (portfolio.products && portfolio.products.length > 0 && !selectedProductId) {
        setSelectedProductId(portfolio.products[0].id);
      }

      if (selectedProductId) {
        const d = await productApi.getProductDashboard(selectedProductId);
        setDashboardData(d);
        const t = await productApi.getTraceability(selectedProductId);
        setTraceability(t);
        const b = await productApi.getBacklog(selectedProductId);
        setBacklog(b);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedProductId]);

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4 md:p-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 uppercase font-semibold">
              Phase 56 Platform
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase font-semibold">
              Continuous Delivery OS
            </span>
          </div>
          <h1 className="text-2xl font-black text-white tracking-tight">
            Unified Product Lifecycle & Delivery Intelligence
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Closed-loop Product Operating System: Customer Problem → PRD → Traceability → Prioritized Backlog → Governed Release Gates.
          </p>
        </div>

        <button
          onClick={loadData}
          disabled={loading}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-colors"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Navigation Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-800 pb-2">
        <button
          onClick={() => setActiveTab('portfolio')}
          className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-lg transition-colors ${
            activeTab === 'portfolio'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <Layers className="h-4 w-4" />
          Product Portfolio
        </button>
        <button
          onClick={() => setActiveTab('strategy')}
          className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-lg transition-colors ${
            activeTab === 'strategy'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <Compass className="h-4 w-4" />
          Vision & North Star
        </button>
        <button
          onClick={() => setActiveTab('traceability')}
          className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-lg transition-colors ${
            activeTab === 'traceability'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <Link2 className="h-4 w-4" />
          Traceability Matrix
        </button>
        <button
          onClick={() => setActiveTab('backlog')}
          className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-lg transition-colors ${
            activeTab === 'backlog'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <ListFilter className="h-4 w-4" />
          Backlog & RICE Prioritizer
        </button>
        <button
          onClick={() => setActiveTab('copilot')}
          className={`flex items-center gap-2 px-3.5 py-2 text-xs font-bold rounded-lg transition-colors ${
            activeTab === 'copilot'
              ? 'bg-indigo-600 text-white shadow-lg'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
          }`}
        >
          <Bot className="h-4 w-4" />
          Product Co-Pilot
        </button>
      </div>

      {/* Main Tab Content */}
      <div className="space-y-6">
        {activeTab === 'portfolio' && (
          <ProductPortfolioBoard
            products={products}
            selectedProductId={selectedProductId}
            onSelectProduct={(id) => setSelectedProductId(id)}
            onCreateProduct={() => {}}
          />
        )}

        {activeTab === 'strategy' && dashboardData && (
          <VisionStrategyPanel
            vision={dashboardData.vision}
            objectives={dashboardData.objectives || []}
            metrics={dashboardData.metrics || []}
          />
        )}

        {activeTab === 'traceability' && traceability && (
          <RequirementsTraceabilityMatrix matrix={traceability} />
        )}

        {activeTab === 'backlog' && (
          <BacklogPrioritizer
            epics={backlog.epics}
            features={backlog.features}
            items={backlog.items}
          />
        )}

        {activeTab === 'copilot' && (
          <ProductCopilot productId={selectedProductId} />
        )}

        {/* Global Product Health Gauge at the bottom */}
        {dashboardData?.health && (
          <ProductHealthGauge health={dashboardData.health} />
        )}
      </div>
    </div>
  );
};
