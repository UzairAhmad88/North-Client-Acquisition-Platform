"""Production Response & Conversation Intelligence Agent."""

import uuid
from typing import Any, Dict
from agents.core.base import BaseAgent, AgentResult
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.response.buying_signals import BuyingSignalDetector
from agents.response.draft import ResponseDraftGenerator
from agents.response.extraction import RequirementExtractor
from agents.response.intent import IntentClassifier
from agents.response.models import ResponseAnalysisResult
from agents.response.next_action import NextActionRecommender
from agents.response.objections import ObjectionClassifier


class ResponseAgent(BaseAgent):
    """
    Response & Conversation Intelligence Agent.
    Evaluates inbound messages, classifies intent, extracts requirements/objections,
    recommends next action, and generates human-reviewable response drafts.
    """

    agent_id = "response_agent"
    name = "Response Agent"
    version = "1.0"
    description = "Analyzes inbound client messages, detects intent, objections, and drafts responses."
    permissions: set[str] = {
        "READ_BUSINESS",
        "READ_LEAD",
        "READ_RESEARCH",
        "READ_AUDIT",
        "READ_SCORE",
        "READ_SERVICES",
        "READ_CONVERSATION",
        "READ_OUTREACH",
        "CREATE_DRAFT",
    }

    def get_permissions(self) -> list[AgentPermission]:
        return [AgentPermission(p) for p in self.permissions]

    async def run(self, context: AgentContext) -> AgentResult:
        latest_message = context.metadata.get("latest_message", {})
        message_body = latest_message.get("body", "")
        message_id = latest_message.get("id")

        # 1. Intent Classification
        primary_intent, all_intents, intent_confidence = IntentClassifier.classify(message_body)

        # 2. Buying Signal Detection
        buying_signal = BuyingSignalDetector.detect(message_body)

        # 3. Objection Detection
        objection = ObjectionClassifier.detect(message_body)

        # 4. Requirement Extraction & Missing Information
        extracted_reqs, missing_info = RequirementExtractor.extract(message_body, message_id)

        # 5. Next Action Recommendation
        next_action, reason, action_conf = NextActionRecommender.recommend(
            primary_intent, buying_signal, objection
        )

        # 6. Response Draft Generation
        draft_subject, draft_body = ResponseDraftGenerator.generate_draft(
            primary_intent, next_action, context.metadata
        )

        # Stage calculation
        stage = "NEW_RESPONSE"
        if primary_intent == "OPT_OUT":
            stage = "OPTED_OUT"
        elif primary_intent == "NOT_INTERESTED":
            stage = "NOT_INTERESTED"
        elif next_action == "SCHEDULE_MEETING":
            stage = "MEETING_REQUESTED"
        elif primary_intent == "REQUEST_FOR_PRICE":
            stage = "PRICING"
        elif primary_intent == "INTERESTED":
            stage = "INTERESTED"

        result_payload = ResponseAnalysisResult(
            primary_intent=primary_intent,
            all_intents=all_intents,
            intent_confidence=intent_confidence,
            buying_signal=buying_signal,
            objection=objection,
            extracted_requirements=extracted_reqs,
            missing_information=missing_info,
            conversation_stage=stage,
            recommended_next_action=next_action,
            recommended_next_action_reason=reason,
            next_action_confidence=action_conf,
            sentiment_signal="POSITIVE" if buying_signal.level != "NONE" else "NEUTRAL",
            priority="HIGH" if next_action == "SCHEDULE_MEETING" else "NORMAL",
            draft_subject=draft_subject,
            draft_body=draft_body,
        )

        return AgentResult(
            status="COMPLETED",
            result=result_payload.model_dump(),
            confidence="HIGH",
            evidence=[],
            warnings=[],
            errors=[],
            next_action={"action": next_action, "reason": reason},
            metadata={"run_id": context.agent_run_id, "agent_id": self.name},
        )


response_agent = ResponseAgent()
