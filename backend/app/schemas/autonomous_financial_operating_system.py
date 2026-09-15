"""
Phase 72: Autonomous Financial Infrastructure, Treasury, Payments, Capital Intelligence
& Enterprise Financial Operating System Schemas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# 1. Chart of Accounts & Master Data
class FinAccountCreate(BaseModel):
    account_number: str
    account_name: str
    account_type: str = "ASSET"  # ASSET, LIABILITY, EQUITY, REVENUE, COGS, EXPENSE
    sub_category: str = "CURRENT"
    currency: str = "USD"


class FinAccountResponse(BaseModel):
    id: str
    account_number: str
    account_name: str
    account_type: str
    sub_category: str
    currency: str
    current_balance: float
    is_reconcilable: bool


class FinCustomerResponse(BaseModel):
    id: str
    customer_code: str
    company_name: str
    credit_limit_usd: float
    current_ar_balance: float
    payment_terms_days: int
    risk_score: float
    credit_hold: bool


class FinVendorResponse(BaseModel):
    id: str
    vendor_code: str
    company_name: str
    payment_terms_days: int
    beneficiary_verified: bool
    compliance_status: str


# 2. Invoicing, Accounts Receivable & Revenue
class FinInvoiceCreate(BaseModel):
    invoice_number: str
    customer_id: str
    subtotal: float
    tax_amount: float = 0.0
    currency: str = "USD"
    due_date: datetime


class FinInvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    customer_id: str
    subtotal: float
    tax_amount: float
    total_amount: float
    currency: str
    paid_amount: float
    status: str
    issue_date: datetime
    due_date: datetime


class FinArAgingResponse(BaseModel):
    current_bucket_usd: float
    days_1_30_usd: float
    days_31_60_usd: float
    days_61_90_usd: float
    days_90_plus_usd: float
    total_outstanding_usd: float
    dso_days: float


# 3. Accounts Payable & 3-Way Matching
class FinVendorBillResponse(BaseModel):
    id: str
    bill_number: str
    vendor_id: str
    purchase_order_id: Optional[str] = None
    goods_receipt_id: Optional[str] = None
    total_amount: float
    currency: str
    three_way_match_status: str
    status: str
    due_date: datetime


class FinThreeWayMatchResponse(BaseModel):
    bill_id: str
    purchase_order_id: str
    goods_receipt_id: str
    po_amount: float
    received_quantity: float
    billed_amount: float
    variance_amount: float
    is_matched: bool
    requires_approval: bool


# 4. Payment Orchestration & Dual-Control Approvals
class FinPaymentCreate(BaseModel):
    payment_reference: str
    idempotency_key: str
    payment_type: str = "VENDOR_DISBURSEMENT"
    amount: float
    currency: str = "USD"
    source_bank_account_id: str
    destination_entity_or_vendor: str
    requires_dual_approval: bool = False


class FinPaymentResponse(BaseModel):
    id: str
    payment_reference: str
    idempotency_key: str
    payment_type: str
    amount: float
    currency: str
    source_bank_account_id: str
    destination_entity_or_vendor: str
    status: str
    fraud_risk_score: float
    requires_dual_approval: bool


class FinPaymentApprovalRequest(BaseModel):
    payment_id: str
    decision: str = "APPROVED"  # APPROVED or REJECTED
    comments: Optional[str] = None


# 5. Banking & Automated Reconciliation
class FinBankAccountResponse(BaseModel):
    id: str
    account_code: str
    bank_name: str
    account_mask: str
    currency: str
    ledger_balance: float
    available_balance: float
    last_synced_at: datetime


class FinBankTransactionResponse(BaseModel):
    id: str
    bank_account_id: str
    fit_id: str
    transaction_date: datetime
    amount: float
    currency: str
    description: str
    counterparty: str
    reconciliation_status: str


class FinReconciliationResponse(BaseModel):
    id: str
    bank_transaction_id: str
    journal_entry_id: str
    match_confidence: float
    match_type: str
    reconciled_by: str


# 6. Double-Entry General Ledger, Journals & Accounting Periods
class FinJournalCreate(BaseModel):
    journal_code: str
    period_code: str = "2026-09"
    description: str
    source_module: str = "AR"
    debit_account: str
    credit_account: str
    amount: float
    currency: str = "USD"


class FinJournalResponse(BaseModel):
    id: str
    journal_code: str
    entity_id: str
    period_code: str
    entry_date: datetime
    description: str
    source_module: str
    total_debit: float
    total_credit: float
    posting_status: str
    is_balanced: bool


class FinAccountingPeriodResponse(BaseModel):
    id: str
    period_code: str
    fiscal_year: int
    period_number: int
    status: str
    start_date: datetime
    end_date: datetime


# 7. FP&A, Budgets & Cash Forecasting
class FinBudgetResponse(BaseModel):
    id: str
    budget_code: str
    department: str
    fiscal_year: int
    allocated_amount: float
    actual_spent_amount: float
    committed_amount: float
    variance_amount: float
    variance_pct: float


class FinCashForecastResponse(BaseModel):
    forecast_period: str
    opening_cash: float
    projected_inflows: float
    projected_outflows: float
    projected_closing_cash: float
    net_monthly_burn_rate: float
    estimated_runway_months: float


class FinTreasuryPositionResponse(BaseModel):
    total_cash_usd: float
    restricted_cash_usd: float
    total_debt_principal: float
    annual_debt_service: float
    net_liquidity_usd: float
    eur_exposure_usd: float
    jpy_exposure_usd: float


# 8. Fraud Intelligence & Risk Scoring
class FinFraudAlertResponse(BaseModel):
    id: str
    alert_code: str
    fraud_category: str
    severity: str
    entity_reference: str
    anomaly_score: float
    status: str
    mitigation_action: str


class FinRiskAssessmentResponse(BaseModel):
    liquidity_risk_score: float
    credit_risk_score: float
    fx_volatility_exposure_usd: float
    interest_rate_sensitivity: str
    overall_financial_health_index: float


# 9. Financial Digital Twin & What-If Simulations
class FinDigitalTwinResponse(BaseModel):
    id: str
    twin_code: str
    revenue_growth_rate_pct: float
    gross_margin_pct: float
    working_capital_usd: float
    dso_days: float
    dpo_days: float
    resilience_rating: str


class FinFinancialWhatIfRequest(BaseModel):
    scenario_type: str = "REVENUE_CONTRACTION_20"  # REVENUE_CONTRACTION_20, AR_PAYMENT_DELAY_30D, OPEX_SURGE_15, RATE_HIKE_200BP
    horizon_months: int = 12
    dry_run: bool = True


class FinFinancialWhatIfResponse(BaseModel):
    scenario_type: str
    horizon_months: int
    projected_cash_impact_usd: float
    projected_ebitda_impact_usd: float
    post_shock_runway_months: float
    recommended_mitigations: List[str]
    requires_executive_action: bool


# 10. Financial Command Center Summary & Autonomous Operating Cycle
class FinControlCenterSummaryResponse(BaseModel):
    total_cash_and_equivalents_usd: float
    available_liquidity_usd: float
    net_monthly_burn_rate_usd: float
    estimated_runway_months: float
    total_accounts_receivable_usd: float
    dso_days: float
    total_accounts_payable_usd: float
    dpo_days: float
    budget_variance_pct: float
    active_fraud_alerts_count: int
    open_accounting_period: str
    active_financial_agents_count: int


class FinOperatingCycleExecutionResponse(BaseModel):
    cycle_run_id: str
    stage_progress: Dict[str, str]
    overall_status: str
    transactions_processed: int
    reconciliations_completed: int
    actions_requiring_human_approval: int
    simulated_cash_optimization_usd: float
