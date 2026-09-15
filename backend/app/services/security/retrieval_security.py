"""RAG Retrieval Security & Authorization Filtering Service."""
from typing import List, Dict, Any

class RetrievalSecurityService:
    def filter_retrieved_documents(self, user_roles: List[str], documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        is_admin = "admin" in user_roles
        filtered = []
        for doc in documents:
            classification = doc.get("classification", "PUBLIC")
            if classification == "PUBLIC":
                filtered.append(doc)
            elif classification == "INTERNAL" and len(user_roles) > 0:
                filtered.append(doc)
            elif classification in ["CONFIDENTIAL", "RESTRICTED"] and is_admin:
                filtered.append(doc)
        return filtered
