# Payments & Automated Reconciliation

## 1. Provider Integrations

* `BasePaymentProvider` defines standard interface methods: `create_payment`, `get_payment_status`, `verify_webhook_signature`, `refund_payment`.
* `MockPaymentProvider` provides deterministic local testing with in-memory transaction and idempotency key caching.

## 2. Automated Reconciliation Logic

`ReconciliationManager.match_transaction` categorizes provider transaction events:
* **Exact Match**: `provider_amount == invoice_balance_due` $\rightarrow$ Invoice updated to `PAID`, automatic settlement.
* **Partial Match**: `provider_amount < invoice_balance_due` $\rightarrow$ Invoice updated to `PARTIALLY_PAID`, remaining balance calculated.
* **Overpayment**: `provider_amount > invoice_balance_due` $\rightarrow$ Human approval required, credit note recommendation generated.
* **Missing Reference**: Transaction without valid invoice ID routed to exception queue for manual allocation.
