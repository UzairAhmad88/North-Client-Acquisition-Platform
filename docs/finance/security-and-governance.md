# Financial Security, Privacy & Governance

## 1. Multi-Tenant Boundaries & Privacy Masking

* All financial database entities enforce strict `tenant_id` query scoping.
* `FinancialAuthorizationManager.mask_client_payload` systematically strips:
  * Developer hourly rates
  * Contractor expenses
  * Internal gross margin percentages
  * Internal profit calculations
  * AI token infrastructure costs
  * Internal double-entry ledger postings

## 2. Deny-by-Default Financial Prohibitions for AI

AI agents (`FinanceAgent`) are strictly prohibited from:
* `EXECUTE_PAYMENT`
* `ISSUE_REFUND`
* `APPROVE_INVOICE`
* `APPLY_DISCOUNT`
* `CHANGE_TAX_CONFIG`
* `ALTER_LEDGER`
* `DELETE_FINANCIAL_RECORD`
* `CHANGE_FINANCIAL_POLICY`
