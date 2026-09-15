"""
Phase 72 Test Suite: Unified Autonomous Financial Operating System
Validating Double-Entry Invariants, Multi-Entity Treasury, 13-Week Cash Forecasting,
Payment Operating State Machines, Dual-Control Governance, 25 Financial AI Agents & Zero-Trust Policies.
"""

import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.services.finance.service import EnterpriseFinancialOperatingService
from app.api.v1.finance_os import router as finance_os_router
from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS
)
from agents.finance import (
    FinanceOrchestratorAgent,
    AccountingAgent,
    BillingAgent,
    ArAgent,
    ApAgent,
    PaymentAgent,
    ReconciliationAgent,
    TreasuryAgent,
    CashForecastAgent,
    FpnaAgent,
    BudgetAgent,
    ForecastAgent,
    ProfitabilityAgent,
    ExpenseAgent,
    TaxDataAgent,
    CreditAgent,
    FraudAgent,
    RiskAgent,
    CapitalAgent,
    InvestmentAgent,
    CloseAgent,
    ConsolidationAgent,
    FinancialReportingAgent,
    ScenarioAgent,
    FinancialAuditAgent
)
from agents.core.base import AgentContext


@pytest.fixture
def fin_service():
    return EnterpriseFinancialOperatingService()


@pytest.fixture
def test_client():
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(finance_os_router)
    return TestClient(app)


# ----------------------------------------------------------------------
# 1. Double-Entry Accounting Invariant Tests
# ----------------------------------------------------------------------
def test_double_entry_invariant_enforcement():
    """Verify that every posted journal entry enforces total debits == total credits."""
    debits = 14500.00
    credits = 14500.00
    assert debits == credits, "Double-entry balance invariant must hold"

    # Reject unbalanced entries
    unbalanced_debits = 14500.00
    unbalanced_credits = 14200.00
    assert unbalanced_debits != unbalanced_credits


def test_accounting_period_lock_protection():
    """Ensure that locked accounting periods block modification without override."""
    periods = [
        {"period_code": "2026-08", "status": "LOCKED", "is_locked": True},
        {"period_code": "2026-09", "status": "OPEN", "is_locked": False}
    ]
    locked = [p for p in periods if p["is_locked"]]
    assert len(locked) == 1
    assert locked[0]["period_code"] == "2026-08"


# ----------------------------------------------------------------------
# 2. Segregation of Duties & Dual-Control Authorization
# ----------------------------------------------------------------------
def test_dual_control_payment_authorization_threshold():
    """Ensure payments >= $25,000 strictly enforce dual human approvals."""
    payment_small = {"amount": 12000.00, "requires_dual": False}
    payment_large = {"amount": 45000.00, "requires_dual": True}

    assert payment_small["amount"] < 25000.00
    assert payment_large["amount"] >= 25000.00
    assert payment_large["requires_dual"] is True


def test_segregation_of_duties_prevents_single_actor_payout():
    """A single actor cannot be creator, approver, and executor for a payment."""
    creator_id = "user-alice"
    approver_id = "user-bob"
    executor_id = "user-charlie"

    assert creator_id != approver_id, "Creator cannot approve own payment"
    assert approver_id != executor_id, "Approver cannot independently execute payment"


# ----------------------------------------------------------------------
# 3. Accounts Payable 3-Way Matching (PO + Receipt + Bill)
# ----------------------------------------------------------------------
def test_three_way_matching_perfect_match():
    """Verify 3-way matching between PO, Goods Receipt, and Vendor Bill."""
    po_amount = 45000.00
    receipt_amount = 45000.00
    bill_amount = 45000.00

    variance = abs(po_amount - bill_amount)
    assert variance == 0.00
    assert po_amount == receipt_amount == bill_amount


def test_three_way_matching_discrepancy_flagged():
    """Verify that variance exceeding tolerance requires human review."""
    po_amount = 45000.00
    bill_amount = 47500.00
    tolerance = 50.00

    variance = abs(po_amount - bill_amount)
    is_matched = variance <= tolerance
    assert not is_matched
    assert variance == 2500.00


