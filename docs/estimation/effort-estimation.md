# Effort Estimation & PERT Three-Point Model

## 1. Estimation Formula

The estimation engine uses the Program Evaluation and Review Technique (PERT) three-point estimation model to calculate expected work item hours and prevent false precision:

$$\text{Expected Hours} = \frac{\text{Optimistic} + 4 \times \text{Most Likely} + \text{Pessimistic}}{6}$$

Where:
- **Optimistic ($O$)**: Best-case scenario duration with zero unforeseen integration or environment issues.
- **Most Likely ($M$)**: Normal expected duration based on typical implementation complexity.
- **Pessimistic ($P$)**: Worst-case duration accounting for technical complexities, API issues, and rework.

---

## 2. Work Item Categories

Work items are classified across standard engineering categories:

| Category | Typical Primary Role | Description |
| :--- | :--- | :--- |
| `FRONTEND` | `FRONTEND_DEVELOPER` | Client web interface, React components, and responsive views |
| `BACKEND` | `BACKEND_DEVELOPER` | Business logic APIs, database queries, and service handlers |
| `DESIGN` | `UI_UX_DESIGNER` | Wireframes, UI design specs, and user journey flows |
| `DATABASE` | `BACKEND_DEVELOPER` | Schema migrations, data modeling, and query optimizations |
| `INTEGRATION` | `BACKEND_DEVELOPER` | Third-party API connections (Stripe, Twilio, SendGrid) |
| `AI` | `AI_ENGINEER` | LLM prompts, agent orchestration, and context vector stores |
| `TESTING` | `QA_ENGINEER` | End-to-end integration tests, edge case testing, and QA |
| `DEVOPS` | `DEVOPS_ENGINEER` | Container deployment, CI/CD pipelines, and domain SSL |
