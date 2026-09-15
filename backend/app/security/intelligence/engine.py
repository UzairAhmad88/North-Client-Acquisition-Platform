"""
Threat Intelligence Foundation and Entity Behavioral Baselines (Sections 8.4, 31).
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

try:
    from app.security.base import (
        ThreatIndicator,
        ThreatIndicatorType,
        SecuritySeverity,
    )
except ImportError:
    from backend.app.security.base import (
        ThreatIndicator,
        ThreatIndicatorType,
        SecuritySeverity,
    )


class ThreatIntelligenceEngine:
    """
    Manages IOCs (Indicators of Compromise), reputation scoring, and expiration.
    Evaluates incoming events against known malicious indicators.
    """

    def __init__(self):
        self._indicators: Dict[str, ThreatIndicator] = {}
        self._seed_default_indicators()

    def _seed_default_indicators(self):
        """Pre-seeds standard test IOCs for malicious IPs, domains, and known scanners."""
        seeds = [
            ThreatIndicator(
                indicator_id="ioc_malicious_ip_1",
                indicator_type=ThreatIndicatorType.IP,
                indicator_value="198.51.100.42",
                threat_category="Known Botnet Node",
                severity=SecuritySeverity.CRITICAL,
                confidence=0.95,
                source="THREAT_FEED_COMMUNITY",
                reputation=95,
                observed_at=datetime.now(timezone.utc)
            ),
            ThreatIndicator(
                indicator_id="ioc_phishing_domain_1",
                indicator_type=ThreatIndicatorType.DOMAIN,
                indicator_value="evil-credential-stealer.xyz",
                threat_category="Credential Harvesting",
                severity=SecuritySeverity.HIGH,
                confidence=0.90,
                source="INTERNAL_RESEARCH",
                reputation=90,
                observed_at=datetime.now(timezone.utc)
            )
        ]
        for s in seeds:
            self._indicators[s.indicator_value] = s

    def add_indicator(self, indicator: ThreatIndicator) -> None:
        self._indicators[indicator.indicator_value] = indicator

    def lookup_indicator(self, value: str) -> Optional[ThreatIndicator]:
        ind = self._indicators.get(value)
        if ind and ind.is_active:
            if ind.expires_at and ind.expires_at < datetime.now(timezone.utc):
                ind.is_active = False
                return None
            return ind
        return None

    def list_indicators(self, tenant_id: Optional[str] = None) -> List[ThreatIndicator]:
        return list(self._indicators.values())

    # --- Behavioral Baselining (Section 8.4) ---

    def calculate_behavioral_deviation(
        self,
        current_val: float,
        baseline_mean: float,
        baseline_stddev: float
    ) -> float:
        """
        Calculates Z-score deviation from entity behavioral baseline.
        Returns deviation factor (>3.0 indicates high anomaly).
        """
        if baseline_stddev <= 0.0:
            return 0.0
        z_score = abs(current_val - baseline_mean) / baseline_stddev
        return round(z_score, 2)
