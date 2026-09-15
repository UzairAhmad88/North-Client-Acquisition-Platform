"""
Source Registry, Trust Ranking, and Safe Web Research Defense.
"""

import uuid
import hashlib
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse
from backend.app.services.research_intelligence.base import SourceTrustLevel


class SourceRegistryManager:
    """Manages source registration, canonical URL normalization, trust ranking, and SSRF security."""

    def __init__(self):
        self._sources: Dict[str, List[Dict[str, Any]]] = {}

    def register_source(
        self,
        workspace_id: str,
        url_or_reference: str,
        source_type: SourceTrustLevel = SourceTrustLevel.SECONDARY,
        publisher: Optional[str] = None,
        author: Optional[str] = None,
        authority_score: float = 0.75,
        freshness: str = "CURRENT",
    ) -> Dict[str, Any]:
        """Register and validate a research source with trust and provenance scores."""
        # SSRF / URL validation
        self._validate_source_url(url_or_reference)

        content_hash = hashlib.sha256(url_or_reference.encode("utf-8")).hexdigest()[:16]
        src_id = f"src_{uuid.uuid4().hex[:12]}"

        # Map trust level to reliability string
        reliability_map = {
            SourceTrustLevel.PRIMARY: "HIGH_TRUST",
            SourceTrustLevel.OFFICIAL: "OFFICIAL",
            SourceTrustLevel.GOVERNMENT: "OFFICIAL",
            SourceTrustLevel.ACADEMIC: "HIGH_TRUST",
            SourceTrustLevel.PROFESSIONAL: "HIGH_TRUST",
            SourceTrustLevel.SECONDARY: "MEDIUM_TRUST",
            SourceTrustLevel.COMMUNITY: "LOW_TRUST",
            SourceTrustLevel.UNKNOWN: "LOW_TRUST",
        }
        rel_str = reliability_map.get(source_type, "MEDIUM_TRUST")

        source = {
            "id": src_id,
            "workspace_id": workspace_id,
            "url_or_reference": url_or_reference,
            "source_type": source_type.value if hasattr(source_type, "value") else str(source_type),
            "publisher": publisher or "Web Reference",
            "author": author,
            "authority_score": max(0.1, min(1.0, authority_score)),
            "reliability": rel_str,
            "freshness": freshness,
            "content_hash": content_hash,
            "status": "VALIDATED",
        }
        self._sources.setdefault(workspace_id, []).append(source)
        return source

    def list_sources(
        self,
        workspace_id: str,
        source_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        sources = self._sources.get(workspace_id, [])
        if source_type:
            sources = [s for s in sources if s["source_type"] == source_type]
        return sources

    def _validate_source_url(self, url: str) -> None:
        """Validate URL to protect against SSRF, private IPs, and malicious schemes."""
        if not url.startswith(("http://", "https://", "ref://", "doc://")):
            raise ValueError(f"Invalid source scheme in '{url}'. Only HTTPS, HTTP, and internal REFs permitted.")

        if url.startswith(("http://", "https://")):
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            blocked_hosts = ["localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254", "internal"]
            if any(blocked in hostname.lower() for blocked in blocked_hosts) or hostname.startswith("192.168.") or hostname.startswith("10."):
                raise ValueError(f"SSRF blocked: Hostname '{hostname}' is a restricted private IP or local endpoint.")
