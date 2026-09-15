"""Platform Assistant Service Orchestrator."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.assistant.base import AnswerType, AssistantMessage, AssistantRole
from app.assistant.context import ContextBuilder
from app.assistant.planner import AssistantPlanner
from app.assistant.retrieval import AssistantRetriever
from app.search.service import GlobalSearchService


class PlatformAssistantService:
    """Coordinates natural-language conversations, question planning, grounded answer generation, and citations."""

    def __init__(self, search_service: Optional[GlobalSearchService] = None):
        self.search_service = search_service or GlobalSearchService()
        self.retriever = AssistantRetriever(self.search_service)
        self.planner = AssistantPlanner()
        self.context_builder = ContextBuilder()

        # In-memory session store (backed by database repo where applicable)
        self._sessions: Dict[str, List[Dict[str, Any]]] = {}

    def ask(
        self,
        question: str,
        tenant_id: str,
        user_id: str,
        session_id: Optional[str] = None,
        is_client: bool = False,
        role: str = "",
    ) -> Dict[str, Any]:
        """Process user question, retrieve authorized context, and generate grounded answer with citations."""
        sid = session_id or str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        # 1. Question Planning
        plan = self.planner.plan_question(question)

        # 2. Retrieve Authorized Records
        records = self.retriever.retrieve_context(
            query=question,
            tenant_id=tenant_id,
            user_id=user_id,
            is_client=is_client,
            role=role,
            limit=5,
        )

        # 3. Context Sanitization & Injection Defense
        context_envelope = self.context_builder.build_context_envelope(
            user_id=user_id,
            tenant_id=tenant_id,
            role=role,
            authorized_records=records,
        )

        # 4. Compose Grounded Answer
        answer_data = self.planner.compose_grounded_answer(
            question=question,
            retrieved_records=records,
            answer_type=AnswerType.FACT,
        )

        response_payload = {
            "session_id": sid,
            "question": question,
            "answer": answer_data["content"],
            "answer_type": answer_data["answer_type"],
            "sources": answer_data["sources"],
            "suggested_actions": answer_data["suggested_actions"],
            "created_at": now_iso,
            "ai_trace_id": f"trace_{uuid.uuid4().hex[:12]}",
        }

        # Store in session history
        if sid not in self._sessions:
            self._sessions[sid] = []
        self._sessions[sid].append({"role": "user", "content": question, "timestamp": now_iso})
        self._sessions[sid].append({"role": "assistant", "content": answer_data["content"], "timestamp": now_iso})

        return response_payload

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Return message turns for a conversation session."""
        return self._sessions.get(session_id, [])
