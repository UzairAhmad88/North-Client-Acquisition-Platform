"""
MITRE ATT&CK Framework Mapping and Categorization.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

try:
    from app.security.base import MitreTactic, AnomalyType
except ImportError:
    from backend.app.security.base import MitreTactic, AnomalyType


class MitreTechnique(BaseModel):
    technique_id: str
    name: str
    tactic: MitreTactic
    description: str
    url: Optional[str] = None


MITRE_TECHNIQUE_MAPPING: Dict[AnomalyType, MitreTechnique] = {
    AnomalyType.CREDENTIAL_STUFFING: MitreTechnique(
        technique_id="T1110.004",
        name="Brute Force: Credential Stuffing",
        tactic=MitreTactic.CREDENTIAL_ACCESS,
        description="Adversaries may use lists of compromised credentials to authenticate across services."
    ),
    AnomalyType.BRUTE_FORCE: MitreTechnique(
        technique_id="T1110.001",
        name="Brute Force: Password Guessing",
        tactic=MitreTactic.CREDENTIAL_ACCESS,
        description="Adversaries may attempt to guess passwords systematically."
    ),
    AnomalyType.IMPOSSIBLE_TRAVEL: MitreTechnique(
        technique_id="T1078.004",
        name="Valid Accounts: Cloud Accounts",
        tactic=MitreTactic.INITIAL_ACCESS,
        description="Access from impossible geographical locations within a brief time window indicating session hijacking or credential sharing."
    ),
    AnomalyType.TOKEN_LEAK: MitreTechnique(
        technique_id="T1552.001",
        name="Unsecured Credentials: Credentials in Files / Logs",
        tactic=MitreTactic.CREDENTIAL_ACCESS,
        description="Exposure of sensitive bearer tokens or secrets in headers or payloads."
    ),
    AnomalyType.DATA_EXFILTRATION: MitreTechnique(
        technique_id="T1048.003",
        name="Exfiltration Over Alternative Protocol: Exfiltration Over Web Service",
        tactic=MitreTactic.EXFILTRATION,
        description="Mass extraction or downloading of sensitive database or storage artifacts."
    ),
    AnomalyType.AGENT_PROMPT_INJECTION: MitreTechnique(
        technique_id="AML.T0054",
        name="LLM Jailbreak / Prompt Injection",
        tactic=MitreTactic.EXECUTION,
        description="Manipulating LLM prompts to bypass guardrails, execute unauthorized tools, or reveal confidential system instructions."
    ),
    AnomalyType.AGENT_TOOL_HIJACK: MitreTechnique(
        technique_id="AML.T0051",
        name="LLM Tool Hijacking",
        tactic=MitreTactic.LATERAL_MOVEMENT,
        description="Tricking an autonomous agent into invoking sensitive tools without authorization."
    ),
    AnomalyType.AGENT_RUNAWAY_SPEND: MitreTechnique(
        technique_id="AML.T0040",
        name="Resource Exhaustion / Denial of Wallet",
        tactic=MitreTactic.IMPACT,
        description="Adversarial loops or prompt loops triggering extreme token consumption and API billing spikes."
    ),
    AnomalyType.PRIVILEGE_ESCALATION: MitreTechnique(
        technique_id="T1068",
        name="Exploitation for Privilege Escalation",
        tactic=MitreTactic.PRIVILEGE_ESCALATION,
        description="Adversaries attempt to gain higher privileges than originally granted."
    ),
    AnomalyType.SENSITIVE_CONFIG_TAMPERING: MitreTechnique(
        technique_id="T1562.001",
        name="Impair Defenses: Disable or Modify Tools",
        tactic=MitreTactic.DEFENSE_EVASION,
        description="Tampering with audit configurations, tenant security policies, or guardrail parameters."
    ),
    AnomalyType.UNAUTHORIZED_RESOURCE_ACCESS: MitreTechnique(
        technique_id="T1083",
        name="File and Directory Discovery / BOLA",
        tactic=MitreTactic.DISCOVERY,
        description="Attempting to access records belonging to other tenants or restricted domains."
    ),
    AnomalyType.CROSS_TENANT_VIOLATION: MitreTechnique(
        technique_id="T1078.004",
        name="Cross-Tenant Boundary Violation",
        tactic=MitreTactic.LATERAL_MOVEMENT,
        description="Adversary attempts to access resources belonging to a different tenant domain."
    ),
    AnomalyType.API_RATE_ABUSE: MitreTechnique(
        technique_id="T1499.003",
        name="Endpoint Denial of Service: Application Exhaustion",
        tactic=MitreTactic.IMPACT,
        description="Excessive API traffic intended to overwhelm endpoints or harvest data."
    ),
    AnomalyType.API_ENUMERATION: MitreTechnique(
        technique_id="T1595.002",
        name="Active Scanning: Vulnerability / Endpoint Scanning",
        tactic=MitreTactic.DISCOVERY,
        description="Systematic probing of undocumented endpoints and object IDs."
    ),
    AnomalyType.SUSPICIOUS_SEQUENCE: MitreTechnique(
        technique_id="TA0001",
        name="Multi-Stage Attack Sequence",
        tactic=MitreTactic.LATERAL_MOVEMENT,
        description="Correlated sequence of authentication anomaly, privilege change, and exfiltration."
    ),
}


class MitreMapper:
    """Provides MITRE ATT&CK lookup and context enrichment for security anomalies."""

    @staticmethod
    def get_technique(anomaly_type: AnomalyType) -> Optional[MitreTechnique]:
        return MITRE_TECHNIQUE_MAPPING.get(anomaly_type)

    @staticmethod
    def get_tactic_for_anomaly(anomaly_type: AnomalyType) -> Optional[MitreTactic]:
        tech = MITRE_TECHNIQUE_MAPPING.get(anomaly_type)
        return tech.tactic if tech else None

    @staticmethod
    def enrich_alert_with_mitre(anomaly_dict: Dict[str, Any]) -> Dict[str, Any]:
        atype = anomaly_dict.get("anomaly_type")
        if atype:
            try:
                enum_val = AnomalyType(atype)
                tech = MitreMapper.get_technique(enum_val)
                if tech:
                    anomaly_dict["mitre_technique_id"] = tech.technique_id
                    anomaly_dict["mitre_technique_name"] = tech.name
                    anomaly_dict["mitre_tactic"] = tech.tactic.value
            except ValueError:
                pass
        return anomaly_dict
