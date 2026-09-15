"""Unit tests for Phase 40 — Unified Billing, Invoicing, Payments, Financial Operations & Commercial Control."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from datetime import datetime, timezone
from decimal import Decimal
import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from integrations.payments.base import PaymentRequest, RefundRequest
from integrations.payments.models import PaymentProviderType
from integrations.payments.providers.mock import MockPaymentProvider
from integrations.payments.service import PaymentService

from app.finance.base import (
    InvoiceStatus,
    PaymentStatus,
    PaymentTerms,
    TaxType,
    LedgerDirection,
    FinancialAccountType,
    InvoiceTotals,
)
from app.finance.calculator import FinancialCalculator
from app.finance.invoicing import InvoicingManager
from app.finance.reconciliation import ReconciliationManager
from app.finance.ledger import LedgerManager
from app.finance.profitability import ProfitabilityManager
from app.finance.authorization import FinancialAuthorizationManager
from app.finance.service import FinancialPlatformService
from app.models.base import Base
from app.models.finance import (
    BillingProfileModel,
    CurrencyModel,
    TaxProfileModel,
    InvoiceModel,
    InvoiceItemModel,
    PaymentModel,
    FinancialAccountModel,
    LedgerEntryModel,
)
from app.repositories.finance import FinanceRepository
from agents.core.context import AgentContext
from agents.core.errors import AgentPermissionDeniedError
from agents.finance.finance_agent import FinanceAgent
from agents.finance.validation import FinancialSafetyValidator
from agents.finance.forecasting import FinancialForecastingEngine
from agents.finance.reconciliation import FinancialReconciliationAssistant
from agents.finance.profitability import FinancialProfitabilityAssistant


@pytest.fixture
def db_session():
    """Provides an isolated in-memory SQLite database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


class TestFinancialCalculator:
    """Deterministic Decimal arithmetic tests."""

    def test_line_item_and_invoice_totals(self):
        items = [
            {"title": "Dev Sprint 1", "quantity": "2.5", "unit_price": "100.00"},
            {"title": "Architecture Design", "quantity": "1.0", "unit_price": "500.00"},
        ]
        totals = FinancialCalculator.calculate_invoice_totals(
            items=items,
            discount_rate_pct=Decimal("10.00"),  # 10% discount on 750 = 75.00 -> taxable = 675.00
            tax_rate_pct=Decimal("8.25"),        # 8.25% of 675 = 55.69
            tax_type=TaxType.SALES_TAX,
        )

        assert totals.subtotal == Decimal("750.00")
        assert totals.discount_amount == Decimal("75.00")
        assert totals.taxable_amount == Decimal("675.00")
        assert totals.tax_amount == Decimal("55.69")
        assert totals.total_amount == Decimal("730.69")

    def test_margin_and_variance_percentages(self):
        # Margin: (Revenue - Cost) / Revenue
        margin = FinancialCalculator.calculate_margin_pct(Decimal("40.00"), Decimal("100.00"))
        assert margin == Decimal("40.00")

        # Zero revenue protection
        zero_margin = FinancialCalculator.calculate_margin_pct(Decimal("0.00"), Decimal("0.00"))
        assert zero_margin == Decimal("0.00")

        # Variance: (Actual - Baseline) / Baseline
        variance = FinancialCalculator.calculate_variance_pct(Decimal("120.00"), Decimal("100.00"))
        assert variance == Decimal("20.00")


class TestPaymentProviderIntegration:
    """Payment provider abstraction and mock provider testing."""

    def test_mock_charge_and_idempotency(self):
        provider = MockPaymentProvider()
        key = f"idem-{uuid.uuid4()}"
        req = PaymentRequest(
            amount=Decimal("250.00"),
            currency="USD",
            payment_method="credit_card",
            idempotency_key=key,
            tenant_id="tenant-1",
        )

        # Initial charge
        res1 = provider.charge(req)
        assert res1.is_success is True
        assert res1.amount == Decimal("250.00")
        assert res1.fee_amount == Decimal("7.55")  # (250 * 0.029) + 0.30 = 7.25 + 0.30 = 7.55

        # Re-sending with same idempotency key returns identical cached result
        res2 = provider.charge(req)
        assert res2.provider_payment_id == res1.provider_payment_id

    def test_mock_refund(self):
        provider = MockPaymentProvider()
        ref_req = RefundRequest(
            payment_id="ch_mock_123",
            amount=Decimal("100.00"),
            currency="USD",
            reason="Customer requested",
            tenant_id="tenant-1",
        )
        ref_res = provider.refund(ref_req)
        assert ref_res.is_success is True
        assert ref_res.amount == Decimal("100.00")


