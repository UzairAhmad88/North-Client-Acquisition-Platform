# Adversarial Testing & Guardrails

## Overview
Protection against prompt injection, graph poisoning, and false entity merges.

## Architecture & Design Principles
- **Enterprise-Grade Governance**: All knowledge entities and relationships are versioned, timestamped, and auditable.
- **Zero-Trust & Least Privilege**: Every retrieval query, search request, and graph traversal verifies caller RBAC/ABAC clearance.
- **Evidence-Grounded**: Statements distinguish facts, inferences, predictions, recommendations, and unknown states with full provenance.

## Key Implementation Components
1. **Model Storage**: Isolated under `ekg_*` table prefix.
2. **Modular Services**: Coordinated through `EnterpriseKnowledgeFabricService`.
3. **Agent Integration**: Governed through 13 specialized knowledge agents inheriting Phase 76 autonomy constraints.

## Cross-Phase Synergy
- **Phase 72 (Finance)**: General ledger, invoices, budgets, and treasury telemetry.
- **Phase 73 (Trust & Compliance)**: Regulatory policies, controls, evidence, and contracts.
- **Phase 74 (Operations)**: Locations, purchase orders, shipments, and inventory.
- **Phase 75 (Decision Intelligence)**: Scenarios, simulations, digital twin forecasts, and OKRs.
- **Phase 76 (AI OS)**: Multi-agent mesh, memory fabric, tool gateway, and approval workflows.
