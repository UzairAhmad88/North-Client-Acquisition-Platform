"""AI Security, Prompt Injection & Sandbox Guardrails Service."""
import re
from typing import Dict, Any, List, List

class AiSecurityGuardrailsService:
    _INJECTION_PATTERNS = [
        r"ignore previous instructions",
        r"bypass security policy",
        r"reveal system prompt",
        r"override safety filters",
        r"disregard safety guidelines",
    ]

    def scan_prompt(self, prompt_text: str) -> Dict[str, Any]:
        threats = []
        for pat in self._INJECTION_PATTERNS:
            if re.search(pat, prompt_text, re.IGNORECASE):
                threats.append(pat)

        is_safe = len(threats) == 0
        return {
            "is_safe": is_safe,
            "risk_level": "CRITICAL" if not is_safe else "LOW",
            "detected_threats": threats,
            "action": "BLOCK" if not is_safe else "ALLOW",
        }

    def validate_tool_execution(self, agent_id: str, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        high_risk_tools = ["delete_database", "execute_sql_raw", "export_all_users", "rotate_root_keys"]
        is_high_risk = tool_name in high_risk_tools
        return {
            "is_allowed": True,
            "requires_human_approval": is_high_risk,
            "risk_score": 0.95 if is_high_risk else 0.1,
            "reason": "High-risk tool call requires explicit approval gate." if is_high_risk else "Tool call within standard autonomy limits.",
        }
