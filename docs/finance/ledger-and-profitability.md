# Ledger & Profitability Intelligence

## 1. Project Cost Tracking

`ProfitabilityManager.analyze_project_profitability` aggregates four cost categories:
1. **Direct Labor**: `labor_hours_logged * labor_hourly_cost_rate` (derived from effort tracking in Phase 24).
2. **AI Inference Costs**: token execution usage from Phase 33.
3. **Infrastructure & Hosting**: direct server and cloud expenses.
4. **Subcontractors & Miscellaneous**: pass-through project expenses.

## 2. Margin Variance & Health Classification

* **Estimated Margin %**: $(\text{Contracted Revenue} - \text{Estimated Cost}) / \text{Contracted Revenue} \times 100$
* **Invoiced Margin %**: $(\text{Invoiced Revenue} - \text{Actual Cost}) / \text{Invoiced Revenue} \times 100$
* **Realized Margin %**: $(\text{Collected Revenue} - \text{Actual Cost}) / \text{Collected Revenue} \times 100$
* **Health Classifications**:
  * `HIGHLY_PROFITABLE`: Realized Margin $\ge 40\%$
  * `PROFITABLE`: Realized Margin $\ge 20\%$
  * `AT_RISK`: Cost overrun $> 15\%$ or Margin $< 20\%$
  * `LOSS_MAKING`: Collected Revenue $> 0$ and Realized Margin $< 0\%$
