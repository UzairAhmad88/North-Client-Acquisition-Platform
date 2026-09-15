"use client";

import React, { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import {
  createService,
  listServices,
  Service,
  ServiceCreateInput,
} from "@/lib/api/services";

export default function ServiceCatalogPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination & Filters
  const [page, setPage] = useState(1);
  const [pageSize] = useState(12);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<string>("");
  const [statusFilter, setStatusFilter] = useState<string>("ACTIVE");
  const [pricingFilter, setPricingFilter] = useState<string>("");
  const [sortField, setSortField] = useState("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  // Create Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [modalError, setModalError] = useState<string | null>(null);

  const [form, setForm] = useState<ServiceCreateInput>({
    name: "",
    slug: "",
    short_description: "",
    description: "",
    category: "WEB_DEVELOPMENT",
    subcategory: "",
    status: "ACTIVE",
    delivery_model: "FIXED_PROJECT",
    pricing_model: "CUSTOM",
    base_price: undefined,
    price_min: undefined,
    price_max: undefined,
    currency: "USD",
    estimated_duration_days: undefined,
    is_featured: false,
    is_active: true,
  });

  const fetchServices = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await listServices({
        page,
        page_size: pageSize,
        search: search || undefined,
        category: categoryFilter || undefined,
        status: statusFilter || undefined,
        pricing_model: pricingFilter || undefined,
        sort: sortField,
        order: sortOrder,
      });
      setServices(res.data);
      setTotalPages(res.pagination.total_pages || 1);
      setTotalCount(res.pagination.total || 0);
    } catch (err: any) {
      setError(err.message || "Failed to load service catalog.");
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, search, categoryFilter, statusFilter, pricingFilter, sortField, sortOrder]);

  useEffect(() => {
    fetchServices();
  }, [fetchServices]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    fetchServices();
  };

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setModalError(null);
    try {
      await createService(form);
      setIsModalOpen(false);
      setForm({
        name: "",
        slug: "",
        short_description: "",
        description: "",
        category: "WEB_DEVELOPMENT",
        subcategory: "",
        status: "ACTIVE",
        delivery_model: "FIXED_PROJECT",
        pricing_model: "CUSTOM",
        base_price: undefined,
        price_min: undefined,
        price_max: undefined,
        currency: "USD",
        estimated_duration_days: undefined,
        is_featured: false,
        is_active: true,
      });
      fetchServices();
    } catch (err: any) {
      setModalError(err.message || "Failed to create catalog service.");
    } finally {
      setSubmitting(false);
    }
  };

  const categories = [
    { label: "All Categories", value: "" },
    { label: "Web Development", value: "WEB_DEVELOPMENT" },
    { label: "Software Systems", value: "SOFTWARE_DEVELOPMENT" },
    { label: "Business Automation", value: "BUSINESS_AUTOMATION" },
    { label: "AI Systems", value: "AI_SYSTEMS" },
    { label: "Data Analytics", value: "DATA_ANALYTICS" },
  ];

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
          <h1 className="text-2xl font-bold text-neutral-900 mt-1">Service Catalog</h1>
          <p className="text-sm text-neutral-500 mt-1">
            Structured solutions, software systems, and AI assistants offered by North&apos;s.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsModalOpen(true)}
            className="inline-flex items-center justify-center px-4 py-2 bg-neutral-900 text-white text-sm font-medium rounded-lg hover:bg-neutral-800 transition shadow-sm"
          >
            + Add Service
          </button>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex items-center space-x-2 border-b border-neutral-200 overflow-x-auto pb-1 text-xs font-medium text-neutral-600">
        {categories.map((cat) => (
          <button
            key={cat.value}
            onClick={() => {
              setCategoryFilter(cat.value);
              setPage(1);
            }}
            className={`px-3 py-2 border-b-2 font-semibold whitespace-nowrap transition ${
              categoryFilter === cat.value
                ? "border-neutral-900 text-neutral-900"
                : "border-transparent text-neutral-500 hover:text-neutral-900"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Toolbar */}
      <div className="bg-white p-4 rounded-xl border border-neutral-200 shadow-sm space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search services by title, slug, features, or description..."
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
              <option value="DRAFT">Draft</option>
              <option value="PAUSED">Paused</option>
              <option value="ARCHIVED">Archived</option>
            </select>

            <select
              value={pricingFilter}
              onChange={(e) => {
                setPricingFilter(e.target.value);
                setPage(1);
              }}
              className="px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
            >
              <option value="">All Pricing Models</option>
              <option value="CUSTOM">Custom Quote</option>
              <option value="STARTING_AT">Starting At</option>
              <option value="FIXED">Fixed Price</option>
              <option value="RANGE">Price Range</option>
            </select>

            <button
              type="submit"
              className="px-4 py-2 bg-neutral-100 hover:bg-neutral-200 text-neutral-800 text-sm font-medium rounded-lg transition"
            >
              Search
            </button>
          </div>
        </form>
      </div>

      {/* Content Grid */}
      {loading ? (
        <div className="p-12 text-center text-neutral-500 text-sm bg-white rounded-xl border border-neutral-200">
          Loading service catalog...
        </div>
      ) : error ? (
        <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm space-y-3">
          <p className="font-semibold">{error}</p>
          <button
            onClick={() => fetchServices()}
            className="px-3 py-1.5 bg-red-600 text-white rounded-md text-xs font-medium hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      ) : services.length === 0 ? (
        <div className="p-12 text-center bg-white rounded-xl border border-neutral-200 space-y-3">
          <div className="w-12 h-12 rounded-full bg-neutral-100 text-neutral-400 flex items-center justify-center mx-auto text-xl font-bold">
            ⚡
          </div>
          <h3 className="text-base font-semibold text-neutral-900">No services found</h3>
          <p className="text-sm text-neutral-500 max-w-md mx-auto">
            {search || categoryFilter
              ? "No catalog services matched your query. Try clearing your filters."
              : "Create your first solution in the Service Catalog."}
          </p>
          <button
            onClick={() => setIsModalOpen(true)}
            className="inline-flex items-center px-4 py-2 bg-neutral-900 text-white text-sm font-medium rounded-lg hover:bg-neutral-800 transition"
          >
            + Add Service
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((srv) => (
              <div
                key={srv.id}
                className="bg-white p-6 rounded-xl border border-neutral-200 shadow-sm flex flex-col justify-between hover:shadow-md transition space-y-4"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span
                      className={`inline-block px-2 py-0.5 text-[10px] font-bold tracking-wider rounded uppercase ${
                        srv.category === "WEB_DEVELOPMENT"
                          ? "bg-indigo-100 text-indigo-800"
                          : srv.category === "SOFTWARE_DEVELOPMENT"
                          ? "bg-blue-100 text-blue-800"
                          : srv.category === "BUSINESS_AUTOMATION"
                          ? "bg-amber-100 text-amber-800"
                          : srv.category === "AI_SYSTEMS"
                          ? "bg-purple-100 text-purple-800"
                          : "bg-neutral-100 text-neutral-700"
                      }`}
                    >
                      {srv.category.replace("_", " ")}
                    </span>
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${
                        srv.status === "ACTIVE"
                          ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                          : "bg-neutral-100 text-neutral-600 border-neutral-200"
                      }`}
                    >
                      {srv.status}
                    </span>
                  </div>

                  <Link href={`/services/${srv.id}`} className="block group">
                    <h3 className="text-lg font-bold text-neutral-900 group-hover:text-blue-600 transition">
                      {srv.name}
                    </h3>
                  </Link>
                  <p className="text-xs text-neutral-400 font-mono">slug: {srv.slug}</p>

                  <p className="text-xs text-neutral-600 leading-relaxed line-clamp-3">
                    {srv.short_description || srv.description || "No short description provided."}
                  </p>
                </div>

                <div className="pt-3 border-t border-neutral-100 space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <div>
                      <span className="text-neutral-400 block text-[10px] font-medium">PRICING</span>
                      <span className="font-bold text-neutral-900">
                        {srv.pricing_model === "CUSTOM"
                          ? "Custom Quote"
                          : srv.base_price
                          ? `${srv.currency} ${srv.base_price.toLocaleString()}`
                          : "Contact for Quote"}
                      </span>
                    </div>

                    <div className="text-right">
                      <span className="text-neutral-400 block text-[10px] font-medium">ESTIMATED DURATION</span>
                      <span className="font-semibold text-neutral-700">
                        {srv.estimated_duration_days
                          ? `${srv.estimated_duration_days} days`
                          : "Flexible"}
                      </span>
                    </div>
                  </div>

                  <Link
                    href={`/services/${srv.id}`}
                    className="block w-full text-center text-xs font-semibold py-2 px-3 border border-neutral-300 rounded-lg hover:bg-neutral-100 text-neutral-800 transition"
                  >
                    View Details →
                  </Link>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination Footer */}
          <div className="px-4 py-3 bg-neutral-50 border border-neutral-200 rounded-xl flex items-center justify-between text-xs text-neutral-600">
            <div>
              Showing <span className="font-semibold">{services.length}</span> of{" "}
              <span className="font-semibold">{totalCount}</span> catalog services
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

      {/* Create Service Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl border border-neutral-200 max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-neutral-200 pb-3">
              <h3 className="text-lg font-bold text-neutral-900">Add New Service</h3>
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

            <form onSubmit={handleCreateSubmit} className="space-y-4 text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">
                    Service Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    placeholder="e.g. AI Customer Support Assistant"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Category *</label>
                  <select
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value as any })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  >
                    <option value="WEB_DEVELOPMENT">WEB_DEVELOPMENT</option>
                    <option value="SOFTWARE_DEVELOPMENT">SOFTWARE_DEVELOPMENT</option>
                    <option value="BUSINESS_AUTOMATION">BUSINESS_AUTOMATION</option>
                    <option value="AI_SYSTEMS">AI_SYSTEMS</option>
                    <option value="DATA_ANALYTICS">DATA_ANALYTICS</option>
                    <option value="UI_UX">UI_UX</option>
                    <option value="MAINTENANCE">MAINTENANCE</option>
                    <option value="CONSULTING">CONSULTING</option>
                    <option value="OTHER">OTHER</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Delivery Model</label>
                  <select
                    value={form.delivery_model}
                    onChange={(e) => setForm({ ...form, delivery_model: e.target.value as any })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  >
                    <option value="FIXED_PROJECT">FIXED_PROJECT</option>
                    <option value="CUSTOM_QUOTE">CUSTOM_QUOTE</option>
                    <option value="SUBSCRIPTION">SUBSCRIPTION</option>
                    <option value="RETAINER">RETAINER</option>
                    <option value="HOURLY">HOURLY</option>
                    <option value="CONSULTATION">CONSULTATION</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Pricing Model</label>
                  <select
                    value={form.pricing_model}
                    onChange={(e) => setForm({ ...form, pricing_model: e.target.value as any })}
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  >
                    <option value="CUSTOM">CUSTOM</option>
                    <option value="STARTING_AT">STARTING_AT</option>
                    <option value="FIXED">FIXED</option>
                    <option value="RANGE">RANGE</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Base Price</label>
                  <input
                    type="number"
                    value={form.base_price || ""}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        base_price: e.target.value ? parseFloat(e.target.value) : undefined,
                      })
                    }
                    placeholder="1500"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-neutral-700 mb-1">Est. Days</label>
                  <input
                    type="number"
                    value={form.estimated_duration_days || ""}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        estimated_duration_days: e.target.value ? parseInt(e.target.value, 10) : undefined,
                      })
                    }
                    placeholder="14"
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
                  <label className="block font-semibold text-neutral-700 mb-1">Short Description</label>
                  <input
                    type="text"
                    value={form.short_description || ""}
                    onChange={(e) => setForm({ ...form, short_description: e.target.value })}
                    placeholder="Summary for cards and quick service overview"
                    className="w-full px-3 py-2 text-sm border border-neutral-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                </div>

                <div className="sm:col-span-2">
                  <label className="block font-semibold text-neutral-700 mb-1">Full Description</label>
                  <textarea
                    rows={3}
                    value={form.description || ""}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    placeholder="Detailed explanation of the solution..."
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
                  {submitting ? "Saving..." : "Save Service"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}
