"""AI Security: Prompt Injection Defense & Untrusted Content Sanitizer Service."""

from typing import Dict, Any
import re

class SecurityPromptInjectionService:
    @staticmethod
    def inspect_input(payload_text: str, source_context: str = "DOCUMENT_ATTACHMENT", tenant_id: str = "tenant-default") -> Dict[str, Any]:
        text_lower = payload_text.lower()
        
        # High risk prompt injection patterns
        injection_patterns = [
            r"ignore previous instructions",
            r"system prompt override",
            r"you are now in developer mode",
            r"disregard all security policies",
            r"bypass authorization",
            r"print internal credentials",
            r"dump system environment"
        ]
        
        detected_triggers = []
        for pattern in injection_patterns:
            if re.search(pattern, text_lower):
                detected_triggers.append(pattern)
        
        if detected_triggers:
            return {
                "safe": False,
                "threat_level": "HIGH",
                "reason": "Indirect / Direct Prompt Injection Override Attack Detected",
                "matched_triggers": detected_triggers,
                "action": "BLOCKED_AND_LOGGED",
                "sanitized_text": "[SECURITY BLOCK: Malicious prompt override instruction removed]"
            }
        
        return {
            "safe": True,
            "threat_level": "NEGLIGIBLE",
            "reason": "Input passed security injection heuristic validation.",
            "matched_triggers": [],
            "action": "ALLOWED",
            "sanitized_text": payload_text
        }
