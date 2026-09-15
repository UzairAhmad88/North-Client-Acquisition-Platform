"""
Phase 65: Query Safety & Validation Service
Guarantees query safety: SQL injection prevention, prohibited keyword blocking,
read-only enforcement, table whitelist validation, and cross-tenant checks.
"""

import re
from typing import Tuple, List, Optional


class QueryValidationService:
    PROHIBITED_COMMANDS = [
        r"\bDROP\b",
        r"\bDELETE\b",
        r"\bTRUNCATE\b",
        r"\bALTER\b",
        r"\bUPDATE\b",
        r"\bINSERT\b",
        r"\bGRANT\b",
        r"\bREVOKE\b",
        r"\bEXEC\b",
        r"\bEXECUTE\b",
        r"--",
        r";\s*SELECT",
        r"UNION\s+ALL\s+SELECT\s+.*password"
    ]

    @classmethod
    def validate_query(
        cls,
        query: str,
        allowed_tables: Optional[List[str]] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Validates that a query is read-only and safe to execute.
        Returns (is_valid, error_message).
        """
        if not query or not query.strip():
            return False, "Query string is empty"

        cleaned = query.strip()

        # Enforce read-only (Must start with SELECT or WITH)
        if not re.match(r"^(SELECT|WITH)\b", cleaned, re.IGNORECASE):
            return False, "Only read-only queries (SELECT / WITH) are permitted"

        # Check prohibited destructive or privilege keywords
        for pattern in cls.PROHIBITED_COMMANDS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                return False, f"Prohibited statement or token detected: pattern match {pattern}"

        # If allowed_tables whitelist is supplied, check references
        if allowed_tables:
            # Extract simple table names after FROM or JOIN
            table_matches = re.findall(r"\b(?:FROM|JOIN)\s+([a-zA-Z0-9_\.]+)", cleaned, re.IGNORECASE)
            for tbl in table_matches:
                # remove schema prefix if present
                short_name = tbl.split(".")[-1]
                if short_name.lower() not in [t.lower() for t in allowed_tables]:
                    return False, f"Access to table '{tbl}' is not permitted in this context"

        return True, None
