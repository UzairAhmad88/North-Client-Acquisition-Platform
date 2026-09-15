"""Application Security & DevSecOps Gate Service."""
from typing import Dict, Any, List, List

class ApplicationSecurityService:
    def evaluate_build_security(self, sast_criticals: int, dependency_criticals: int, secrets_found: int) -> Dict[str, Any]:
        passed = (sast_criticals == 0) and (dependency_criticals == 0) and (secrets_found == 0)
        reasons = []
        if sast_criticals > 0:
            reasons.append(f"{sast_criticals} critical SAST flaws detected")
        if dependency_criticals > 0:
            reasons.append(f"{dependency_criticals} vulnerable dependencies detected")
        if secrets_found > 0:
            reasons.append(f"{secrets_found} plaintext secrets detected in repository")

        return {
            "gate_passed": passed,
            "status": "APPROVED" if passed else "BLOCKED",
            "blocking_reasons": reasons,
        }
