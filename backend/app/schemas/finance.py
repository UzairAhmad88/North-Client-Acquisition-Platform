"""Pydantic schemas for Unified Billing, Invoicing, Payments, Financial Operations & Commercial Control."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- Billing Profile ---

class BillingProfileCreate(BaseModel):
    client_id: str
    legal_name: str
    tax_id: Optional[str] = None
    billing_email: str
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "US"
    default_currency: str = "USD"
    payment_terms: str = "net_30"


class BillingProfileResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    legal_name: str
    tax_id: Optional[str] = None
    billing_email: str
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str
    default_currency: str
    payment_terms: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Currency & Tax Profiles ---

class CurrencyCreate(BaseModel):
    code: str
    name: str
    symbol: str = "$"
    decimal_places: int = 2
    is_active: bool = True


class CurrencyResponse(BaseModel):
    id: str
    code: str
    name: str
    symbol: str
    decimal_places: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TaxProfileCreate(BaseModel):
    name: str
    tax_type: str = "sales_tax"
    rate_pct: Decimal = Decimal("0.00")
    country: str
    state: Optional[str] = None
    is_compound: bool = False
    is_active: bool = True


class TaxProfileResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    tax_type: str
    rate_pct: Decimal
    country: str
    state: Optional[str] = None
    is_compound: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- Line Items & Invoices ---

class InvoiceItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    quantity: Decimal = Decimal("1.00")
    unit_price: Decimal = Decimal("0.00")
    item_type: str = "fixed"
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    contract_id: Optional[str] = None


class InvoiceItemResponse(BaseModel):
    id: str
    invoice_id: str
    title: str
    description: Optional[str] = None
    quantity: Decimal
    unit_price: Decimal
    subtotal: Decimal
    discount_amount: Decimal
    taxable_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    item_type: str
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    contract_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceCreate(BaseModel):
    client_id: str
    billing_profile_id: Optional[str] = None
    project_id: Optional[str] = None
    contract_id: Optional[str] = None
    proposal_id: Optional[str] = None
    currency: str = "USD"
    payment_terms: str = "net_30"
    custom_terms_days: Optional[int] = None
    items: List[InvoiceItemCreate] = []
    discount_rate_pct: Decimal = Decimal("0.00")
    fixed_discount_amount: Decimal = Decimal("0.00")
    tax_rate_pct: Decimal = Decimal("0.00")
    tax_type: str = "none"
    tax_region: Optional[str] = None
    notes: Optional[str] = None
    terms_and_conditions: Optional[str] = None


class InvoiceUpdate(BaseModel):
    billing_profile_id: Optional[str] = None
    payment_terms: Optional[str] = None
    custom_terms_days: Optional[int] = None
    items: Optional[List[InvoiceItemCreate]] = None
    discount_rate_pct: Optional[Decimal] = None
    fixed_discount_amount: Optional[Decimal] = None
    tax_rate_pct: Optional[Decimal] = None
    tax_type: Optional[str] = None
    tax_region: Optional[str] = None
    notes: Optional[str] = None
    terms_and_conditions: Optional[str] = None


class InvoiceResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    billing_profile_id: Optional[str] = None
    project_id: Optional[str] = None
    contract_id: Optional[str] = None
    proposal_id: Optional[str] = None
    invoice_number: str
    version: int
    status: str
    currency: str
    payment_terms: str
    custom_terms_days: Optional[int] = None
    issue_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    subtotal: Decimal
    discount_amount: Decimal
    taxable_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    amount_paid: Decimal
    balance_due: Decimal
    tax_rate_pct: Decimal
    tax_type: str
    tax_region: Optional[str] = None
    discount_rate_pct: Decimal
    fixed_discount_amount: Decimal
    notes: Optional[str] = None
    terms_and_conditions: Optional[str] = None
    created_by_user_id: Optional[str] = None
    issued_by_user_id: Optional[str] = None
    approved_by_user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InvoiceDetailResponse(InvoiceResponse):
    items: List[InvoiceItemResponse] = []


class InvoiceApprovalRequest(BaseModel):
    status: str  # approved, rejected
    comments: Optional[str] = None


# --- Payments & Refunds ---

class PaymentChargeRequest(BaseModel):
    invoice_id: str
    amount: Decimal
    currency: str = "USD"
    payment_method: str = "credit_card"
    provider_type: Optional[str] = "mock"
    customer_id: Optional[str] = None
    idempotency_key: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class PaymentResponse(BaseModel):
    id: str
    tenant_id: str
    invoice_id: Optional[str] = None
    client_id: str
    provider_type: str
    provider_payment_id: Optional[str] = None
    amount: Decimal
    currency: str
    status: str
    payment_method: str
    fee_amount: Decimal
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    created_by_user_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RefundProcessRequest(BaseModel):
    payment_id: str
    amount: Decimal
    currency: str = "USD"
    reason: str = "Customer requested refund"
    idempotency_key: Optional[str] = None


class RefundResponse(BaseModel):
    id: str
    tenant_id: str
    payment_id: str
    invoice_id: Optional[str] = None
    provider_refund_id: Optional[str] = None
    amount: Decimal
    currency: str
    status: str
    reason: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Reconciliation ---

class PaymentReconciliationResponse(BaseModel):
    id: str
    tenant_id: str
    payment_id: Optional[str] = None
    provider_event_id: Optional[str] = None
    invoice_id: Optional[str] = None
    status: str
    matched_amount: Decimal
    discrepancy_amount: Decimal
    discrepancy_type: Optional[str] = None
    notes: Optional[str] = None
    resolved_by_user_id: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Credit Note ---

class CreditNoteCreate(BaseModel):
    client_id: str
    invoice_id: Optional[str] = None
    amount: Decimal
    currency: str = "USD"
    reason: Optional[str] = None


class CreditNoteResponse(BaseModel):
    id: str
    tenant_id: str
    client_id: str
    invoice_id: Optional[str] = None
    credit_note_number: str
    amount: Decimal
    currency: str
    balance: Decimal
    reason: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- Financial Accounts & Ledger ---

class FinancialAccountCreate(BaseModel):
    account_code: str
    account_name: str
    account_type: str
    currency: str = "USD"
    is_active: bool = True


class FinancialAccountResponse(BaseModel):
    id: str
    tenant_id: str
    account_code: str
    account_name: str
    account_type: str
    currency: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class JournalItem(BaseModel):
    account_id: str
    account_type: Optional[str] = None
    direction: str  # debit, credit
    amount: Decimal
    description: Optional[str] = None


class JournalEntryRequest(BaseModel):
    description: str
    reference_type: str
    reference_id: str
    currency: str = "USD"
    items: List[JournalItem]


class LedgerEntryResponse(BaseModel):
    id: str
    tenant_id: str
    entry_group_id: str
    account_id: str
    account_type: Optional[str] = None
    direction: str
    amount: Decimal
    currency: str
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    description: Optional[str] = None
    is_reversed: bool
    posted_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# --- Profitability & Forecast ---

class ProjectProfitabilityRequest(BaseModel):
    project_id: str
    contracted_revenue: Decimal
    invoiced_revenue: Decimal
    collected_revenue: Decimal
    estimated_cost: Decimal
    labor_hours_logged: Decimal = Decimal("0.00")
    labor_hourly_cost_rate: Decimal = Decimal("0.00")
    ai_token_cost: Decimal = Decimal("0.00")
    infrastructure_cost: Decimal = Decimal("0.00")
    subcontractor_cost: Decimal = Decimal("0.00")
    other_expenses: Decimal = Decimal("0.00")


class CashFlowForecastRequest(BaseModel):
    months_ahead: int = 3
    projected_monthly_burn: Decimal = Decimal("0.00")
