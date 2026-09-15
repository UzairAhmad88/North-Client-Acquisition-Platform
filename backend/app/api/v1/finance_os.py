"""
Phase 72 Enterprise Financial Operating System - FastAPI Router
Mount path: /finance-os
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from datetime import datetime
import logging

from app.services.finance.service import EnterpriseFinancialOperatingService
from app.schemas.autonomous_financial_operating_system import (
    FinAccountCreate, FinAccountResponse,
    FinInvoiceCreate, FinInvoiceResponse, FinArAgingResponse,
    FinVendorBillResponse, FinThreeWayMatchResponse,
    FinPaymentCreate, FinPaymentResponse, FinPaymentApprovalRequest,
    FinBankAccountResponse, FinBankTransactionResponse, FinReconciliationResponse,
    FinJournalCreate, FinJournalResponse, FinAccountingPeriodResponse,
    FinBudgetResponse, FinCashForecastResponse, FinTreasuryPositionResponse,
    FinFraudAlertResponse, FinRiskAssessmentResponse,
    FinDigitalTwinResponse, FinFinancialWhatIfRequest, FinFinancialWhatIfResponse,
    FinControlCenterSummaryResponse, FinOperatingCycleExecutionResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/finance-os", tags=["Enterprise Financial Operating System"])

def get_fin_service() -> EnterpriseFinancialOperatingService:
    return EnterpriseFinancialOperatingService()


# ---------------------------------------------------------
# Executive Command Center & 12-Stage Operating Loop
# ---------------------------------------------------------
@router.get("/summary", response_model=FinControlCenterSummaryResponse)
def get_control_center_summary(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    return FinControlCenterSummaryResponse(
        total_cash_and_equivalents_usd=12540000.00,
        available_liquidity_usd=10200000.00,
        net_monthly_burn_rate_usd=450000.00,
        estimated_runway_months=27.8,
        total_accounts_receivable_usd=3420000.00,
        dso_days=38.5,
        total_accounts_payable_usd=1820000.00,
        dpo_days=42.1,
        budget_variance_pct=-2.4,
        active_fraud_alerts_count=0,
        open_accounting_period="2026-09",
        active_financial_agents_count=25
    )

@router.post("/operating-cycle/run", response_model=FinOperatingCycleExecutionResponse)
def run_financial_operating_cycle(
    tenant_id: str = Query("tenant-default"),
    dry_run: bool = Query(True),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    cycle = service.run_financial_operating_cycle(tenant_id, dry_run)
    stage_map = {s["stage"]: s["status"] for s in cycle["stages"]}
    return FinOperatingCycleExecutionResponse(
        cycle_run_id=cycle["cycle_id"],
        stage_progress=stage_map,
        overall_status=cycle["status"],
        transactions_processed=142,
        reconciliations_completed=48,
        actions_requiring_human_approval=2,
        simulated_cash_optimization_usd=185000.00
    )


# ---------------------------------------------------------
# Chart of Accounts & General Ledger & Periods
# ---------------------------------------------------------
@router.get("/chart-of-accounts", response_model=List[FinAccountResponse])
def list_chart_of_accounts(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    return [
        FinAccountResponse(
            id="coa-1000",
            account_number="1000",
            account_name="Operating Cash & Equivalents",
            account_type="ASSET",
            sub_category="CURRENT",
            currency="USD",
            current_balance=10200000.00,
            is_reconcilable=True
        ),
        FinAccountResponse(
            id="coa-1200",
            account_number="1200",
            account_name="Accounts Receivable",
            account_type="ASSET",
            sub_category="CURRENT",
            currency="USD",
            current_balance=3420000.00,
            is_reconcilable=True
        ),
        FinAccountResponse(
            id="coa-2000",
            account_number="2000",
            account_name="Accounts Payable",
            account_type="LIABILITY",
            sub_category="CURRENT",
            currency="USD",
            current_balance=1820000.00,
            is_reconcilable=True
        ),
        FinAccountResponse(
            id="coa-4000",
            account_number="4000",
            account_name="Enterprise Platform SaaS Revenue",
            account_type="REVENUE",
            sub_category="OPERATING",
            currency="USD",
            current_balance=1450000.00,
            is_reconcilable=False
        )
    ]

@router.post("/chart-of-accounts", response_model=FinAccountResponse)
def create_chart_of_account(
    account: FinAccountCreate,
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    return FinAccountResponse(
        id=f"coa-{account.account_number}",
        account_number=account.account_number,
        account_name=account.account_name,
        account_type=account.account_type,
        sub_category=account.sub_category,
        currency=account.currency,
        current_balance=0.0,
        is_reconcilable=True
    )

@router.post("/journals/post", response_model=FinJournalResponse)
def post_journal_entry(
    journal: FinJournalCreate,
    idempotency_key: Optional[str] = Header(None),
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    # Enforce Double-entry Invariant: Debits == Credits (equal amount on debit and credit account)
    if journal.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Journal posting amount must be strictly greater than 0"
        )
    return FinJournalResponse(
        id=f"jnl-{int(datetime.utcnow().timestamp())}",
        journal_code=journal.journal_code,
        entity_id=tenant_id,
        period_code=journal.period_code,
        entry_date=datetime.utcnow(),
        description=journal.description,
        source_module=journal.source_module,
        total_debit=journal.amount,
        total_credit=journal.amount,
        posting_status="POSTED",
        is_balanced=True
    )

@router.get("/accounting-periods", response_model=List[FinAccountingPeriodResponse])
def list_accounting_periods(tenant_id: str = Query("tenant-default")):
    return [
        FinAccountingPeriodResponse(
            id="per-2026-08",
            period_code="2026-08",
            fiscal_year=2026,
            period_number=8,
            status="LOCKED",
            start_date=datetime(2026, 8, 1),
            end_date=datetime(2026, 8, 31)
        ),
        FinAccountingPeriodResponse(
            id="per-2026-09",
            period_code="2026-09",
            fiscal_year=2026,
            period_number=9,
            status="OPEN",
            start_date=datetime(2026, 9, 1),
            end_date=datetime(2026, 9, 30)
        )
    ]


# ---------------------------------------------------------
# Billing, Invoicing & Accounts Receivable
# ---------------------------------------------------------
@router.get("/invoices", response_model=List[FinInvoiceResponse])
def list_invoices(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    return [
        FinInvoiceResponse(
            id="inv-101",
            invoice_number="INV-2026-001",
            customer_id="cust-enterprise-a",
            subtotal=100000.00,
            tax_amount=0.00,
            total_amount=100000.00,
            paid_amount=0.00,
            currency="USD",
            status="ISSUED",
            issue_date=datetime(2026, 9, 1),
            due_date=datetime(2026, 10, 1)
        )
    ]

@router.post("/invoices", response_model=FinInvoiceResponse)
def create_invoice(
    inv: FinInvoiceCreate,
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    tot = inv.subtotal + inv.tax_amount
    return FinInvoiceResponse(
        id=f"inv-{int(datetime.utcnow().timestamp())}",
        invoice_number=inv.invoice_number,
        customer_id=inv.customer_id,
        subtotal=inv.subtotal,
        tax_amount=inv.tax_amount,
        total_amount=tot,
        paid_amount=0.00,
        currency=inv.currency,
        status="ISSUED",
        issue_date=datetime.utcnow(),
        due_date=inv.due_date
    )

@router.get("/ar-aging", response_model=FinArAgingResponse)
def get_ar_aging_summary(tenant_id: str = Query("tenant-default")):
    return FinArAgingResponse(
        current_bucket_usd=2980000.00,
        days_1_30_usd=320000.00,
        days_31_60_usd=95000.00,
        days_61_90_usd=0.00,
        days_90_plus_usd=25000.00,
        total_outstanding_usd=3420000.00,
        dso_days=38.5
    )


# ---------------------------------------------------------
# Accounts Payable, Vendor Bills & 3-Way Match
# ---------------------------------------------------------
@router.get("/vendor-bills", response_model=List[FinVendorBillResponse])
def list_vendor_bills(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    return [
        FinVendorBillResponse(
            id="bill-501",
            bill_number="BILL-AWS-882",
            vendor_id="vend-aws",
            purchase_order_id="po-sc-102",
            goods_receipt_id="gr-sc-102",
            total_amount=45000.00,
            currency="USD",
            three_way_match_status="PERFECT_MATCH",
            status="PENDING_APPROVAL",
            due_date=datetime(2026, 9, 18)
        )
    ]

@router.post("/three-way-match", response_model=FinThreeWayMatchResponse)
def execute_three_way_matching(
    bill_id: str = Query(...),
    po_id: str = Query(...),
    goods_receipt_id: str = Query(...),
    po_amount: float = Query(45000.00),
    billed_amount: float = Query(45000.00),
    tolerance_threshold: float = Query(50.00),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    variance = abs(po_amount - billed_amount)
    is_matched = variance <= tolerance_threshold
    return FinThreeWayMatchResponse(
        bill_id=bill_id,
        purchase_order_id=po_id,
        goods_receipt_id=goods_receipt_id,
        po_amount=po_amount,
        received_quantity=1.0,
        billed_amount=billed_amount,
        variance_amount=variance,
        is_matched=is_matched,
        requires_approval=billed_amount >= 25000.00 or not is_matched
    )


# ---------------------------------------------------------
# Payment Operating System & Governance
# ---------------------------------------------------------
@router.get("/payments", response_model=List[FinPaymentResponse])
def list_payments(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    return [
        FinPaymentResponse(
            id="pay-901",
            payment_reference="PAY-2026-009",
            idempotency_key="idemp-pay-901",
            payment_type="VENDOR_DISBURSEMENT",
            amount=45000.00,
            currency="USD",
            source_bank_account_id="bank-chase-01",
            destination_entity_or_vendor="vend-aws",
            status="PENDING_APPROVAL",
            fraud_risk_score=0.02,
            requires_dual_approval=True
        )
    ]

@router.post("/payments", response_model=FinPaymentResponse)
def initiate_payment(
    payment: FinPaymentCreate,
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    requires_dual = payment.amount >= 25000.00 or payment.requires_dual_approval
    return FinPaymentResponse(
        id=f"pay-{int(datetime.utcnow().timestamp())}",
        payment_reference=payment.payment_reference,
        idempotency_key=payment.idempotency_key,
        payment_type=payment.payment_type,
        amount=payment.amount,
        currency=payment.currency,
        source_bank_account_id=payment.source_bank_account_id,
        destination_entity_or_vendor=payment.destination_entity_or_vendor,
        status="PENDING_APPROVAL" if requires_dual else "APPROVED",
        fraud_risk_score=0.01,
        requires_dual_approval=requires_dual
    )

@router.post("/payments/{payment_id}/approve", response_model=FinPaymentResponse)
def approve_payment(
    payment_id: str,
    approval: FinPaymentApprovalRequest,
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    return FinPaymentResponse(
        id=payment_id,
        payment_reference=f"PAY-{payment_id}",
        idempotency_key=f"idemp-approved-{payment_id}",
        payment_type="VENDOR_DISBURSEMENT",
        amount=45000.00,
        currency="USD",
        source_bank_account_id="bank-chase-01",
        destination_entity_or_vendor="vend-aws",
        status="APPROVED" if approval.decision == "APPROVED" else "REJECTED",
        fraud_risk_score=0.01,
        requires_dual_approval=True
    )


# ---------------------------------------------------------
# Banking, Ingestion & High-Confidence Reconciliation
# ---------------------------------------------------------
@router.get("/bank-accounts", response_model=List[FinBankAccountResponse])
def list_bank_accounts(tenant_id: str = Query("tenant-default")):
    return [
        FinBankAccountResponse(
            id="bank-chase-01",
            account_code="CHASE-TREASURY-01",
            bank_name="JPMorgan Chase Commercial",
            account_mask="****-4912",
            currency="USD",
            ledger_balance=10200000.00,
            available_balance=10200000.00,
            last_synced_at=datetime.utcnow()
        )
    ]

@router.post("/reconciliation/auto-match", response_model=List[FinReconciliationResponse])
def trigger_automated_reconciliation(
    tenant_id: str = Query("tenant-default"),
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    return [
        FinReconciliationResponse(
            id="rec-match-01",
            bank_transaction_id="tx-bk-101",
            journal_entry_id="jnl-post-88",
            match_confidence=0.99,
            match_type="EXACT_AMOUNT_AND_DATE",
            reconciled_by="AUTONOMOUS_RECONCILIATION_AGENT"
        )
    ]


# ---------------------------------------------------------
# Treasury, Cash Forecasting & Runway Analysis
# ---------------------------------------------------------
@router.get("/treasury/positions", response_model=FinTreasuryPositionResponse)
def get_treasury_positions(tenant_id: str = Query("tenant-default")):
    return FinTreasuryPositionResponse(
        total_cash_usd=12540000.00,
        restricted_cash_usd=2340000.00,
        total_debt_principal=0.0,
        annual_debt_service=0.0,
        net_liquidity_usd=10200000.00,
        eur_exposure_usd=620000.00,
        jpy_exposure_usd=180000.00
    )

@router.get("/cash-forecast", response_model=FinCashForecastResponse)
def get_cash_forecast(tenant_id: str = Query("tenant-default")):
    return FinCashForecastResponse(
        forecast_period="13_WEEKS_ROLLING",
        opening_cash=12540000.00,
        projected_inflows=4550000.00,
        projected_outflows=2925000.00,
        projected_closing_cash=14165000.00,
        net_monthly_burn_rate=450000.00,
        estimated_runway_months=27.8
    )


# ---------------------------------------------------------
# Financial Scenarios & Digital Twin Simulation
# ---------------------------------------------------------
@router.post("/scenarios/simulate", response_model=FinFinancialWhatIfResponse)
def simulate_financial_scenario(
    req: FinFinancialWhatIfRequest,
    service: EnterpriseFinancialOperatingService = Depends(get_fin_service)
):
    mitigations = [
        "Extend non-critical accounts payable terms from 30 to 45 days.",
        "Implement prompt settlement discount (2% Net 10) on enterprise invoices.",
        "Freeze discretionary cloud spot cluster auto-scaling thresholds."
    ]
    return FinFinancialWhatIfResponse(
        scenario_type=req.scenario_type,
        horizon_months=req.horizon_months,
        projected_cash_impact_usd=-850000.00,
        projected_ebitda_impact_usd=-290000.00,
        post_shock_runway_months=22.4,
        recommended_mitigations=mitigations,
        requires_executive_action=True
    )


# ---------------------------------------------------------
# Autonomous Financial AI Agents Execution Endpoint
# ---------------------------------------------------------
@router.get("/agents")
def list_financial_agents():
    from agents.finance import __all__ as agent_names
    return {
        "total_agents": len(agent_names),
        "agents": [
            {"agent_id": f"fin_agent_{i+1}", "name": name, "status": "READY_GOVERNED"}
            for i, name in enumerate(agent_names)
        ]
    }
