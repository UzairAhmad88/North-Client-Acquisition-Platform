# Process Catalog and Hierarchies

## Hierarchy Model
The catalog organizes enterprise workflows across 7 structured levels:
1. **Enterprise**: Global corporation or business entity.
2. **Business Area**: High-level segment (e.g., Supply Chain, Global Finance, Revenue Ops).
3. **Value Stream**: End-to-end customer value delivery pipeline (e.g., Order-to-Cash, Procure-to-Pay).
4. **Process**: Cohesive sequence of activities achieving an operational milestone.
5. **Subprocess**: Decomposed component within a parent process.
6. **Activity**: Atomic functional step executed by human, AI, or software system.
7. **Task**: Fine-grained unit of work within an activity.

## Catalog Registry Attributes
- `process_id`: Unique identifier (e.g., `PROC-O2C-001`)
- `domain`: Operational domain (Finance, Logistics, Customer Care, IT)
- `criticality`: Tier 1 (Mission Critical) through Tier 4 (Non-essential)
- `automation_level`: Manual, Semi-Automated, AI-Assisted, Autonomous
- `owner`: Business and Technical owners
- `slas` & `kpis`: Target cycle time, quality yield, error tolerances\n