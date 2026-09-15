"""Natural-Language Question Planner and Answer Structurer."""

from typing import Any, Dict, List, Optional
from app.assistant.base import AnswerType, AssistantSource


class AssistantPlanner:
    """Plans questions, maps entities, and formats answers with provenance citations."""

    @classmethod
    def plan_question(cls, question: str) -> Dict[str, Any]:
        """Analyze question intent, required entities, and analytical scope."""
        q_lower = (question or "").lower()

        intent = "GENERAL_QUERY"
        target_entity = "ALL"

        if "lead" in q_lower:
            target_entity = "LEAD"
            intent = "LEAD_DISCOVERY"
        elif "project" in q_lower or "risk" in q_lower:
            target_entity = "PROJECT"
            intent = "PROJECT_STATUS"
        elif "proposal" in q_lower:
            target_entity = "PROPOSAL"
            intent = "PROPOSAL_LOOKUP"
        elif "requirement" in q_lower:
            target_entity = "REQUIREMENT"
            intent = "REQUIREMENTS_REVIEW"
        elif "support" in q_lower or "incident" in q_lower:
            target_entity = "SUPPORT_REQUEST"
            intent = "SUPPORT_LOOKUP"
        elif "how many" in q_lower or "rate" in q_lower or "metric" in q_lower:
            intent = "ANALYTICS_QUERY"

        return {
            "intent": intent,
            "target_entity": target_entity,
            "raw_question": question,
            "requires_analytical_metric": intent == "ANALYTICS_QUERY",
        }

    @classmethod
    def compose_grounded_answer(
        cls,
        question: str,
        retrieved_records: List[Dict[str, Any]],
        answer_type: AnswerType = AnswerType.FACT,
    ) -> Dict[str, Any]:
        """Compose answer grounded in retrieved facts with explicit source citations."""
        sources: List[AssistantSource] = []

        if not retrieved_records:
            return {
                "content": f"I couldn't find any authorized records matching '{question}'. Please try refining your query or check your filters.",
                "answer_type": AnswerType.UNKNOWN.value,
                "sources": [],
                "suggested_actions": [],
            }

        # Build grounded response summary
        lines: List[str] = [f"Found {len(retrieved_records)} relevant record(s):"]
        suggested_actions: List[Dict[str, Any]] = []

        for rec in retrieved_records[:5]:
            title = rec.get("title", "Untitled Record")
            etype = rec.get("entity_type", "RECORD")
            eid = str(rec.get("entity_id", ""))
            status = rec.get("status", "ACTIVE")

            lines.append(f"• **{title}** ({etype} · Status: `{status}`)")

            source = AssistantSource(
                entity_type=etype,
                entity_id=eid,
                title=title,
                action_url=rec.get("action_url") or f"/{etype.lower()}s/{eid}",
                snippet=rec.get("snippet", ""),
            )
            sources.append(source)

            # Suggest quick view action
            suggested_actions.append({
                "label": f"View {title}",
                "command": "NAVIGATE",
                "url": source.action_url,
            })

        return {
            "content": "\n".join(lines),
            "answer_type": answer_type.value,
            "sources": [
                {
                    "entity_type": s.entity_type,
                    "entity_id": s.entity_id,
                    "title": s.title,
                    "action_url": s.action_url,
                    "snippet": s.snippet,
                    "confidence": s.confidence,
                }
                for s in sources
            ],
            "suggested_actions": suggested_actions,
        }
