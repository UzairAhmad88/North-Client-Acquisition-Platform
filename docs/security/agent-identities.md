# AI Agent Identity & Security Boundary

## 1. Distinct Non-Human Principal Model

AI agents in **Uzaii Develop By North's** operate as dedicated non-human principals:
- `principal_type = AGENT`
- `agent_id = research_agent` (or `qualification_agent`, `response_agent`, etc.)
- `agent_version = 1.0`

> **Security Rule**: AI agents **NEVER** impersonate human administrators, developers, or client users.

---

## 2. Hard-Prohibited Agent Permissions

Under no circumstances can an AI agent be granted autonomous authority to execute external side effects or legally binding commercial commitments:

```python
AGENT_PROHIBITED_ACTIONS = {
    "outreach.send",       # Transmitting external messages/emails
    "proposal.send",       # Submitting binding proposals to clients
    "contract.sign",       # Signing legal agreements
    "price.change",        # Altering authoritative cost/pricing baselines
    "release.approve",     # Approving production software releases
    "ai_model.promote",    # Promoting AI model weights to production
    "ai_kill_switch",      # Activating emergency platform kill switch
    "user.manage",         # Modifying user accounts or credentials
    "role.manage",         # Modifying security roles or permissions
    "tenant.manage",       # Modifying tenant isolation settings
    "api_key.manage",      # Generating API integration secrets
    "project.delete",      # Deleting project records
    "business.delete",     # Deleting CRM profiles
}
```

If an agent attempts any of these actions, the `AuthorizationEngine` immediately returns `AGENT_PROHIBITED_ACTION` and logs an alert to `security_events`.
