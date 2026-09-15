"""Deterministic Financial Calculator using Decimal arithmetic."""

from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional, Tuple, Union
from app.finance.base import InvoiceTotals, LineItemCalculation, TaxType

TWO_PLACES = Decimal("0.01")


def quantize_money(amount: Union[Decimal, str, int, float]) -> Decimal:
    """Quantize to 2 decimal places using standard half-up rounding."""
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))
    return amount.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)


class FinancialCalculator:
    """Pure deterministic arithmetic engine for invoices, payments, margins, and taxes."""

    @staticmethod
    def round_currency(amount: Union[Decimal, str, int, float]) -> Decimal:
        """Alias for quantize_money."""
        return quantize_money(amount)

    @staticmethod
    def calculate_line_item(
        description: str,
        quantity: Union[Decimal, float, int, str],
        unit_price: Union[Decimal, float, int, str],
        discount_amount: Union[Decimal, float, int, str] = Decimal("0.00"),
        tax_rate: Union[Decimal, float, int, str] = Decimal("0.00"),
        source_type: Optional[str] = "MANUAL",
        source_id: Optional[str] = None,
        title: Optional[str] = None,
        item_type: str = "fixed",
        reference_type: Optional[str] = None,
        reference_id: Optional[str] = None,
        contract_id: Optional[str] = None,
    ) -> LineItemCalculation:
        qty = Decimal(str(quantity))
        price = quantize_money(unit_price)
        disc = quantize_money(discount_amount)
        rate = Decimal(str(tax_rate))

        base_subtotal = quantize_money(qty * price)
        discounted_subtotal = max(Decimal("0.00"), base_subtotal - disc)
        tax_amt = quantize_money(discounted_subtotal * rate)
        item_total = quantize_money(discounted_subtotal + tax_amt)

        return LineItemCalculation(
            title=title or description,
            description=description,
            quantity=qty,
            unit_price=price,
            discount_amount=disc,
            taxable_amount=discounted_subtotal,
            tax_rate=rate,
            tax_amount=tax_amt,
            subtotal=base_subtotal,
            total_amount=item_total,
            total=item_total,
            item_type=item_type,
            reference_type=reference_type,
            reference_id=reference_id,
            contract_id=contract_id,
            source_type=source_type,
            source_id=source_id,
        )

    @classmethod
    def calculate_invoice_totals(
        cls,
        items: List[Union[LineItemCalculation, Dict[str, Any]]],
        amount_paid: Union[Decimal, float, int, str] = Decimal("0.00"),
        currency: str = "USD",
        discount_rate_pct: Union[Decimal, float, int, str] = Decimal("0.00"),
        fixed_discount_amount: Union[Decimal, float, int, str] = Decimal("0.00"),
        tax_rate_pct: Union[Decimal, float, int, str] = Decimal("0.00"),
        tax_type: TaxType = TaxType.NONE,
        tax_region: Optional[str] = None,
    ) -> InvoiceTotals:
        calc_items: List[LineItemCalculation] = []
        raw_subtotal = Decimal("0.00")

        for itm in items:
            if isinstance(itm, LineItemCalculation):
                calc_items.append(itm)
                raw_subtotal += itm.subtotal
            else:
                qty = Decimal(str(itm.get("quantity", "1.00")))
                price = quantize_money(itm.get("unit_price", "0.00"))
                line_subtotal = quantize_money(qty * price)
                raw_subtotal += line_subtotal
                calc_items.append(
                    LineItemCalculation(
                        title=itm.get("title", itm.get("description", "Item")),
                        description=itm.get("description"),
                        quantity=qty,
                        unit_price=price,
                        subtotal=line_subtotal,
                        discount_amount=Decimal("0.00"),
                        taxable_amount=line_subtotal,
                        tax_rate=Decimal("0.00"),
                        tax_amount=Decimal("0.00"),
                        total_amount=line_subtotal,
                        total=line_subtotal,
                        item_type=itm.get("item_type", "fixed"),
                        reference_type=itm.get("reference_type"),
                        reference_id=itm.get("reference_id"),
                        contract_id=itm.get("contract_id"),
                    )
                )

        raw_subtotal = quantize_money(raw_subtotal)
        d_rate = Decimal(str(discount_rate_pct))
        d_fixed = quantize_money(fixed_discount_amount)

        # Discount
        rate_discount = quantize_money(raw_subtotal * (d_rate / Decimal("100.00")))
        total_discount = min(raw_subtotal, rate_discount + d_fixed)
        taxable_amount = max(Decimal("0.00"), raw_subtotal - total_discount)

        # Tax
        t_rate = Decimal(str(tax_rate_pct))
        tax_amount = quantize_money(taxable_amount * (t_rate / Decimal("100.00")))

        total_amount = quantize_money(taxable_amount + tax_amount)
        paid = quantize_money(amount_paid)
        balance_due = max(Decimal("0.00"), total_amount - paid)

        return InvoiceTotals(
            subtotal=raw_subtotal,
            discount_amount=total_discount,
            taxable_amount=taxable_amount,
            tax_amount=tax_amount,
            total_amount=total_amount,
            amount_paid=paid,
            balance_due=balance_due,
            total_discount=total_discount,
            total_tax=tax_amount,
            amount_due=balance_due,
            currency=currency,
            items=calc_items,
        )

    @staticmethod
    def calculate_margin(
        revenue: Union[Decimal, str, int, float],
        cost: Union[Decimal, str, int, float],
    ) -> Tuple[Decimal, Decimal]:
        """Calculate gross profit contribution and margin percentage."""
        rev = quantize_money(revenue)
        c = quantize_money(cost)
        gross_profit = rev - c

        if rev > Decimal("0.00"):
            margin_pct = quantize_money((gross_profit / rev) * Decimal("100.00"))
        else:
            margin_pct = Decimal("0.00")

        return gross_profit, margin_pct

    @staticmethod
    def calculate_margin_pct(
        gross_profit: Union[Decimal, str, int, float],
        revenue: Union[Decimal, str, int, float],
    ) -> Decimal:
        """Calculate gross margin percentage."""
        rev = quantize_money(revenue)
        gp = quantize_money(gross_profit)
        if rev <= Decimal("0.00"):
            return Decimal("0.00")
        return quantize_money((gp / rev) * Decimal("100.00"))

    @staticmethod
    def calculate_variance_pct(
        actual: Union[Decimal, str, int, float],
        baseline: Union[Decimal, str, int, float],
    ) -> Decimal:
        """Calculate cost or budget variance percentage."""
        act = quantize_money(actual)
        base = quantize_money(baseline)
        if base <= Decimal("0.00"):
            return Decimal("0.00")
        diff = act - base
        return quantize_money((diff / base) * Decimal("100.00"))
