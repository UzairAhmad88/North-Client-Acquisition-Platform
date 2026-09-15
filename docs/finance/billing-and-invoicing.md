# Billing & Invoicing Lifecycle

## 1. Invoice Lifecycles & State Transitions

```text
               ┌──────────┐
               │  DRAFT   │
               └────┬─────┘
                    │ Submit
                    ▼
           ┌─────────────────┐
           │ PENDING_APPROVAL│
           └────┬────────────┘
     Approve    │     │ Reject
   ┌────────────┘     └──────────┐
   ▼                             ▼
┌──────────┐               ┌──────────┐
│ APPROVED │               │ REJECTED │
└────┬─────┘               └──────────┘
     │ Issue (Assigns INV-YYYY-XXXX)
     ▼
┌──────────┐
│  ISSUED  │◄─────────────┐
└────┬─────┘              │
     │ Payment Collected  │ Partial Balance
     ▼                    │
┌───────────────┐         │
│PARTIALLY_PAID ├─────────┘
└────┬──────────┘
     │ Full Settlement
     ▼
┌──────────┐
│   PAID   │
└────┬─────┘
     │ Refund Issued
     ▼
┌──────────┐
│ REFUNDED │
└──────────┘
```

## 2. Milestone and Scope Linking

* Invoices are directly derived from approved contract milestones (`InvoicingManager.draft_from_contract_milestone`) or approved Change Requests (`InvoicingManager.draft_from_change_request`).
* The system enforces commercial baselines: attempts to draft an invoice exceeding approved milestones triggers exception flags.
