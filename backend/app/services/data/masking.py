"""
Phase 65: Data Masking Service
Provides dynamic data masking: Redaction, Hashing (SHA256), Tokenization,
Partial Masking, and Synthetic Replacement.
"""

import hashlib
from typing import Dict, Any, List, Optional


class DataMaskingService:
    @staticmethod
    def mask_value(value: Any, strategy: str = "REDACT", options: Optional[Dict[str, Any]] = None) -> Any:
        if value is None:
            return None
        val_str = str(value)
        options = options or {}

        if strategy == "REDACT":
            return "[REDACTED]"
        elif strategy == "HASH":
            salt = options.get("salt", "")
            return hashlib.sha256((val_str + salt).encode("utf-8")).hexdigest()
        elif strategy == "PARTIAL":
            visible_chars = options.get("visible_chars", 4)
            if len(val_str) <= visible_chars:
                return "*" * len(val_str)
            return val_str[:visible_chars] + "*" * (len(val_str) - visible_chars)
        elif strategy == "EMAIL":
            if "@" in val_str:
                user, domain = val_str.split("@", 1)
                masked_user = user[0] + "***" if len(user) > 1 else "***"
                return f"{masked_user}@{domain}"
            return "[REDACTED_EMAIL]"
        elif strategy == "SYNTHETIC":
            synth_type = options.get("type", "generic")
            if synth_type == "name":
                return "Synthetic User"
            elif synth_type == "email":
                return "synthetic.user@example.corp"
            return "SYNTHETIC_VAL"
        return "[MASKED]"

    @staticmethod
    def mask_record(record: Dict[str, Any], column_rules: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        column_rules: {
            "email": {"strategy": "EMAIL"},
            "ssn": {"strategy": "REDACT"},
            "credit_card": {"strategy": "PARTIAL", "options": {"visible_chars": 4}}
        }
        """
        masked = dict(record)
        for col, rule in column_rules.items():
            if col in masked:
                strategy = rule.get("strategy", "REDACT")
                options = rule.get("options")
                masked[col] = DataMaskingService.mask_value(masked[col], strategy=strategy, options=options)
        return masked

    @staticmethod
    def mask_dataset(dataset: List[Dict[str, Any]], column_rules: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [DataMaskingService.mask_record(rec, column_rules) for rec in dataset]
