"""
Customer Feedback Intake, Sentiment Analysis, Classification, and Intelligence Clustering.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.product_management.base import FeedbackType


class FeedbackIntelligenceManager:
    """Manages raw feedback intake, categorization, and AI-assisted theme clustering."""

    def __init__(self):
        self._feedback: Dict[str, List[Dict[str, Any]]] = {}

    def record_feedback(
        self,
        product_id: str,
        raw_text: Optional[str] = None,
        source: str = "CLIENT",
        feedback_type: Any = FeedbackType.FEATURE_REQUEST,
        customer_segment: Optional[str] = None,
        revenue_impact_usd: float = 0.0,
        severity: str = "MEDIUM",
        sentiment_score: Optional[float] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Record customer or internal feedback item."""
        fb_id = f"fb_{uuid.uuid4().hex[:12]}"
        text = raw_text or kwargs.get("content", "Customer feedback observation")

        # Deterministic sentiment heuristic if not provided
        if sentiment_score is None:
            lower = text.lower()
            if any(w in lower for w in ["love", "great", "excellent", "fast", "helpful"]):
                sentiment = 0.8
            elif any(w in lower for w in ["slow", "bug", "broken", "fail", "bad", "confusing", "lost"]):
                sentiment = -0.6
            else:
                sentiment = 0.1
        else:
            sentiment = sentiment_score

        ftype = feedback_type.value if hasattr(feedback_type, "value") else str(feedback_type)
        fb = {
            "id": fb_id,
            "product_id": product_id,
            "source": source,
            "feedback_type": ftype,
            "raw_text": text,
            "content": text,
            "customer_segment": customer_segment or kwargs.get("customer_segment", "Mid-Market"),
            "revenue_impact_usd": revenue_impact_usd or kwargs.get("revenue_impact_usd", 0.0),
            "sentiment_score": sentiment,
            "theme_cluster": self._assign_theme(text),
            "severity": severity,
            "status": "NEW",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._feedback.setdefault(product_id, []).append(fb)
        return fb

    def ingest_feedback(self, *args, **kwargs) -> Dict[str, Any]:
        """Alias for record_feedback."""
        return self.record_feedback(*args, **kwargs)

    def _assign_theme(self, text: str) -> str:
        """Heuristic theme clustering based on key phrases."""
        lower = text.lower()
        if "speed" in lower or "slow" in lower or "latency" in lower or "load" in lower:
            return "Performance & Latency"
        elif "integrat" in lower or "api" in lower or "webhook" in lower or "crm" in lower:
            return "Integrations & Ecosystem"
        elif "ui" in lower or "ux" in lower or "design" in lower or "confusing" in lower:
            return "Usability & Workflow Experience"
        elif "price" in lower or "cost" in lower or "plan" in lower:
            return "Pricing & Packaging"
        elif "ai" in lower or "prompt" in lower or "model" in lower or "accuracy" in lower:
            return "AI Quality & Accuracy"
        return "General Usability"

    def list_feedback(
        self,
        product_id: str,
        feedback_type: Optional[str] = None,
        theme: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        items = self._feedback.get(product_id, [])
        if feedback_type:
            items = [i for i in items if i["feedback_type"] == feedback_type]
        if theme:
            items = [i for i in items if i["theme_cluster"] == theme]
        return items

    def cluster_feedback_themes(self, product_id: str) -> List[Dict[str, Any]]:
        """Synthesize feedback items into ranked thematic intelligence clusters."""
        items = self._feedback.get(product_id, [])
        if not items:
            return []

        clusters: Dict[str, List[Dict[str, Any]]] = {}
        for item in items:
            t = item.get("theme_cluster", "General")
            clusters.setdefault(t, []).append(item)

        results = []
        total_items = max(len(items), 1)

        for theme_name, theme_items in clusters.items():
            freq_pct = round((len(theme_items) / total_items) * 100, 1)
            avg_sentiment = round(sum(i["sentiment_score"] for i in theme_items) / len(theme_items), 2)
            tot_revenue = sum(i.get("revenue_impact_usd", 0.0) for i in theme_items)
            critical_count = sum(1 for i in theme_items if i.get("severity") in ["HIGH", "CRITICAL"])

            results.append({
                "theme": theme_name,
                "item_count": len(theme_items),
                "frequency": len(theme_items),
                "frequency_percentage": freq_pct,
                "average_sentiment": avg_sentiment,
                "sentiment_avg": avg_sentiment,
                "total_revenue_impact_usd": tot_revenue,
                "revenue_impact_total": tot_revenue,
                "critical_severity_count": critical_count,
                "urgency_level": "HIGH" if critical_count > 0 else "MEDIUM",
                "sample_quotes": [i["raw_text"] for i in theme_items[:3]],
                "confidence": 0.91,
            })

        # Sort by critical items and frequency
        results.sort(key=lambda x: (x["critical_severity_count"], x["item_count"]), reverse=True)
        return results

    def cluster_feedback_into_themes(self, product_id: str) -> List[Dict[str, Any]]:
        """Alias for cluster_feedback_themes."""
        return self.cluster_feedback_themes(product_id)
