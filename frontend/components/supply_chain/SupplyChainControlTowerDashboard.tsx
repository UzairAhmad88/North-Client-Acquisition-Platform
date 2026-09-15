'use client';

import React, { useState } from 'react';
import {
  Truck,
  Box,
  Boxes,
  Compass,
  AlertTriangle,
  Play,
  CheckCircle2,
  XCircle,
  Clock,
  RotateCcw,
  Zap,
  TrendingUp,
  Workflow,
  Search,
  BookOpen,
  Gauge,
  Sparkles,
  BarChart3,
  Check,
  ChevronRight,
  Eye,
  Settings,
  Shield,
  RefreshCw,
  Radio,
  MapPin,
  Thermometer,
  BatteryCharging,
  Bot,
  Factory,
  Layers,
  DollarSign,
  Package,
  Globe,
  Sliders,
  Anchor
} from 'lucide-react';

export default function SupplyChainControlTowerDashboard() {
  const [roleView, setRoleView] = useState<'vp_supply_chain' | 'logistics_dir' | 'warehouse_lead' | 'procurement_mgr' | 'resilience_eng'>('vp_supply_chain');
  const [activeTab, setActiveTab] = useState<'overview' | 'suppliers' | 'inventory' | 'warehouses' | 'transport' | 'shipments' | 'disruptions' | 'agents'>('overview');

  // Closed-loop 11-stage cycle simulator
  const [cycleRunning, setCycleRunning] = useState(false);
  const [cycleStep, setCycleStep] = useState(0);
  const [cycleResult, setCycleResult] = useState<any>(null);

  const runOperatingCycle = () => {
    setCycleRunning(true);
    setCycleStep(1);
    setCycleResult(null);

    const timer = setInterval(() => {
      setCycleStep((prev) => {
        if (prev >= 11) {
          clearInterval(timer);
          setCycleRunning(false);
          setCycleResult({
            cycleId: `sc_cyc_${Math.random().toString(36).substring(2, 8)}`,
            status: 'COMPLETED',
            actions: [
              'Ingested multi-echelon telemetry from 8 global hubs',
              'Generated 30-day probabilistic demand forecast (MAPE 94.2%)',
              'Calculated net MRP component requirements',
              'Evaluated contingency alternate routing around Suez chokepoint',
              'Solved mixed-integer VRP routing (projected fuel savings 14.2%)',
              'Flagged PO-2026-9001 ($145,000) for dual-control human authorization',
              'Synchronized digital twin nodes and cold-chain sensors'
            ]
          });
          return 11;
        }
        return prev + 1;
      });
    }, 320);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header & Role Bar */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-500/10 border border-blue-500/30 rounded-xl text-blue-400">
              <Globe className="w-7 h-7" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-blue-400 via-indigo-300 to-teal-300 bg-clip-text text-transparent">
                Global Autonomous Supply Chain Control Tower
              </h1>
              <p className="text-sm text-slate-400">
                Phase 71 &bull; Autonomous Logistics, Multi-Echelon Inventory, Warehousing, Fleet Intelligence &amp; Physical Commerce
              </p>
            </div>
          </div>
        </div>

        {/* Role Persona Switcher */}
        <div className="flex items-center gap-2 bg-slate-900/80 p-1.5 rounded-lg border border-slate-800 text-xs">
          <span className="text-slate-500 font-medium px-2">Role Persona:</span>
          {(['vp_supply_chain', 'logistics_dir', 'warehouse_lead', 'procurement_mgr', 'resilience_eng'] as const).map((r) => (
            <button
              key={r}
              onClick={() => setRoleView(r)}
              className={`px-3 py-1.5 rounded-md font-medium capitalize transition-all ${
                roleView === r
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              {r.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Top Level Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400">Global Resilience Index</p>
            <p className="text-2xl font-bold text-emerald-400 mt-1">94.6%</p>
            <p className="text-[11px] text-emerald-500/80 mt-0.5 flex items-center gap-1">
              <Shield className="w-3 h-3" /> High Resilience Buffer
            </p>
          </div>
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
            <Shield className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400">Total Inventory Valuation</p>
            <p className="text-2xl font-bold text-blue-400 mt-1">$18.45M</p>
            <p className="text-[11px] text-slate-400 mt-0.5">8 Hubs &bull; 72.4% Capacity</p>
          </div>
          <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-400">
            <Boxes className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400">On-Time Delivery SLA</p>
            <p className="text-2xl font-bold text-teal-400 mt-1">98.4%</p>
            <p className="text-[11px] text-teal-500/80 mt-0.5">420 Shipments In Transit</p>
          </div>
          <div className="p-3 bg-teal-500/10 border border-teal-500/20 rounded-xl text-teal-400">
            <Truck className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400">Autonomous AI Agents</p>
            <p className="text-2xl font-bold text-indigo-400 mt-1">22 Active</p>
            <p className="text-[11px] text-indigo-400 mt-0.5">Zero-Trust Governed</p>
          </div>
          <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-400">
            <Bot className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Autonomous Operating Cycle Runner */}
      <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
          <div>
            <div className="flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" />
              <h2 className="text-base font-semibold text-slate-100">Closed-Loop Autonomous Supply Chain Cycle</h2>
              <span className="text-[11px] px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30">
                11 Stages
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Observe &rarr; Forecast &rarr; Plan &rarr; Simulate &rarr; Optimize &rarr; Policy Check &rarr; Approval &rarr; Execute &rarr; Verify &rarr; Learn &rarr; Audit
            </p>
          </div>
          <button
            onClick={runOperatingCycle}
            disabled={cycleRunning}
            className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all ${
              cycleRunning
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-blue-600/20'
            }`}
          >
            <Play className="w-4 h-4 fill-current" />
            {cycleRunning ? 'Executing Cycle...' : 'Run Autonomous Cycle'}
          </button>
        </div>

        {/* 11 Stage Stepper */}
        <div className="grid grid-cols-3 sm:grid-cols-6 lg:grid-cols-11 gap-2 pt-2">
          {[
            '1. Observe', '2. Forecast', '3. Plan', '4. Simulate', '5. Optimize',
            '6. Policy', '7. Approve', '8. Execute', '9. Verify', '10. Learn', '11. Audit'
          ].map((stage, idx) => {
            const num = idx + 1;
            const isCompleted = cycleStep > num;
            const isCurrent = cycleStep === num;
            return (
              <div
                key={stage}
                className={`p-2.5 rounded-lg border text-center transition-all ${
                  isCurrent
                    ? 'bg-blue-500/20 border-blue-500 text-blue-300 shadow-md shadow-blue-500/10'
                    : isCompleted
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                    : 'bg-slate-900/60 border-slate-800/80 text-slate-500'
                }`}
              >
                <div className="flex items-center justify-center gap-1 text-[11px] font-medium">
                  {isCompleted ? <Check className="w-3 h-3 text-emerald-400" /> : null}
                  {stage}
                </div>
              </div>
            );
          })}
        </div>

        {cycleResult && (
          <div className="mt-3 p-3 bg-blue-950/40 border border-blue-800/60 rounded-lg text-xs space-y-1">
            <div className="flex items-center justify-between text-blue-300 font-semibold">
              <span>Execution Summary &bull; {cycleResult.cycleId}</span>
              <span className="text-emerald-400 font-bold">Status: {cycleResult.status}</span>
            </div>
            <ul className="list-disc list-inside text-slate-300 space-y-0.5 pt-1">
              {cycleResult.actions.map((act: string, i: number) => (
                <li key={i}>{act}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-slate-800 gap-2 overflow-x-auto text-xs pb-1">
        {[
          { id: 'overview', label: 'Network Overview', icon: Globe },
          { id: 'suppliers', label: 'Suppliers & Procurement', icon: DollarSign },
          { id: 'inventory', label: 'Inventory & MRP', icon: Boxes },
          { id: 'warehouses', label: 'Warehousing & AMRs', icon: Factory },
          { id: 'transport', label: 'Fleet & VRP Routing', icon: Truck },
          { id: 'shipments', label: 'Shipments & Cold Chain', icon: Package },
          { id: 'disruptions', label: 'Disruptions & Resilience', icon: AlertTriangle },
          { id: 'agents', label: '22 Autonomous Agents', icon: Bot },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-t-lg font-medium whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'border-b-2 border-blue-500 text-blue-400 bg-slate-900/80 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab Panels */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Globe className="w-4 h-4 text-blue-400" />
              Global Supply Network Topology &amp; Physical Hubs
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="p-3.5 bg-slate-900 border border-slate-800 rounded-lg space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-xs text-blue-300">WH-ORD-01 (Chicago Mega Hub)</span>
                  <span className="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded">OPERATIONAL</span>
                </div>
                <p className="text-xs text-slate-400">Capacity: 24,500 / 35,000 pallets (70.0%)</p>
                <div className="flex justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800/60">
                  <span>38 AMR Robots Active</span>
                  <span>142 Workers</span>
                </div>
              </div>

              <div className="p-3.5 bg-slate-900 border border-slate-800 rounded-lg space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-xs text-blue-300">WH-RTM-01 (Rotterdam EuroPort)</span>
                  <span className="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded">OPERATIONAL</span>
                </div>
                <p className="text-xs text-slate-400">Capacity: 29,800 / 42,000 pallets (70.9%)</p>
                <div className="flex justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800/60">
                  <span>54 AMR Robots Active</span>
                  <span>165 Workers</span>
                </div>
              </div>
            </div>

            <div className="p-3.5 bg-slate-950 border border-slate-800/80 rounded-lg space-y-2">
              <h4 className="text-xs font-semibold text-slate-300">Active Freight Corridors &amp; Routing Optimization</h4>
              <div className="flex justify-between text-xs text-slate-400 py-1 border-b border-slate-800">
                <span>RT-ORD-JFK-01 (Chicago &rarr; New York)</span>
                <span className="text-emerald-400 font-medium">18.0h Transit &bull; Fuel Opt: -14.2%</span>
              </div>
              <div className="flex justify-between text-xs text-slate-400 py-1">
                <span>RT-RTM-MUC-02 (Rotterdam &rarr; Munich)</span>
                <span className="text-emerald-400 font-medium">12.5h Transit &bull; VRP Solved</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Shield className="w-4 h-4 text-emerald-400" />
              Resilience &amp; Concentration Risk
            </h3>
            <div className="space-y-3">
              <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Supplier Concentration Risk</span>
                  <span className="text-emerald-400 font-semibold">18.2% (Target &lt; 25%)</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: '18.2%' }} />
                </div>
              </div>

              <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Buffer Inventory Health</span>
                  <span className="text-blue-400 font-semibold">96.4%</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: '96.4%' }} />
                </div>
              </div>

              <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Contingency Alternate Coverage</span>
                  <span className="text-teal-400 font-semibold">98.1%</span>
                </div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-teal-500 h-1.5 rounded-full" style={{ width: '98.1%' }} />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'suppliers' && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-slate-200">Tier 1 &amp; Tier 2 Commercial Suppliers &amp; PO Sign-off Gates</h3>
            <span className="text-xs text-amber-400 bg-amber-500/10 border border-amber-500/30 px-2.5 py-1 rounded-md">
              Dual-Control Authorization Required for PO &gt; $50,000
            </span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-2.5">Supplier Code</th>
                  <th>Company Name</th>
                  <th>Tier</th>
                  <th>Country</th>
                  <th>On-Time Rate</th>
                  <th>Defect PPM</th>
                  <th>Risk Score</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                <tr>
                  <td className="py-2.5 font-medium text-blue-400">SUP-ALPHA</td>
                  <td>Alpha Semi &amp; Microchips Corp</td>
                  <td>TIER_1</td>
                  <td>TW</td>
                  <td className="text-emerald-400">97.8%</td>
                  <td>12.0 ppm</td>
                  <td>14.5 / 100</td>
                  <td><span className="bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded">COMPLIANT</span></td>
                </tr>
                <tr>
                  <td className="py-2.5 font-medium text-blue-400">SUP-BETA</td>
                  <td>Beta Precision Metals &amp; Alloys</td>
                  <td>TIER_1</td>
                  <td>DE</td>
                  <td className="text-emerald-400">98.4%</td>
                  <td>8.5 ppm</td>
                  <td>9.2 / 100</td>
                  <td><span className="bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded">COMPLIANT</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'inventory' && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="text-sm font-semibold text-slate-200">Multi-Echelon Inventory &amp; MRP Stock Balancing</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-semibold text-xs text-blue-300">SKU-NV-A100 (AI Accelerator Module)</span>
                <span className="text-[11px] text-slate-400">WH-ORD-01 &bull; Bin A-12-04</span>
              </div>
              <p className="text-xs text-slate-300">On Hand: 1,840 units &bull; Available: 1,420 units &bull; Allocated: 420 units</p>
              <div className="text-[11px] text-slate-400 flex justify-between border-t border-slate-800/80 pt-2">
                <span>Safety Stock: 250 units</span>
                <span>Reorder Point: 600 units</span>
                <span className="text-emerald-400">Stockout Risk: 4.5%</span>
              </div>
            </div>

            <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-semibold text-xs text-blue-300">SKU-BIO-SENS (Cryo-Biosensor Cartridge)</span>
                <span className="text-[11px] text-slate-400">WH-RTM-01 &bull; Bin C-02-01</span>
              </div>
              <p className="text-xs text-slate-300">On Hand: 5,400 units &bull; Available: 4,300 units &bull; Allocated: 1,100 units</p>
              <div className="text-[11px] text-slate-400 flex justify-between border-t border-slate-800/80 pt-2">
                <span>Safety Stock: 800 units</span>
                <span>Reorder Point: 1,800 units</span>
                <span className="text-emerald-400">Stockout Risk: 2.1%</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'agents' && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-slate-200">22 Autonomous Supply Chain AI Agents</h3>
            <span className="text-xs text-blue-400 font-medium">Zero-Trust &amp; Cyber-Physical Integrated</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {[
              { name: 'SupplyChainOrchestratorAgent', id: 'sc_orchestrator', role: 'Master 11-stage cycle coordination' },
              { name: 'SupplierAgent', id: 'sc_supplier', role: 'Supplier scoring & PPM defect tracking' },
              { name: 'ProcurementAgent', id: 'sc_procurement', role: 'PO issuance with dual-authorization gates' },
              { name: 'DemandAgent', id: 'sc_demand', role: 'Velocity monitoring & sudden spike detection' },
              { name: 'ForecastingAgent', id: 'sc_forecasting', role: 'Multi-horizon MAPE probabilistic forecast' },
              { name: 'InventoryAgent', id: 'sc_inventory', role: 'Safety stock & multi-echelon balancing' },
              { name: 'WarehouseAgent', id: 'sc_warehouse', role: 'Golden-zone slotting & AMR coordination' },
              { name: 'PickingAgent', id: 'sc_picking', role: 'Wave sequencing & robot pick missions' },
              { name: 'PackingAgent', id: 'sc_packing', role: 'Carton dimensions & eco-cushioning optimization' },
              { name: 'ShippingAgent', id: 'sc_shipping', role: 'Manifest generation & carrier handoff' },
              { name: 'TransportationAgent', id: 'sc_transportation', role: 'Multimodal freight capacity & SLA compliance' },
              { name: 'FleetAgent', id: 'sc_fleet', role: 'Private vehicle telemetry & battery charging' },
              { name: 'RoutingAgent', id: 'sc_routing', role: 'Mixed-integer VRP route solver' },
              { name: 'EtaAgent', id: 'sc_eta', role: 'Dynamic weather/traffic ETA prediction' },
              { name: 'DisruptionAgent', id: 'sc_disruption', role: 'Chokepoint detection & contingency lanes' },
              { name: 'ResilienceAgent', id: 'sc_resilience', role: 'Stress testing single points of failure' },
              { name: 'OrderAgent', id: 'sc_order', role: 'Sales order allocation & fulfillment' },
              { name: 'ReturnsAgent', id: 'sc_returns', role: 'RMA inspection, grading & restock' },
              { name: 'CostAgent', id: 'sc_cost', role: 'True landed cost & tariff accounting' },
              { name: 'SustainabilityAgent', id: 'sc_sustainability', role: 'Scope 3 freight carbon accounting' },
              { name: 'DigitalTwinAgent', id: 'sc_digital_twin', role: 'Cyber-physical network state synchronization' },
              { name: 'OptimizationAgent', id: 'sc_optimization', role: 'Mathematical mixed-integer solver' }
            ].map((ag) => (
              <div key={ag.id} className="p-3 bg-slate-900 border border-slate-800 rounded-lg space-y-1">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-xs text-blue-300">{ag.name}</span>
                  <span className="text-[10px] bg-emerald-500/10 text-emerald-400 px-1.5 py-0.5 rounded">ACTIVE</span>
                </div>
                <p className="text-[11px] text-slate-400">{ag.role}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