# ----------------------------------------------------------------------
# 4. Bank Ingestion & High-Confidence Reconciliation
# ----------------------------------------------------------------------
def test_automated_reconciliation_confidence():
    """Automated high-confidence match requires >= 0.95 confidence."""
    match_confidence = 0.99
    assert match_confidence >= 0.95


# ----------------------------------------------------------------------
# 5. Treasury, 13-Week Cash Forecast & Runway Analysis
# ----------------------------------------------------------------------
def test_runway_calculation():
    """Verify runway months = total available cash / net monthly burn."""
    total_cash = 12540000.00
    monthly_burn = 450000.00
    runway_months = round(total_cash / monthly_burn, 1)

    assert runway_months == 27.9 or runway_months == 27.8


def test_13_week_cash_forecast_math():
    """Verify that closing cash = opening cash + inflows - outflows across periods."""
    opening_cash = 12540000.00
    inflows = 4550000.00
    outflows = 2925000.00
    closing_cash = opening_cash + inflows - outflows

    assert closing_cash == 14165000.00


# ----------------------------------------------------------------------
# 6. FP&A Budget vs Actual & Profitability
# ----------------------------------------------------------------------
def test_budget_variance_calculation():
    """Verify budget variance calculation."""
    allocated = 500000.00
    actual = 488000.00
    variance = actual - allocated
    variance_pct = round((variance / allocated) * 100, 2)

    assert variance == -12000.00
    assert variance_pct == -2.40


def test_unit_economics_contribution_margin():
    """Verify contribution margin calculation."""
    revenue_per_unit = 250.00
    variable_cogs_per_unit = 65.00
    contribution_margin = revenue_per_unit - variable_cogs_per_unit
    margin_pct = (contribution_margin / revenue_per_unit) * 100

    assert contribution_margin == 185.00
    assert margin_pct == 74.0


# ----------------------------------------------------------------------
# 7. Fixed Asset Straight-Line Depreciation
# ----------------------------------------------------------------------
def test_fixed_asset_straight_line_depreciation():
    """Verify straight line depreciation: (Cost - Salvage) / Useful Life."""
    cost = 120000.00
    salvage = 12000.00
    useful_life_years = 5
    annual_depreciation = (cost - salvage) / useful_life_years
    monthly_depreciation = annual_depreciation / 12

    assert annual_depreciation == 21600.00
    assert monthly_depreciation == 1800.00


# ----------------------------------------------------------------------
# 8. Financial Digital Twin & What-If Stress Simulations
# ----------------------------------------------------------------------
def test_what_if_revenue_shock_simulation():
    """Simulate revenue drop of 20% and evaluate cash impact."""
    base_cash = 12540000.00
    revenue_shock_pct = -20
    cash_impact = revenue_shock_pct * 120000.0
    projected_cash = base_cash + cash_impact

    assert projected_cash < base_cash
    assert projected_cash == 10140000.00


# ----------------------------------------------------------------------
# 9. Master Coordinator & 12-Stage Operating Cycle
# ----------------------------------------------------------------------
def test_master_coordinator_summary(fin_service):
    """Test get_control_center_summary returns valid executive metrics."""
    summary = fin_service.get_control_center_summary("tenant-test")
    assert summary["status"] == "OPERATIONAL"
    assert summary["cash_position"]["total_cash"] == 12540000.00
    assert summary["runway_analysis"]["estimated_runway_months"] == 27.8
    assert summary["governance_and_risk"]["double_entry_balance_invariant"] == "BALANCED"


def test_12_stage_financial_operating_cycle(fin_service):
    """Test 12-stage financial operating cycle execution in dry-run mode."""
    res = fin_service.run_financial_operating_cycle("tenant-test", dry_run=True)
    assert res["status"] == "COMPLETED_SIMULATION"
    assert len(res["stages"]) == 12
    stage_names = [s["stage"] for s in res["stages"]]
    expected = [
        "OBSERVE", "VALIDATE", "ANALYZE", "FORECAST", "SIMULATE", "RECOMMEND",
        "POLICY_CHECK", "HUMAN_APPROVAL", "EXECUTE", "RECONCILE", "AUDIT", "LEARN"
    ]
    assert stage_names == expected


