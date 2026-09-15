"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { Business, listBusinesses } from "@/lib/api/businesses";
import {
  checkDuplicateLead,
  createLead,
  Lead,
  LeadCreateInput,
  LeadDuplicateCheckResponse,
  listLeads,
} from "@/lib/api/leads";

export default function LeadsPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination & Filters
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [priorityFilter, setPriorityFilter] = useState<string>("");
  const [qualificationFilter, setQualificationFilter] = useState<string>("");
  const [sortField, setSortField] = useState("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  // Create Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);
  const [duplicateResult, setDuplicateResult] = useState<LeadDuplicateCheckResponse | null>(null);

  // Business Selector in Modal
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [businessSearch, setBusinessSearch] = useState("");

  const [form, setForm] = useState<LeadCreateInput>({
    business_id: "",
    title: "",
    description: "",
    source: "MANUAL",
    source_detail: "",
    priority: "MEDIUM",
    qualification_status: "UNQUALIFIED",
    contactability_status: "UNKNOWN",
    estimated_value: undefined,
    currency: "USD",
    next_action: "",
    next_action_at: "",
    notes: "",
  });

  const fetchLeads = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await listLeads({
        page,
        page_size: pageSize,
        search: search || undefined,
        status: statusFilter || undefined,
        priority: priorityFilter || undefined,
        qualification_status: qualificationFilter || undefined,
        sort: sortField,
        order: sortOrder,
      });
      setLeads(res.data);
      setTotalPages(res.pagination.total_pages || 1);
      setTotalCount(res.pagination.total || 0);
    } catch (err: any) {
      setError(err.message || "Failed to load lead opportunities.");
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, search, statusFilter, priorityFilter, qualificationFilter, sortField, sortOrder]);

  useEffect(() => {
    fetchLeads();
  }, [fetchLeads]);

  // Load business list for modal dropdown
  const loadBusinesses = useCallback(async (query = "") => {
    try {
      const res = await listBusinesses({ page: 1, page_size: 50, search: query || undefined, status: "ACTIVE" });
      setBusinesses(res.data);
    } catch (err) {
      // Ignore
    }
  }, []);

  useEffect(() => {
    if (isModalOpen) {
      loadBusinesses();
    }
  }, [isModalOpen, loadBusinesses]);

  const handleDuplicateCheck = async () => {
    if (!form.business_id || !form.title.trim()) return;
    try {
      const res = await checkDuplicateLead(form.business_id, form.title);
      setDuplicateResult(res.data);
    } catch (err) {
      // Ignore
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    fetchLeads();
  };

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.business_id) {
      setModalError("Please select a target business organization.");
      return;
    }
    setSubmitting(true);
    setModalError(null);
    try {
      await createLead(form);
      setIsModalOpen(false);
      setForm({
        business_id: "",
        title: "",
        description: "",
        source: "MANUAL",
        source_detail: "",
        priority: "MEDIUM",
        qualification_status: "UNQUALIFIED",
        contactability_status: "UNKNOWN",
        estimated_value: undefined,
        currency: "USD",
        next_action: "",
        next_action_at: "",
        notes: "",
      });
      setDuplicateResult(null);
      fetchLeads();
    } catch (err: any) {
      setModalError(err.message || "Failed to create lead opportunity.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-neutral-200 pb-5">
        <div>
          <div className="flex items-center space-x-3">
            <Link
              href="/dashboard"
              className="text-xs font-semibold text-neutral-500 hover:text-neutral-900 transition"
            >
              ← Back to Dashboard
            </Link>
          </div>
          <h1 className="text-2xl font-bold text-neutral-900 mt-1">Lead CRM</h1>
          <p className="text-sm text-neutral-500 mt-1">
            Sales opportunity tracking & qualification pipeline.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsModalOpen(true)}
            className="inline-flex items-center justify-center px-4 py-2 bg-neutral-900 text-white text-sm font-medium rounded-lg hover:bg-neutral-800 transition shadow-sm"
          >
            + Add Lead
          </button>
        </div>
      </div>

      {/* Toolbar */}
      <div className="bg-white p-4 rounded-xl border border-neutral-200 shadow-sm space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search by opportunity title, business name, or description..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
            />
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <select
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setPage(1);
              }}
              className="px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
            >
              <option value="">All Statuses</option>
              <option value="NEW">NEW</option>
              <option value="RESEARCHING">RESEARCHING</option>
              <option value="QUALIFIED">QUALIFIED</option>
              <option value="CONTACTED">CONTACTED</option>
              <option value="RESPONDED">RESPONDED</option>
              <option value="INTERESTED">INTERESTED</option>
              <option value="MEETING">MEETING</option>
              <option value="PROPOSAL">PROPOSAL</option>
              <option value="WON">WON</option>
              <option value="FOLLOW_UP">FOLLOW_UP</option>
              <option value="LOST">LOST</option>
              <option value="ARCHIVED">ARCHIVED</option>
            </select>

            <select
              value={priorityFilter}
              onChange={(e) => {
                setPriorityFilter(e.target.value);
                setPage(1);
              }}
              className="px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
            >
              <option value="">All Priorities</option>
              <option value="LOW">LOW</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HIGH">HIGH</option>
              <option value="URGENT">URGENT</option>
            </select>

            <select
              value={sortField}
              onChange={(e) => setSortField(e.target.value)}
              className="px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
            >
              <option value="created_at">Date Created</option>
              <option value="title">Title</option>
              <option value="priority">Priority</option>
              <option value="estimated_value">Value</option>
            </select>

            <button
              type="button"
              onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
              className="px-3 py-2 text-sm border border-neutral-300 rounded-lg hover:bg-neutral-50 font-medium"
            >
              {sortOrder.toUpperCase()}
            </button>

            <button
              type="submit"
              className="px-4 py-2 bg-neutral-100 hover:bg-neutral-200 text-neutral-800 text-sm font-medium rounded-lg transition"
            >
              Search
            </button>
          </div>
        </form>
      </div>

      {/* Content */}
      {loading ? (
        <div className="p-12 text-center text-neutral-500 text-sm bg-white rounded-xl border border-neutral-200">
          Loading lead opportunities...
        </div>
      ) : error ? (
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm space-y-3">
          <p className="font-semibold">{error}</p>
          <button
            onClick={() => fetchLeads()}
            className="px-3 py-1.5 bg-red-600 text-white rounded-md text-xs font-medium hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      ) : leads.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-xl border border-neutral-200 space-y-3">
          <div className="w-12 h-12 rounded-full bg-neutral-100 text-neutral-400 flex items-center justify-center mx-auto text-xl font-bold">
            🎯
          </div>
          <h3 className="text-base font-semibold text-neutral-900">No sales leads found</h3>
          <p className="text-sm text-neutral-500 max-w-md mx-auto">
            {search || statusFilter || priorityFilter
              ? "No lead opportunities matched your current filter criteria."
              : "Create your first sales lead to begin tracking client acquisition opportunities."}
          </p>
          <button
            onClick={() => setIsModalOpen(true)}
            className="inline-flex items-center px-4 py-2 bg-neutral-900 text-white text-sm font-medium rounded-lg hover:bg-neutral-800 transition"
          >
            + Create Lead
          </button>
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-neutral-200 overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm border-collapse">
              <thead>
                <tr className="bg-neutral-50 border-b border-neutral-200 text-neutral-600 font-semibold text-xs uppercase tracking-wider">
                  <th className="py-3 px-4">Opportunity</th>
                  <th className="py-3 px-4">Business</th>
                  <th className="py-3 px-4">Priority</th>
                  <th className="py-3 px-4">Est. Value</th>
                  <th className="py-3 px-4">Next Action</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-200">
                {leads.map((lead) => (
                  <tr key={lead.id} className="hover:bg-neutral-50 transition">
                    <td className="py-3.5 px-4">
                      <Link
                        href={`/leads/${lead.id}`}
                        className="font-semibold text-neutral-900 hover:text-blue-600 transition"
                      >
                        {lead.title}
                      </Link>
                      {lead.qualification_status && (
                        <div className="text-[11px] text-neutral-400">
                          Qual: {lead.qualification_status}
                        </div>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-xs">
                      {lead.business ? (
                        <Link
                          href={`/businesses/${lead.business.id}`}
                          className="font-medium text-neutral-800 hover:underline"
                        >
                          🏢 {lead.business.name}
                        </Link>
                      ) : (
                        <span className="text-neutral-400">—</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold ${
                          lead.priority === "URGENT"
                            ? "bg-red-100 text-red-800"
                            : lead.priority === "HIGH"
                            ? "bg-amber-100 text-amber-800"
                            : lead.priority === "MEDIUM"
                            ? "bg-blue-100 text-blue-800"
                            : "bg-neutral-100 text-neutral-600"
                        }`}
                      >
                        {lead.priority}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-xs font-medium text-neutral-700">
                      {lead.estimated_value
                        ? `${lead.currency} ${lead.estimated_value.toLocaleString()}`
                        : "—"}
                    </td>
                    <td className="py-3.5 px-4 text-xs text-neutral-600 max-w-xs truncate">
                      {lead.next_action || "—"}
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                          lead.status === "WON"
                            ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                            : lead.status === "LOST"
                            ? "bg-red-50 text-red-700 border-red-200"
                            : lead.status === "QUALIFIED"
                            ? "bg-blue-50 text-blue-700 border-blue-200"
                            : lead.status === "CONTACTED"
                            ? "bg-indigo-50 text-indigo-700 border-indigo-200"
                            : "bg-neutral-100 text-neutral-700 border-neutral-200"
                        }`}
                      >
                        {lead.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        href={`/leads/${lead.id}`}
                        className="inline-block text-xs font-medium text-neutral-700 hover:text-neutral-900 border border-neutral-300 rounded px-2.5 py-1 hover:bg-neutral-100 transition"
                      >
                        View Detail
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="px-4 py-3 bg-neutral-50 border-t border-neutral-200 flex items-center justify-between text-xs text-neutral-600">
            <div>
              Showing <span className="font-semibold">{leads.length}</span> of{" "}
              <span className="font-semibold">{totalCount}</span> leads
            </div>
            <div className="flex items-center space-x-2">
              <button
                disabled={page <= 1}
                onClick={() => setPage(page - 1)}
                className="px-3 py-1 bg-white border border-neutral-300 rounded hover:bg-neutral-100 disabled:opacity-50 font-medium"
              >
                Previous
              </button>
              <span>
                Page {page} of {totalPages}
              </span>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage(page + 1)}
                className="px-3 py-1 bg-white border border-neutral-300 rounded hover:bg-neutral-100 disabled:opacity-50 font-medium"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Create Lead Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-neutral-200 pb-3">
              <h3 className="text-lg font-bold text-neutral-900">Add New Lead Opportunity</h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-neutral-400 hover:text-neutral-700 font-bold"
              >
                ✕
              </button>
            </div>

            {modalError && (
              <div className="p-3 bg-red-50 text-red-700 border border-red-200 rounded-lg text-xs font-medium">
                {modalError}
              </div>
            )}

            {duplicateResult?.possible_duplicate && (
              <div className="p-3 bg-amber-50 border border-amber-300 rounded-lg text-xs text-amber-900 space-y-1">
                <div className="font-bold">
                  ⚠️ Possible Duplicate Lead Detected ({Math.round(duplicateResult.confidence * 100)}% match)
                </div>
                <p>Existing opportunities for this business:</p>
                <ul className="list-disc pl-4 space-y-0.5">
                  {duplicateResult.matches.map((m) => (
                    <li key={m.lead_id}>
                      <span className="font-semibold">{m.title}</span> ({m.status})
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <form onSubmit={handleCreateSubmit} className="space-y-4 text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Select Target Business *
                  </label>
                  <select
                    required
                    value={form.business_id}
                    onChange={(e) => {
                      setForm({ ...form, business_id: e.target.value });
                    }}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  >
                    <option value="">-- Choose an Organization --</option>
                    {businesses.map((b) => (
                      <option key={b.id} value={b.id}>
                        {b.name} ({b.city || "No City"} - {b.industry})
                      </option>
                    ))}
                  </select>
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Opportunity Title *
                  </label>
                  <input
                    type="text"
                    required
                    value={form.title}
                    onBlur={handleDuplicateCheck}
                    onChange={(e) => setForm({ ...form, title: e.target.value })}
                    placeholder="e.g. Website Redesign & Lead Gen System"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Priority</label>
                  <select
                    value={form.priority}
                    onChange={(e) =>
                      setForm({ ...form, priority: e.target.value as any })
                    }
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  >
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                    <option value="URGENT">URGENT</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Source</label>
                  <input
                    type="text"
                    value={form.source || "MANUAL"}
                    onChange={(e) => setForm({ ...form, source: e.target.value })}
                    placeholder="MANUAL, DISCOVERY, REFERRAL"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Est. Value</label>
                  <input
                    type="number"
                    value={form.estimated_value || ""}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        estimated_value: e.target.value ? parseFloat(e.target.value) : undefined,
                      })
                    }
                    placeholder="2500"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Currency</label>
                  <input
                    type="text"
                    value={form.currency || "USD"}
                    onChange={(e) => setForm({ ...form, currency: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Next Planned Action
                  </label>
                  <input
                    type="text"
                    value={form.next_action || ""}
                    onChange={(e) => setForm({ ...form, next_action: e.target.value })}
                    placeholder="e.g. Audit website and prepare initial review"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">Description</label>
                  <textarea
                    rows={3}
                    value={form.description || ""}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    placeholder="Provide details about the opportunity..."
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-3 border-t border-neutral-200">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 border border-neutral-300 rounded-lg font-medium text-neutral-700 hover:bg-neutral-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 bg-neutral-900 text-white rounded-lg font-medium hover:bg-neutral-800 disabled:opacity-50"
                >
                  {submitting ? "Saving..." : "Save Lead"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}