class TestInvoicingLifecycle:
    """Invoice generation, milestone conversions, and status transitions."""

    def test_create_draft_from_contract_milestone(self):
        draft = InvoicingManager.draft_from_contract_milestone(
            tenant_id="tenant-1",
            client_id="client-1",
            contract_id="contract-100",
            milestone_id="ms-01",
            milestone_name="Beta MVP Delivery",
            milestone_amount=Decimal("15000.00"),
            payment_terms=PaymentTerms.NET_30,
        )

        assert draft["status"] == InvoiceStatus.DRAFT.value
        assert draft["total_amount"] == "15000.00"
        assert draft["balance_due"] == "15000.00"
        assert len(draft["items"]) == 1
        assert draft["items"][0]["title"] == "Milestone: Beta MVP Delivery"

    def test_create_draft_from_change_request(self):
        draft = InvoicingManager.draft_from_change_request(
            tenant_id="tenant-1",
            client_id="client-1",
            change_request_id="cr-50",
            change_request_title="Add Multi-Currency Support",
            price_amount=Decimal("3500.00"),
        )
        assert draft["total_amount"] == "3500.00"
        assert draft["items"][0]["item_type"] == "change_request"

    def test_valid_and_invalid_transitions(self):
        assert InvoicingManager.validate_transition("draft", "pending_approval") is True
        assert InvoicingManager.validate_transition("pending_approval", "approved") is True
        assert InvoicingManager.validate_transition("approved", "issued") is True
        assert InvoicingManager.validate_transition("issued", "paid") is True
        # Invalid backwards transition
        assert InvoicingManager.validate_transition("paid", "draft") is False


class TestReconciliationManager:
    """Payment transaction reconciliation against invoices."""

    def test_exact_match(self):
        res = ReconciliationManager.match_transaction(
            provider_transaction_id="tx-1",
            provider_amount=Decimal("1500.00"),
            provider_currency="USD",
            provider_status="succeeded",
            invoice_id="inv-1",
            invoice_balance_due=Decimal("1500.00"),
            invoice_currency="USD",
        )
        assert res["status"] == "matched"
        assert res["is_exact_match"] is True
        assert res["resulting_invoice_status"] == InvoiceStatus.PAID.value
        assert res["requires_human_approval"] is False

    def test_partial_match(self):
        res = ReconciliationManager.match_transaction(
            provider_transaction_id="tx-2",
            provider_amount=Decimal("500.00"),
            provider_currency="USD",
            provider_status="succeeded",
            invoice_id="inv-1",
            invoice_balance_due=Decimal("1500.00"),
            invoice_currency="USD",
        )
        assert res["status"] == "partial_match"
        assert res["discrepancy_type"] == "partial_payment"
        assert res["resulting_invoice_status"] == InvoiceStatus.PARTIALLY_PAID.value
        assert res["remaining_balance"] == "1000.00"

    def test_overpayment_requires_approval(self):
        res = ReconciliationManager.match_transaction(
            provider_transaction_id="tx-3",
            provider_amount=Decimal("2000.00"),
            provider_currency="USD",
            provider_status="succeeded",
            invoice_id="inv-1",
            invoice_balance_due=Decimal("1500.00"),
            invoice_currency="USD",
        )
        assert res["status"] == "overpaid"
        assert res["overpaid_amount"] == "500.00"
        assert res["requires_human_approval"] is True


class TestLedgerManager:
    """Double-entry balanced journal entries and adjustments."""

    def test_balanced_journal_entry(self):
        journal = LedgerManager.post_invoice_issuance(
            tenant_id="tenant-1",
            invoice_id="inv-1",
            invoice_number="INV-2026-0001",
            accounts_receivable_account_id="acc-ar",
            revenue_account_id="acc-rev",
            total_amount=Decimal("1000.00"),
            tax_account_id="acc-tax",
            tax_amount=Decimal("80.00"),
        )
        assert journal["total_amount"] == "1000.00"
        assert len(journal["entries"]) == 3

        # Verify Debits == Credits
        debits = sum(Decimal(e["amount"]) for e in journal["entries"] if e["direction"] == "debit")
        credits = sum(Decimal(e["amount"]) for e in journal["entries"] if e["direction"] == "credit")
        assert debits == credits == Decimal("1000.00")

    def test_unbalanced_entry_rejected(self):
        with pytest.raises(ValueError, match="Unbalanced journal entry"):
            LedgerManager.create_journal_entry(
                tenant_id="tenant-1",
                description="Faulty entry",
                reference_type="manual",
                reference_id="ref-1",
                entries=[
                    {"account_id": "acc-1", "direction": "debit", "amount": "100.00"},
                    {"account_id": "acc-2", "direction": "credit", "amount": "80.00"},
                ]
            )