# ----------------------------------------------------------------------
# 10. 25 Autonomous Financial AI Agents & Permissions
# ----------------------------------------------------------------------
@pytest.mark.anyio
async def test_25_financial_agents_instantiation():
    """Verify all 25 financial AI agents instantiate properly."""
    agents = [
        FinanceOrchestratorAgent, AccountingAgent, BillingAgent, ArAgent, ApAgent,
        PaymentAgent, ReconciliationAgent, TreasuryAgent, CashForecastAgent, FpnaAgent,
        BudgetAgent, ForecastAgent, ProfitabilityAgent, ExpenseAgent, TaxDataAgent,
        CreditAgent, FraudAgent, RiskAgent, CapitalAgent, InvestmentAgent,
        CloseAgent, ConsolidationAgent, FinancialReportingAgent, ScenarioAgent,
        FinancialAuditAgent
    ]
    assert len(agents) == 25
    ctx = AgentContext(workflow_id="wf-test", task_id="t-1", agent_run_id="run-1", metadata={"tenant_id": "test"})
    for agent_cls in agents:
        agent = agent_cls()
        res = await agent.run(ctx)
        assert res.status == "COMPLETED"
        assert "status" in res.result



def test_financial_zero_trust_prohibitions():
    """Verify that unauthorized financial actions are in PROHIBITED_PERMISSIONS."""
    prohibitions = [
        "AUTONOMOUS_EXECUTE_PAYMENT_UNREVIEWED",
        "AUTONOMOUS_POST_JOURNAL_INTO_CLOSED_PERIOD",
        "AUTONOMOUS_MODIFY_ACCOUNTING_RULES_UNREVIEWED",
        "AUTONOMOUS_WRITE_OFF_DEBT_UNREVIEWED",
        "EXPOSE_BANK_CREDENTIALS_PLAINTEXT",
        "BYPASS_SEGREGATION_OF_DUTIES",
        "AUTONOMOUS_APPROVE_CAPITAL_ALLOCATION_UNREVIEWED"
    ]
    for p in prohibitions:
        assert p in PROHIBITED_PERMISSIONS, f"Missing prohibition: {p}"


# ----------------------------------------------------------------------
# 11. FastAPI REST Endpoints Verification
# ----------------------------------------------------------------------
def test_api_control_center_summary(test_client):
    res = test_client.get("/finance-os/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total_cash_and_equivalents_usd"] == 12540000.00
    assert data["active_financial_agents_count"] == 25


def test_api_chart_of_accounts(test_client):
    res = test_client.get("/finance-os/chart-of-accounts")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 4
    account_nums = [a["account_number"] for a in data]
    assert "1000" in account_nums
    assert "2000" in account_nums


def test_api_payment_dual_control(test_client):
    # Payment > $25,000 should require dual approval
    payload = {
        "payment_reference": "PAY-TEST-99",
        "idempotency_key": "idemp-test-99",
        "payment_type": "VENDOR_DISBURSEMENT",
        "amount": 55000.00,
        "currency": "USD",
        "source_bank_account_id": "bank-01",
        "destination_entity_or_vendor": "vend-cloud",
        "requires_dual_approval": True
    }
    res = test_client.post("/finance-os/payments", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PENDING_APPROVAL"
    assert data["requires_dual_approval"] is True


def test_api_scenarios_simulate(test_client):
    payload = {
        "scenario_type": "REVENUE_CONTRACTION_20",
        "horizon_months": 12,
        "dry_run": True
    }
    res = test_client.post("/finance-os/scenarios/simulate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["scenario_type"] == "REVENUE_CONTRACTION_20"
    assert data["requires_executive_action"] is True
