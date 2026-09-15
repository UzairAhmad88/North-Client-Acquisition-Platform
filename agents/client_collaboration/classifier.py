"""Client request classifier engine."""

from typing import Any, Dict
from agents.client_collaboration.models import RequestClassificationResult


class ClientRequestClassifier:
    """Classifies client incoming requests into scope buckets."""

    def classify_request(self, request_id: str, title: str, description: str) -> RequestClassificationResult:
        content_lower = f"{title} {description}".lower()

        # Keywords triggering potential scope change
        scope_keywords = ["add new feature", "also build", "new page", "mobile app", "extra integration", "additional module", "new screen", "can we include"]
        bug_keywords = ["bug", "error", "broken", "issue", "crash", "fix"]
        support_keywords = ["access", "login", "password", "help", "how to"]
        content_keywords = ["logo", "text", "copy", "image", "asset", "wording"]

        if any(kw in content_lower for kw in scope_keywords):
            return RequestClassificationResult(
                request_id=request_id,
                title=title,
                classification="POTENTIAL_SCOPE_CHANGE",
                reasoning="Request specifies new feature capabilities not covered in baseline project scope.",
                confidence_score=0.92,
                is_potential_scope_change=True,
            )
        elif any(kw in content_lower for kw in bug_keywords):
            return RequestClassificationResult(
                request_id=request_id,
                title=title,
                classification="BUG",
                reasoning="Request specifies unexpected behavior or software flaw in delivered feature.",
                confidence_score=0.88,
                is_potential_scope_change=False,
            )
        elif any(kw in content_lower for kw in support_keywords):
            return RequestClassificationResult(
                request_id=request_id,
                title=title,
                classification="SUPPORT",
                reasoning="Request involves account access or general usage assistance.",
                confidence_score=0.85,
                is_potential_scope_change=False,
            )
        elif any(kw in content_lower for kw in content_keywords):
            return RequestClassificationResult(
                request_id=request_id,
                title=title,
                classification="CONTENT",
                reasoning="Request specifies client asset or copy update.",
                confidence_score=0.90,
                is_potential_scope_change=False,
            )
        else:
            return RequestClassificationResult(
                request_id=request_id,
                title=title,
                classification="IN_SCOPE",
                reasoning="Request aligns with general deliverable feedback and baseline execution.",
                confidence_score=0.80,
                is_potential_scope_change=False,
            )
