# Zero-Trust Architecture & Continuous Evaluation

## 1. Zero-Trust Axiom
*Never automatically trust a user, device, service, agent, application, or network location.*

## 2. Policy Decision Point (PDP) & Policy Enforcement Point (PEP)
Every sensitive request evaluates:
- **WHO**: Authenticated subject identifier and verified credential.
- **WHAT**: Target action (e.g., READ, WRITE, EXECUTE, ELEVATE).
- **WHY**: Justification or business intent.
- **FROM WHERE**: Geo-location, IP address, network zone.
- **WITH WHICH DEVICE**: Posture state (compliant, encrypted, EDR-monitored).
- **TO WHAT RESOURCE**: Target asset criticality and classification.
- **UNDER WHICH POLICY**: Active ABAC/RBAC rules.
- **WITH WHAT RISK**: Continuous entity risk score.

## 3. Decision Outcomes
- `ALLOW`: Unrestricted execution within policy.
- `ALLOW_WITH_RESTRICTIONS`: Rate-limited or masked execution.
- `STEP_UP_AUTHENTICATION`: MFA or WebAuthn FIDO2 challenge.
- `REQUIRE_APPROVAL`: Dual-authorization or supervisor sign-off.
- `DENY`: Request blocked and logged to SIEM.
- `ISOLATE`: Subject or workload quarantined.
