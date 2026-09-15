"""Evidence Collection and Source Hierarchy Classification."""

from typing import Any, Dict, List, Optional


SOURCE_TRUST_HIERARCHY: Dict[str, int] = {
    "OFFICIAL": 100,
    "HIGH_TRUST": 80,
    "MEDIUM_TRUST": 60,
    "LOW_TRUST": 40,
    "UNKNOWN": 20,
}


class ResearchEvidenceCollector:
    """Classifies source trust and compiles evidence items."""

    @staticmethod
    def classify_source_trust(source_url: Optional[str], business_website: Optional[str]) -> str:
        """Determine source trust level based on domain matching."""
        if not source_url:
            return "UNKNOWN"

        if business_website:
            clean_biz_web = business_website.lower().replace("https://", "").replace("http://", "").replace("www.", "").strip("/")
            clean_src_url = source_url.lower().replace("https://", "").replace("http://", "").replace("www.", "").strip("/")

            if clean_biz_web and (clean_biz_web in clean_src_url or clean_src_url in clean_biz_web):
                return "OFFICIAL"

        url_lower = source_url.lower()
        if any(official_dom in url_lower for official_dom in ["facebook.com", "instagram.com", "linkedin.com", "twitter.com"]):
            return "OFFICIAL"
        elif any(trusted_dom in url_lower for trusted_dom in ["google.com", "yelp.com", "tripadvisor.com"]):
            return "HIGH_TRUST"
        elif any(dir_dom in url_lower for dir_dom in ["yellowpages.com", "zoominfo.com"]):
            return "MEDIUM_TRUST"
        else:
            return "MEDIUM_TRUST"

    @staticmethod
    def create_evidence_item(
        field: str,
        value: Any,
        source_url: Optional[str],
        source_trust: str,
        summary: str,
    ) -> Dict[str, Any]:
        return {
            "field": field,
            "value": value,
            "source_type": source_trust,
            "source_url": source_url,
            "source_trust": source_trust,
            "summary": summary,
            "trust_rank": SOURCE_TRUST_HIERARCHY.get(source_trust, 50),
        }
