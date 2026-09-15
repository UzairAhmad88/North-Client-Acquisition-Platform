"""Database repository for Phase 40 Unified Billing, Invoicing, Payments, Ledger & Financial Operations."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
import uuid

from sqlalchemy import desc, select, update, and_
from sqlalchemy.orm import Session

from app.models.finance import (
    BillingProfileModel,
    CurrencyModel,
    TaxProfileModel,
    InvoiceModel,
    InvoiceVersionModel,
    InvoiceItemModel,
    InvoiceApprovalModel,
    BillingScheduleModel,
    BillingScheduleItemModel,
    SubscriptionModel,
    PaymentModel,
    PaymentProviderEventModel,
    PaymentReconciliationModel,
    RefundModel,
    CreditNoteModel,
    FinancialAccountModel,
    LedgerEntryModel,
    FinancialAdjustmentModel,
    ProjectCostModel,
    ExpenseModel,
)


class FinanceRepository:
    """Database operations for invoices, payments, reconciliations, ledgers, billing profiles, and project costs."""

    def __init__(self, db: Session):
        self.db = db

    # --- Billing Profiles ---

    def create_billing_profile(self, tenant_id: str, data: Dict[str, Any]) -> BillingProfileModel:
        record = BillingProfileModel(
            tenant_id=tenant_id,
            client_id=data["client_id"],
            legal_name=data["legal_name"],
            tax_id=data.get("tax_id"),
            billing_email=data["billing_email"],
            address_line1=data.get("address_line1"),
            address_line2=data.get("address_line2"),
            city=data.get("city"),
            state=data.get("state"),
            postal_code=data.get("postal_code"),
            country=data.get("country", "US"),
            default_currency=data.get("default_currency", "USD"),
            payment_terms=data.get("payment_terms", "net_30"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_billing_profile(self, profile_id: str, tenant_id: str) -> Optional[BillingProfileModel]:
        return self.db.execute(
            select(BillingProfileModel).where(
                BillingProfileModel.id == profile_id,
                BillingProfileModel.tenant_id == tenant_id,
            )
        ).scalars().first()

    def list_billing_profiles(self, tenant_id: str, client_id: Optional[str] = None) -> List[BillingProfileModel]:
        stmt = select(BillingProfileModel).where(BillingProfileModel.tenant_id == tenant_id)
        if client_id:
            stmt = stmt.where(BillingProfileModel.client_id == client_id)
        return list(self.db.execute(stmt).scalars().all())

    # --- Currencies & Taxes ---

    def list_currencies(self) -> List[CurrencyModel]:
        return list(self.db.execute(select(CurrencyModel).where(CurrencyModel.is_active == True)).scalars().all())

    def create_currency(self, data: Dict[str, Any]) -> CurrencyModel:
        record = CurrencyModel(
            code=data["code"].upper(),
            name=data["name"],
            symbol=data.get("symbol", "$"),
            decimal_places=data.get("decimal_places", 2),
            is_active=data.get("is_active", True),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_tax_profiles(self, tenant_id: str) -> List[TaxProfileModel]:
        return list(self.db.execute(select(TaxProfileModel).where(TaxProfileModel.tenant_id == tenant_id)).scalars().all())

    def create_tax_profile(self, tenant_id: str, data: Dict[str, Any]) -> TaxProfileModel:
        record = TaxProfileModel(
            tenant_id=tenant_id,
            name=data["name"],
            tax_type=data.get("tax_type", "sales_tax"),
            rate_pct=data.get("rate_pct", Decimal("0.00")),
            country=data["country"],
            state=data.get("state"),
            is_compound=data.get("is_compound", False),
            is_active=data.get("is_active", True),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    # --- Invoices ---

    def create_invoice(self, invoice_data: Dict[str, Any], items_data: List[Dict[str, Any]]) -> InvoiceModel:
        invoice = InvoiceModel(
            id=invoice_data.get("id", str(uuid.uuid4())),
            tenant_id=invoice_data["tenant_id"],
            client_id=invoice_data["client_id"],
            billing_profile_id=invoice_data.get("billing_profile_id"),
            project_id=invoice_data.get("project_id"),
            contract_id=invoice_data.get("contract_id"),
            proposal_id=invoice_data.get("proposal_id"),
            invoice_number=invoice_data["invoice_number"],
            version=invoice_data.get("version", 1),
            status=invoice_data.get("status", "draft"),
            currency=invoice_data.get("currency", "USD"),
            payment_terms=invoice_data.get("payment_terms", "net_30"),
            custom_terms_days=invoice_data.get("custom_terms_days"),
            issue_date=datetime.fromisoformat(invoice_data["issue_date"]) if invoice_data.get("issue_date") else None,
            due_date=datetime.fromisoformat(invoice_data["due_date"]) if invoice_data.get("due_date") else None,
            subtotal=Decimal(str(invoice_data["subtotal"])),
            discount_amount=Decimal(str(invoice_data["discount_amount"])),
            taxable_amount=Decimal(str(invoice_data["taxable_amount"])),
            tax_amount=Decimal(str(invoice_data["tax_amount"])),
            total_amount=Decimal(str(invoice_data["total_amount"])),
            amount_paid=Decimal(str(invoice_data.get("amount_paid", "0.00"))),
            balance_due=Decimal(str(invoice_data.get("balance_due", invoice_data["total_amount"]))),
            tax_rate_pct=Decimal(str(invoice_data.get("tax_rate_pct", "0.00"))),
            tax_type=invoice_data.get("tax_type", "none"),
            tax_region=invoice_data.get("tax_region"),
            discount_rate_pct=Decimal(str(invoice_data.get("discount_rate_pct", "0.00"))),
            fixed_discount_amount=Decimal(str(invoice_data.get("fixed_discount_amount", "0.00"))),
            notes=invoice_data.get("notes"),
            terms_and_conditions=invoice_data.get("terms_and_conditions"),
            created_by_user_id=invoice_data.get("created_by_user_id"),
        )
        self.db.add(invoice)
        self.db.flush()

        for itm in items_data:
            item_model = InvoiceItemModel(
                id=itm.get("id", str(uuid.uuid4())),
                invoice_id=invoice.id,
                title=itm["title"],
                description=itm.get("description"),
                quantity=Decimal(str(itm.get("quantity", "1.00"))),
                unit_price=Decimal(str(itm.get("unit_price", "0.00"))),
                subtotal=Decimal(str(itm.get("subtotal", "0.00"))),
                discount_amount=Decimal(str(itm.get("discount_amount", "0.00"))),
                taxable_amount=Decimal(str(itm.get("taxable_amount", "0.00"))),
                tax_amount=Decimal(str(itm.get("tax_amount", "0.00"))),
                total_amount=Decimal(str(itm.get("total_amount", "0.00"))),
                item_type=itm.get("item_type", "fixed"),
                reference_type=itm.get("reference_type"),
                reference_id=itm.get("reference_id"),
                contract_id=itm.get("contract_id"),
            )
            self.db.add(item_model)

        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def get_invoice(self, invoice_id: str, tenant_id: str) -> Optional[InvoiceModel]:
        return self.db.execute(
            select(InvoiceModel).where(
                InvoiceModel.id == invoice_id,
                InvoiceModel.tenant_id == tenant_id,
            )
        ).scalars().first()

    def get_invoice_items(self, invoice_id: str) -> List[InvoiceItemModel]:
        return list(
            self.db.execute(
                select(InvoiceItemModel).where(InvoiceItemModel.invoice_id == invoice_id)
            ).scalars().all()
        )

    def list_invoices(
        self,
        tenant_id: str,
        client_id: Optional[str] = None,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[InvoiceModel]:
        stmt = select(InvoiceModel).where(InvoiceModel.tenant_id == tenant_id)
        if client_id:
            stmt = stmt.where(InvoiceModel.client_id == client_id)
        if project_id:
            stmt = stmt.where(InvoiceModel.project_id == project_id)
        if status:
            stmt = stmt.where(InvoiceModel.status == status)
        stmt = stmt.order_by(desc(InvoiceModel.created_at)).offset(offset).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def update_invoice_status(
        self,
        invoice_id: str,
        tenant_id: str,
        new_status: str,
        amount_paid: Optional[Decimal] = None,
        balance_due: Optional[Decimal] = None,
        invoice_number: Optional[str] = None,
        issued_by_user_id: Optional[str] = None,
        approved_by_user_id: Optional[str] = None,
    ) -> Optional[InvoiceModel]:
        inv = self.get_invoice(invoice_id, tenant_id)
        if not inv:
            return None

        inv.status = new_status
        if amount_paid is not None:
            inv.amount_paid = amount_paid
        if balance_due is not None:
            inv.balance_due = balance_due
        if invoice_number:
            inv.invoice_number = invoice_number
        if issued_by_user_id:
            inv.issued_by_user_id = issued_by_user_id
            inv.issue_date = datetime.now(timezone.utc)
        if approved_by_user_id:
            inv.approved_by_user_id = approved_by_user_id

        self.db.commit()
        self.db.refresh(inv)
        return inv

    # --- Payments & Refunds ---

    def create_payment(self, payment_data: Dict[str, Any]) -> PaymentModel:
        record = PaymentModel(
            id=payment_data.get("id", str(uuid.uuid4())),
            tenant_id=payment_data["tenant_id"],
            invoice_id=payment_data.get("invoice_id"),
            client_id=payment_data.get("client_id", "client_unknown"),
            provider_type=payment_data.get("provider_type", "mock"),
            provider_payment_id=payment_data.get("provider_payment_id"),
            amount=Decimal(str(payment_data["amount"])),
            currency=payment_data.get("currency", "USD"),
            status=payment_data.get("status", "succeeded"),
            payment_method=payment_data.get("payment_method", "credit_card"),
            fee_amount=Decimal(str(payment_data.get("fee_amount", "0.00"))),
            error_code=payment_data.get("error_code"),
            error_message=payment_data.get("error_message"),
            raw_response=payment_data.get("raw_response"),
            idempotency_key=payment_data.get("idempotency_key"),
            created_by_user_id=payment_data.get("created_by_user_id"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_payments(self, tenant_id: str, invoice_id: Optional[str] = None, client_id: Optional[str] = None) -> List[PaymentModel]:
        stmt = select(PaymentModel).where(PaymentModel.tenant_id == tenant_id)
        if invoice_id:
            stmt = stmt.where(PaymentModel.invoice_id == invoice_id)
        if client_id:
            stmt = stmt.where(PaymentModel.client_id == client_id)
        stmt = stmt.order_by(desc(PaymentModel.created_at))
        return list(self.db.execute(stmt).scalars().all())

    def create_refund(self, refund_data: Dict[str, Any]) -> RefundModel:
        record = RefundModel(
            id=refund_data.get("id", str(uuid.uuid4())),
            tenant_id=refund_data["tenant_id"],
            payment_id=refund_data["payment_id"],
            invoice_id=refund_data.get("invoice_id"),
            provider_refund_id=refund_data.get("provider_refund_id"),
            amount=Decimal(str(refund_data["amount"])),
            currency=refund_data.get("currency", "USD"),
            status=refund_data.get("status", "succeeded"),
            reason=refund_data.get("reason"),
            error_code=refund_data.get("error_code"),
            error_message=refund_data.get("error_message"),
            created_by_user_id=refund_data.get("created_by_user_id"),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    # --- Financial Accounts & Ledger ---

    def create_financial_account(self, tenant_id: str, data: Dict[str, Any]) -> FinancialAccountModel:
        record = FinancialAccountModel(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            account_code=data["account_code"],
            account_name=data["account_name"],
            account_type=data["account_type"],
            currency=data.get("currency", "USD"),
            is_active=data.get("is_active", True),
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_financial_accounts(self, tenant_id: str) -> List[FinancialAccountModel]:
        return list(self.db.execute(select(FinancialAccountModel).where(FinancialAccountModel.tenant_id == tenant_id)).scalars().all())

    def create_ledger_entries(self, entries_list: List[Dict[str, Any]]) -> List[LedgerEntryModel]:
        created = []
        for e in entries_list:
            record = LedgerEntryModel(
                id=e.get("id", str(uuid.uuid4())),
                tenant_id=e["tenant_id"],
                entry_group_id=e["entry_group_id"],
                account_id=e["account_id"],
                account_type=e.get("account_type"),
                direction=e["direction"],
                amount=Decimal(str(e["amount"])),
                currency=e.get("currency", "USD"),
                reference_type=e.get("reference_type"),
                reference_id=e.get("reference_id"),
                description=e.get("description"),
                is_reversed=e.get("is_reversed", False),
                reversing_entry_id=e.get("reversing_entry_id"),
                created_by_user_id=e.get("created_by_user_id"),
                posted_at=datetime.fromisoformat(e["posted_at"]) if isinstance(e.get("posted_at"), str) else (e.get("posted_at") or datetime.now(timezone.utc)),
            )
            self.db.add(record)
            created.append(record)
        self.db.commit()
        return created

    def list_ledger_entries(self, tenant_id: str, account_id: Optional[str] = None, limit: int = 100) -> List[LedgerEntryModel]:
        stmt = select(LedgerEntryModel).where(LedgerEntryModel.tenant_id == tenant_id)
        if account_id:
            stmt = stmt.where(LedgerEntryModel.account_id == account_id)
        stmt = stmt.order_by(desc(LedgerEntryModel.posted_at)).limit(limit)
        return list(self.db.execute(stmt).scalars().all())
