"""Security Input Validation & AST Query Safety Service."""
import re

class SecurityInputValidationService:
    _SQL_INJECTION = [r"drop\s+table", r"union\s+select", r"insert\s+into", r"delete\s+from"]

    def is_safe_input(self, text: str) -> bool:
        for pat in self._SQL_INJECTION:
            if re.search(pat, text, re.IGNORECASE):
                return False
        return True
