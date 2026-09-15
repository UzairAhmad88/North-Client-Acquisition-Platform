"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import {
  Business,
  BusinessCreateInput,
  BusinessDuplicateCheckResponse,
  checkDuplicateBusiness,
  createBusiness,
  listBusinesses,
} from "@/lib/api/businesses";

export default function BusinessesPage() {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination & Filters
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [industryFilter, setIndustryFilter] = useState<string>("");
  const [cityFilter, setCityFilter] = useState<string>("");
  const [sortField, setSortField] = useState("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  // Create Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);
  const [duplicateResult, setDuplicateResult] = useState<BusinessDuplicateCheckResponse | null>(null);

  const [form, setForm] = useState<BusinessCreateInput>({
    name: "",
    legal_name: "",
    description: "",
    business_type: "SERVICE",
    industry: "RETAIL",
    category: "",
    subcategory: "",
    phone: "",
    email: "",
    website_url: "",
    address: "",
    city: "Peshawar",
    state: "KPK",
    country: "Pakistan",
    postal_code: "",
    source: "MANUAL",
  });

  const fetchBusinesses = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await listBusinesses({
        page,
        page_size: pageSize,
        search: search || undefined,
        status: statusFilter || undefined,
        industry: industryFilter || undefined,
        city: cityFilter || undefined,
        sort: sortField,
        order: sortOrder,
      });
      setBusinesses(res.data);
      setTotalPages(res.pagination.total_pages || 1);
      setTotalCount(res.pagination.total || 0);
    } catch (err: any) {
      setError(err.message || "Failed to load business records.");
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, search, statusFilter, industryFilter, cityFilter, sortField, sortOrder]);

  useEffect(() => {
    fetchBusinesses();
  }, [fetchBusinesses]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    fetchBusinesses();
  };

  const handleDuplicateCheck = async () => {
    if (!form.name.trim()) return;
    try {
      const res = await checkDuplicateBusiness(form.name, {
        phone: form.phone || "",
        email: form.email || "",
        website_url: form.website_url || "",
        city: form.city || "",
      });
      setDuplicateResult(res.data);
    } catch (err) {
      // Ignore background check error
    }
  };

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setModalError(null);
    try {
      await createBusiness(form);
      setIsModalOpen(false);
      setForm({
        name: "",
        legal_name: "",
        description: "",
        business_type: "SERVICE",
        industry: "RETAIL",
        category: "",
        subcategory: "",
        phone: "",
        email: "",
        website_url: "",
        address: "",
        city: "Peshawar",
        state: "KPK",
        country: "Pakistan",
        postal_code: "",
        source: "MANUAL",
      });
      setDuplicateResult(null);
      fetchBusinesses();
    } catch (err: any) {
      setModalError(err.message || "Failed to create business.");
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
          <h1 className="text-2xl font-bold text-neutral-900 mt-1">Business CRM</h1>
          <p className="text-sm text-neutral-500 mt-1">
            Canonical organization registry & deduplicated company metadata.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsModalOpen(true)}
            className="inline-flex items-center justify-center px-4 py-2 bg-neutral-900 text-white text-sm font-medium rounded-lg hover:bg-neutral-800 transition shadow-sm"
          >
            + Add Business
          </button>
        </div>
      </div>

      {/* Filters & Search Toolbar */}
      <div className="bg-white p-4 rounded-xl border border-neutral-200 shadow-sm space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search by business name, email, phone, website, or city..."
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
              <option value="ACTIVE">Active</option>
              <option value="INACTIVE">Inactive</option>
              <option value="ARCHIVED">Archived</option>
            </select>

            <select
              value={sortField}
              onChange={(e) => setSortField(e.target.value)}
              className="px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
            >
              <option value="created_at">Date Created</option>
              <option value="name">Business Name</option>
              <option value="city">City</option>
              <option value="status">Status</option>
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

      {/* Content Area */}
      {loading ? (
        <div className="p-12 text-center text-neutral-500 text-sm bg-white rounded-xl border border-neutral-200">
          Loading business records...
        </div>
      ) : error ? (
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm space-y-3">
          <p className="font-semibold">{error}</p>
          <button
            onClick={() => fetchBusinesses()}
            className="px-3 py-1.5 bg-red-600 text-white rounded-md text-xs font-medium hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      ) : businesses.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-xl border border-neutral-200 space-y-3">
          <div className="w-12 h-12 rounded-full bg-neutral-100 text-neutral-400 flex items-center justify-center mx-auto text-xl font-bold">
            🏢
          </div>
          <h3 className="text-base font-semibold text-neutral-900">No businesses found</h3>
          <p className="text-sm text-neutral-500 max-w-md mx-auto">
            {search || statusFilter
              ? "No businesses matched your current filter criteria. Try resetting your search."
              : "Get started by adding your first organization record to the platform."}
          </p>
          <button
            onClick={() => setIsModalOpen(true)}
            className="inline-flex items-center px-4 py-2 bg-neutral-900 text-white text-sm font-medium rounded-lg hover:bg-neutral-800 transition"
          >
            + Create Business
          </button>
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-neutral-200 overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm border-collapse">
              <thead>
                <tr className="bg-neutral-50 border-b border-neutral-200 text-neutral-600 font-semibold text-xs uppercase tracking-wider">
                  <th className="py-3 px-4">Organization</th>
                  <th className="py-3 px-4">Industry / Type</th>
                  <th className="py-3 px-4">Location</th>
                  <th className="py-3 px-4">Contact</th>
                  <th className="py-3 px-4">Data Quality</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-neutral-200">
                {businesses.map((biz) => (
                  <tr key={biz.id} className="hover:bg-neutral-50 transition">
                    <td className="py-3.5 px-4">
                      <Link
                        href={`/businesses/${biz.id}`}
                        className="font-semibold text-neutral-900 hover:text-blue-600 transition"
                      >
                        {biz.name}
                      </Link>
                      {biz.legal_name && (
                        <div className="text-xs text-neutral-400">{biz.legal_name}</div>
                      )}
                    </td>
                    <td className="py-3.5 px-4 text-neutral-600">
                      <span className="inline-block px-2 py-0.5 text-xs font-medium bg-neutral-100 rounded border border-neutral-200 mr-1">
                        {biz.industry}
                      </span>
                      <span className="text-xs text-neutral-400">{biz.business_type}</span>
                    </td>
                    <td className="py-3.5 px-4 text-neutral-600 text-xs">
                      {biz.city || "—"}{biz.country ? `, ${biz.country}` : ""}
                    </td>
                    <td className="py-3.5 px-4 text-xs text-neutral-600 space-y-0.5">
                      {biz.phone && <div>📞 {biz.phone}</div>}
                      {biz.email && <div>✉️ {biz.email}</div>}
                      {biz.website_url && (
                        <div>
                          🌐{" "}
                          <a
                            href={
                              biz.website_url.startsWith("http")
                                ? biz.website_url
                                : `https://${biz.website_url}`
                            }
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline"
                          >
                            {biz.website_url.replace(/^https?:\/\//, "")}
                          </a>
                        </div>
                      )}
                    </td>
                    <td className="py-3.5 px-4">
                      {biz.data_quality ? (
                        <div className="w-28 space-y-1">
                          <div className="flex justify-between text-xs font-medium text-neutral-600">
                            <span>{biz.data_quality.score}%</span>
                          </div>
                          <div className="w-full bg-neutral-200 h-1.5 rounded-full overflow-hidden">
                            <div
                              className={`h-1.5 rounded-full ${
                                biz.data_quality.score >= 80
                                  ? "bg-emerald-500"
                                  : biz.data_quality.score >= 50
                                  ? "bg-amber-500"
                                  : "bg-red-500"
                              }`}
                              style={{ width: `${biz.data_quality.score}%` }}
                            />
                          </div>
                        </div>
                      ) : (
                        <span className="text-xs text-neutral-400">—</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                          biz.status === "ACTIVE"
                            ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                            : biz.status === "INACTIVE"
                            ? "bg-amber-50 text-amber-700 border-amber-200"
                            : "bg-neutral-100 text-neutral-600 border-neutral-200"
                        }`}
                      >
                        {biz.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        href={`/businesses/${biz.id}`}
                        className="inline-block text-xs font-medium text-neutral-700 hover:text-neutral-900 border border-neutral-300 rounded px-2.5 py-1 hover:bg-neutral-100 transition"
                      >
                        View Profile
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination Footer */}
          <div className="px-4 py-3 bg-neutral-50 border-t border-neutral-200 flex items-center justify-between text-xs text-neutral-600">
            <div>
              Showing <span className="font-semibold">{businesses.length}</span> of{" "}
              <span className="font-semibold">{totalCount}</span> businesses
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

      {/* Create Business Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-neutral-200 pb-3">
              <h3 className="text-lg font-bold text-neutral-900">Add New Business</h3>
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
                <div className="font-bold flex items-center gap-1">
                  ⚠️ Possible Duplicate Detected ({Math.round(duplicateResult.confidence * 100)}% match)
                </div>
                <p>Candidate records with similar signals exist:</p>
                <ul className="list-disc pl-4 space-y-0.5">
                  {duplicateResult.matches.map((m) => (
                    <li key={m.business_id}>
                      <span className="font-semibold">{m.name}</span> ({m.signals.join(", ")})
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <form onSubmit={handleCreateSubmit} className="space-y-4 text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Business Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={form.name}
                    onBlur={handleDuplicateCheck}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    placeholder="e.g. Iron Gym & Fitness"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Legal Name
                  </label>
                  <input
                    type="text"
                    value={form.legal_name || ""}
                    onChange={(e) => setForm({ ...form, legal_name: e.target.value })}
                    placeholder="e.g. Iron Fitness Pvt Ltd"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Industry</label>
                  <input
                    type="text"
                    value={form.industry || ""}
                    onChange={(e) => setForm({ ...form, industry: e.target.value })}
                    placeholder="e.g. GYM, RESTAURANT, CLINIC"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Phone</label>
                  <input
                    type="text"
                    value={form.phone || ""}
                    onBlur={handleDuplicateCheck}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    placeholder="+92 300 1234567"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={form.email || ""}
                    onBlur={handleDuplicateCheck}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    placeholder="info@irongym.pk"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Website URL
                  </label>
                  <input
                    type="text"
                    value={form.website_url || ""}
                    onBlur={handleDuplicateCheck}
                    onChange={(e) => setForm({ ...form, website_url: e.target.value })}
                    placeholder="https://irongym.pk"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">City</label>
                  <input
                    type="text"
                    value={form.city || ""}
                    onChange={(e) => setForm({ ...form, city: e.target.value })}
                    placeholder="Peshawar"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Country</label>
                  <input
                    type="text"
                    value={form.country || ""}
                    onChange={(e) => setForm({ ...form, country: e.target.value })}
                    placeholder="Pakistan"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">Address</label>
                  <input
                    type="text"
                    value={form.address || ""}
                    onChange={(e) => setForm({ ...form, address: e.target.value })}
                    placeholder="University Road, Peshawar"
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
                  {submitting ? "Saving..." : "Save Business"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}
