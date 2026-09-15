# Lead Opportunity Scoring Model

## Predefined Weighted Formula (v1.0)

The Lead Opportunity Score is calculated using a deterministic 7-component weighted sum:

| Component | Weight | Description |
| :--- | :--- | :--- |
| **Website Need** | **25%** | Evaluates website presence, audit findings, security, mobile viewport, and structural gaps. |
| **Online Presence** | **15%** | Evaluates opportunity context of social profiles, research records, and discoverability. |
| **Lead Capture Opportunity** | **15%** | Evaluates gaps in contact forms, booking mechanisms, and call-to-action buttons. |
| **Automation Potential** | **20%** | Evaluates manual contact processes and workflow automation opportunities. |
| **Business Activity** | **10%** | Evaluates active CRM business status and recent research activity. |
| **Contactability** | **10%** | Evaluates availability of verified public phone numbers, email addresses, and locations. |
| **Service Fit** | **5%** | Evaluates alignment with North's Web Development, Software, and AI Automation Service Catalog. |
| **Total** | **100%** | Final Opportunity Score (0–100) |

## Formula Expression

$$\text{Opportunity Score} = 0.25 \times \text{Website Need} + 0.15 \times \text{Online Presence} + 0.15 \times \text{Lead Capture} + 0.20 \times \text{Automation Potential} + 0.10 \times \text{Business Activity} + 0.10 \times \text{Contactability} + 0.05 \times \text{Service Fit}$$