class TestProfitabilityManager:
    """Profitability analysis and client masking."""

    def test_project_profitability_breakdown(self):
        analysis = ProfitabilityManager.analyze_project_profitability(
            project_id="prj-1",
            contracted_revenue=Decimal("50000.00"),
            invoiced_revenue=Decimal("50000.00"),
            collected_revenue=Decimal("50000.00"),
            estimated_cost=Decimal("20000.00"),
            labor_hours_logged=Decimal("100.00"),
            labor_hourly_cost_rate=Decimal("120.00"),  # 12,000 labor
            ai_token_cost=Decimal("500.00"),
            infrastructure_cost=Decimal("1500.00"),
            subcontractor_cost=Decimal("2000.00"),
            other_expenses=Decimal("0.00"),            # total actual cost = 16,000
        )

        assert analysis["cost_breakdown"]["actual_total_cost"] == "16000.00"
        assert analysis["profitability_metrics"]["realized_gross_profit"] == "34000.00"
        assert analysis["profitability_metrics"]["realized_margin_pct"] == "68.00"
        assert analysis["commercial_health"]["status"] == "highly_profitable"

    def test_client_payload_masking(self):
        raw = {
            "project_id": "prj-1",
            "cost_breakdown": {"actual_total_cost": "16000.00"},
            "profitability_metrics": {"realized_margin_pct": "68.00"},
            "financial_summary": {"contracted_revenue": "50000.00"},
        }
        masked = FinancialAuthorizationManager.mask_client_payload(raw, is_client=True)
        assert "cost_breakdown" not in masked
        assert "profitability_metrics" not in masked
        assert masked["financial_summary"]["contracted_revenue"] == "50000.00"


class TestFinanceAgent:
    """Agent validation, forecasting, and guardrails."""

    @pytest.mark.asyncio
    async def test_agent_profitability_task(self):
        agent = FinanceAgent()
        context = AgentContext(
            workflow_id="wf-1",
            task_id="task-1",
            agent_run_id="run-1",
            metadata={
                "task": "profitability_analysis",
                "project_id": "prj-test",
                "contracted_revenue": "20000.00",
                "invoiced_revenue": "20000.00",
                "collected_revenue": "20000.00",
                "estimated_cost": "10000.00",
                "labor_hours_logged": "40.00",
                "labor_hourly_cost_rate": "150.00",
            }
        )

        result = await agent.run(context)
        assert result.status == "completed"
        assert "agent_insights" in result.result
        assert result.result["profitability_metrics"]["realized_margin_pct"] == "70.00"

    @pytest.mark.asyncio
    async def test_agent_prohibited_action_raises_error(self):
        agent = FinanceAgent()
        context = AgentContext(
            workflow_id="wf-1",
            task_id="task-1",
            agent_run_id="run-1",
            metadata={"task": "EXECUTE_PAYMENT"}
        )

        with pytest.raises(AgentPermissionDeniedError, match="strictly prohibited"):
            await agent.run(context)


class TestFinanceDatabaseRepository:
    """Database persistence for billing, invoices, payments, and ledger."""

    def test_invoice_creation_and_listing(self, db_session):
        repo = FinanceRepository(db_session)
        
        draft = InvoicingManager.create_invoice_draft(
            tenant_id="tenant-1",
            client_id="client-1",
            line_items=[{"title": "Initial Retainer", "quantity": "1.0", "unit_price": "5000.00"}],
        )

        invoice = repo.create_invoice(draft, draft["items"])
        assert invoice.id == draft["id"]
        assert invoice.total_amount == Decimal("5000.00")

        fetched = repo.get_invoice(invoice.id, "tenant-1")
        assert fetched is not None
        assert fetched.invoice_number == draft["invoice_number"]

        items = repo.get_invoice_items(invoice.id)
        assert len(items) == 1
        assert items[0].title == "Initial Retainer"

    def test_payment_and_ledger_persistence(self, db_session):
        repo = FinanceRepository(db_session)

        # Create account
        acc = repo.create_financial_account("tenant-1", {
            "account_code": "1000",
            "account_name": "Operating Checking Account",
            "account_type": "cash",
        })
        assert acc.account_code == "1000"

        # Record payment
        pay = repo.create_payment({
            "tenant_id": "tenant-1",
            "client_id": "client-1",
            "amount": Decimal("5000.00"),
            "status": "succeeded",
        })
        assert pay.status == "succeeded"
        assert pay.amount == Decimal("5000.00")
