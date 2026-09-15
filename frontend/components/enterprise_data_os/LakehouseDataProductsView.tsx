"use client";

import React, { useState } from "react";
import { LakehouseDatasetItem, DataProductItem } from "@/lib/api/enterpriseDataOs";

interface Props {
  datasets: LakehouseDatasetItem[];
  products: DataProductItem[];
}

export const LakehouseDataProductsView: React.FC<Props> = ({ datasets, products }) => {
  const [activeTab, setActiveTab] = useState<"datasets" | "products">("products");

  return (
    <div className="bg-slate-900/60 backdrop-blur border border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Lakehouse Tiers & Curated Gold Data Products</h2>
          <p className="text-xs text-slate-400">
            Bronze raw storage, Silver validated datasets, and Gold enterprise reusable data products
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-slate-800/80 p-1 rounded-lg border border-slate-700/50">
          <button
            onClick={() => setActiveTab("products")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "products"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Data Products ({products.length})
          </button>
          <button
            onClick={() => setActiveTab("datasets")}
            className={`px-3 py-1 text-xs font-medium rounded-md transition ${
              activeTab === "datasets"
                ? "bg-indigo-600 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Lakehouse Datasets ({datasets.length})
          </button>
        </div>
      </div>

      <div className="mt-4">
        {activeTab === "products" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {products.map((prod) => (
              <div
                key={prod.product_id}
                className="bg-slate-800/40 border border-slate-700/60 rounded-lg p-4 hover:border-indigo-500/50 transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-bold text-slate-100 text-sm">{prod.name}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded font-bold uppercase bg-emerald-950 text-emerald-400 border border-emerald-800">
                      {prod.health_status}
                    </span>
                  </div>

                  <p className="text-xs text-slate-400 mb-3">{prod.purpose}</p>

                  <div className="bg-slate-900/80 rounded p-2.5 mb-3 border border-slate-800 text-xs space-y-1">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Owner Team:</span>
                      <span className="text-slate-200 font-medium">{prod.owner_team}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Quality Index:</span>
                      <span className="text-emerald-400 font-bold font-mono">{prod.quality_score}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Active Consumers:</span>
                      <span className="text-indigo-400 font-mono">{prod.consumers_count} Systems / Teams</span>
                    </div>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-700/40 flex justify-between items-center text-[11px] text-slate-500">
                  <span>Underlying: {prod.underlying_datasets?.length || 0} Tables</span>
                  <span className="text-slate-400 font-mono text-[10px]">Product ID: {prod.product_id}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "datasets" && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-800/50 text-slate-400 uppercase tracking-wider font-semibold">
                <tr>
                  <th className="p-3">Dataset</th>
                  <th className="p-3">Layer</th>
                  <th className="p-3">Format</th>
                  <th className="p-3">Records / Size</th>
                  <th className="p-3">Classification</th>
                  <th className="p-3">Quality</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {datasets.map((ds) => (
                  <tr key={ds.dataset_id} className="hover:bg-slate-800/30 transition">
                    <td className="p-3">
                      <div className="font-semibold text-slate-100">{ds.name}</div>
                      <div className="text-[10px] text-slate-500 font-mono">{ds.storage_uri}</div>
                    </td>
                    <td className="p-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          ds.layer === "GOLD"
                            ? "bg-amber-950 text-amber-300 border border-amber-800"
                            : ds.layer === "SILVER"
                            ? "bg-slate-700 text-slate-200 border border-slate-600"
                            : "bg-amber-900/60 text-amber-200"
                        }`}
                      >
                        {ds.layer}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-slate-300">{ds.format}</td>
                    <td className="p-3 text-slate-300">
                      {ds.record_count.toLocaleString()} rows · {ds.size_mb} MB
                    </td>
                    <td className="p-3">
                      <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 font-mono">
                        {ds.classification}
                      </span>
                    </td>
                    <td className="p-3 text-emerald-400 font-bold">{ds.quality_status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
