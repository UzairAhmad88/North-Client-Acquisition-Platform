"""RBAC & ABAC Policy Authorization Service."""
from typing import List, Dict, Any, Optional, Optional

class AuthorizationService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._roles: Dict[str, List[str]] = {
            "admin": ["*"],
            "security_analyst": ["security:read", "security:triage", "alerts:investigate", "incident:update"],
            "engineer": ["code:read", "code:write", "pipeline:trigger"],
            "viewer": ["*:read"],
        }

    def check_permission(self, roles: List[str], required_permission: str) -> bool:
        for role in roles:
            perms = self._roles.get(role, [])
            if "*" in perms or required_permission in perms or any(p.endswith(":*") and required_permission.startswith(p[:-2]) for p in perms):
                return True
        return False
