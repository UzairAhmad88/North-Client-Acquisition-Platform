"""Client action item extractor engine."""

from typing import Any, Dict, List
from agents.client_collaboration.models import ExtractedClientActionSchema


class ClientActionExtractor:
    """Extracts required client input items from discussion threads."""

    def extract_action_items(self, messages: List[Dict[str, Any]]) -> List[ExtractedClientActionSchema]:
        extracted: List[ExtractedClientActionSchema] = []

        keywords = ["please provide", "need logo", "send us", "need credentials", "confirm address", "please approve", "upload document"]

        for msg in messages:
            content = str(msg.get("content") or "").lower()
            if any(kw in content for kw in keywords):
                extracted.append(
                    ExtractedClientActionSchema(
                        title=f"Client input required from message #{msg.get('id', '1')}",
                        description=msg.get("content", ""),
                        priority="HIGH",
                        due_in_days=2,
                    )
                )

        return extracted
