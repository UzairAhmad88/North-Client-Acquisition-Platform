import { api } from './client';

export interface BillingProfile {
  id: string;
  tenant_id: string;
  client_id: string;
  legal_name: string;
  tax_id?: string;
  billing_email: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country: string;
  default_currency: string;
  payment_terms: string;
  created_at: string;
  updated_at: string;
}

export interface TaxProfile {
  id: string;
  tenant_id: string;
  name: string;
  tax_type: string;
  rate_pct: string;
  country: string;
  state?: string;
  is_compound: boolean;
  is_active: boolean;
  created_at: string;
}

export interface Currency {
  id: string;
  code: string;
  name: string;
  symbol: string;
  decimal_places: number;
  is_active: boolean;
  created_at: string;
}

export interface InvoiceItem {
  id?: string;
  invoice_id?: string;
  title: string;
  description?: string;
  quantity: string;
  unit_price: string;
  subtotal?: string;
  discount_amount?: string;
  taxable_amount?: string;
  tax_amount?: string;
  total_amount?: string;
  item_type?: string;
  reference_type?: string;
  reference_id?: string;
  contract_id?: string;
}

export interface Invoice {
  id: string;
  tenant_id: string;
  client_id: string;
  billing_profile_id?: string;
  project_id?: string;
  contract_id?: string;
  proposal_id?: string;
  invoice_number: string;
  version: number;
  status: string;
  currency: string;
  payment_terms: string;
  custom_terms_days?: number;
  issue_date?: string;
  due_date?: string;
  subtotal: string;
  discount_amount: string;
  taxable_amount: string;
  tax_amount: string;
  total_amount: string;
  amount_paid: string;
  balance_due: string;
  tax_rate_pct: string;
  tax_type: string;
  tax_region?: string;
  discount_rate_pct: string;
  fixed_discount_amount: string;
  notes?: string;
  terms_and_conditions?: string;
  created_by_user_id?: string;
  issued_by_user_id?: string;
  approved_by_user_id?: string;
  created_at: string;
  updated_at: string;
  items?: InvoiceItem[];
}

export interface Payment {
  id: string;
  tenant_id: string;
  invoice_id?: string;
  client_id: string;
  provider_type: string;
  provider_payment_id?: string;
  amount: string;
  currency: string;
  status: string;
  payment_method: string;
  fee_amount: string;
  error_code?: string;
  error_message?: string;
  created_by_user_id?: string;
  created_at: string;
}

export interface ProjectProfitabilityAnalysis {
  project_id: string;
  financial_summary: {
    contracted_revenue: string;
    invoiced_revenue: string;
    collected_revenue: string;
    unbilled_contract_balance: string;
    outstanding_receivables: string;
  };
  cost_breakdown?: {
    estimated_cost: string;
    actual_total_cost: string;
    labor_hours_logged: string;
    direct_labor_cost: string;
    ai_token_cost: string;
    infrastructure_cost: string;
    subcontractor_cost: string;
    other_expenses: string;
    cost_variance_amount: string;
    cost_variance_pct: string;
  };
  profitability_metrics?: {
    estimated_gross_profit: string;
    estimated_margin_pct: string;
    invoiced_gross_profit: string;
    invoiced_margin_pct: string;
    realized_gross_profit: string;
    realized_margin_pct: string;
  };
  commercial_health?: {
    status: string;
    badge: string;
    is_cost_overrun: boolean;
    is_margin_compressed: boolean;
  };
  agent_insights?: string[];
  calculated_at: string;
}

export interface CashFlowForecast {
  months_ahead: number;
  projected_inflows: {
    outstanding_receivables: string;
    scheduled_billings: string;
    total_expected_inflow: string;
  };
  projected_outflows: {
    monthly_burn_rate: string;
    total_expected_burn: string;
  };
  net_projected_cash_flow: string;
  runway_indicator: string;
  calculated_at: string;
}

export const financeApi = {
  // Invoices
  listInvoices: (params?: { client_id?: string; project_id?: string; status?: string; limit?: number; offset?: number }) =>
    api.get<Invoice[]>('/invoices', { params }),

  getInvoice: (id: string) =>
    api.get<Invoice>(`/invoices/${id}`),

  createInvoice: (data: Partial<Invoice>) =>
    api.post<Invoice>('/invoices', data),

  approveInvoice: (id: string, status: 'approved' | 'rejected', comments?: string) =>
    api.post<Invoice>(`/invoices/${id}/approve`, { status, comments }),

  issueInvoice: (id: string, params?: { ar_account_id?: string; revenue_account_id?: string; tax_account_id?: string }) =>
    api.post<Invoice>(`/invoices/${id}/issue`, null, { params }),

  // Payments
  listPayments: (params?: { invoice_id?: string; client_id?: string }) =>
    api.get<Payment[]>('/payments', { params }),

  chargePayment: (data: {
    invoice_id: string;
    amount: string;
    currency?: string;
    payment_method?: string;
    provider_type?: string;
    customer_id?: string;
    idempotency_key?: string;
  }) =>
    api.post<Payment>('/payments/charge', data),

  processRefund: (data: { payment_id: string; amount: string; currency?: string; reason?: string }) =>
    api.post('/payments/refund', data),

  // Billing & Taxes
  listBillingProfiles: (clientId?: string) =>
    api.get<BillingProfile[]>('/billing/profiles', { params: { client_id: clientId } }),

  createBillingProfile: (data: Partial<BillingProfile>) =>
    api.post<BillingProfile>('/billing/profiles', data),

  listTaxProfiles: () =>
    api.get<TaxProfile[]>('/billing/taxes'),

  listCurrencies: () =>
    api.get<Currency[]>('/billing/currencies'),

  // Intelligence & Ledger
  analyzeProfitability: (data: {
    project_id: string;
    contracted_revenue: string;
    invoiced_revenue: string;
    collected_revenue: string;
    estimated_cost: string;
    labor_hours_logged?: string;
    labor_hourly_cost_rate?: string;
    ai_token_cost?: string;
    infrastructure_cost?: string;
    subcontractor_cost?: string;
    other_expenses?: string;
  }) =>
    api.post<ProjectProfitabilityAnalysis>('/finance/profitability/analyze', data),

  forecastCashFlow: (data: { months_ahead?: number; projected_monthly_burn?: string }) =>
    api.post<CashFlowForecast>('/finance/forecast/cash-flow', data),
};
