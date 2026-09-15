"use client";

import React, { useState } from "react";
import { ProductItem } from "@/lib/api/productOs";

interface Props {
  products: ProductItem[];
  onCreateProduct: (p: any) => Promise<void>;
}

export const PortfolioStrategyPanelView: React.FC<Props> = ({ products, onCreateProduct }) => {
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState("");
  const [productLine, setProductLine] = useState("Enterprise Intelligence");
  const [lifecycleState, setLifecycleState] = useState("DISCOVERY");
  const [targetIcp, setTargetIcp] = useState("Global 2000 CAIOs");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onCreateProduct({
      name,
      product_line: productLine,
      lifecycle_state: lifecycleState,
      target_icp: targetIcp,
      owner_email: "pm@uzaii.com",
    });
    setName("");
    setShowModal(false);
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Product Portfolio & Lifecycle</h2>
          <p className="text-xs text-slate-400">
            Hierarchical catalog tracking lifecycle progression from Discovery to Released and Sunset
          </p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-3 py-1.5 text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg transition shadow-sm"
        >
          + Add Product
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {products.map((p) => (
          <div
            key={p.product_id}
            className="p-4 bg-slate-950/60 border border-slate-800/80 rounded-lg space-y-2 hover:border-slate-700 transition"
          >
            <div className="flex items-center justify-between">
              <span className="font-semibold text-sm text-slate-200">{p.name}</span>
              <span
                className={`text-[10px] px-2 py-0.5 rounded font-mono ${
                  p.lifecycle_state === "RELEASED"
                    ? "bg-emerald-950/80 text-emerald-400 border border-emerald-800"
                    : p.lifecycle_state === "BETA"
                    ? "bg-cyan-950/80 text-cyan-400 border border-cyan-800"
                    : "bg-indigo-950/80 text-indigo-400 border border-indigo-800"
                }`}
              >
                {p.lifecycle_state}
              </span>
            </div>
            <p className="text-xs text-slate-400 line-clamp-2">{p.description || "Core platform offering"}</p>
            <div className="pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-500 font-mono">
              <span>Line: {p.product_line}</span>
              <span>ICP: {p.target_icp}</span>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-xl max-w-md w-full p-5 space-y-4">
            <h3 className="text-base font-semibold text-slate-100">Register New Product</h3>
            <form onSubmit={handleSubmit} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-400 mb-1">Product Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-slate-200"
                  placeholder="e.g. Uzaii Agent Governance Hub"
                />
              </div>
              <div>
                <label className="block text-slate-400 mb-1">Product Line</label>
                <input
                  type="text"
                  value={productLine}
                  onChange={(e) => setProductLine(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-slate-200"
                />
              </div>
              <div>
                <label className="block text-slate-400 mb-1">Lifecycle State</label>
                <select
                  value={lifecycleState}
                  onChange={(e) => setLifecycleState(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-slate-200"
                >
                  <option value="DISCOVERY">DISCOVERY</option>
                  <option value="DESIGN">DESIGN</option>
                  <option value="DEVELOPMENT">DEVELOPMENT</option>
                  <option value="BETA">BETA</option>
                  <option value="RELEASED">RELEASED</option>
                </select>
              </div>
              <div>
                <label className="block text-slate-400 mb-1">Target ICP</label>
                <input
                  type="text"
                  value={targetIcp}
                  onChange={(e) => setTargetIcp(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded px-3 py-2 text-slate-200"
                />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-3 py-1.5 bg-slate-800 text-slate-300 rounded hover:bg-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-3 py-1.5 bg-indigo-600 text-white rounded hover:bg-indigo-500"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
