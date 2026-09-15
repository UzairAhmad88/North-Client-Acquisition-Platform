# Scope Management & Scope Expansion Detection

## 1. Scope Status Matrix (`scope_items`)

Every extracted requirement item is assigned a scope status:
- `IN_SCOPE`: Explicitly requested core features required for launch.
- `OPTIONAL`: Secondary features or Phase 2 candidates.
- `UNKNOWN`: Unclear scope items requiring clarification.
- `OUT_OF_SCOPE`: Features explicitly excluded from the current phase.

---

## 2. Scope Expansion Detection

When new high-complexity scope items (e.g. `MOBILE`, `CRM`, `INVENTORY`) are introduced into a discovery session after initial scope creation, `ScopeManager` flags:

`scope_expansion_detected: True`

This alerts the operator to scope creep without silently inflating project deliverables or binding price assumptions.
