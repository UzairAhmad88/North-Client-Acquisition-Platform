"""Document AI summarization and key findings extraction."""

from typing import Any, Dict, List, Optional


class DocumentAISummarizer:
    """Produces structured executive summaries with citation anchors."""

    def summarize_document(
        self,
        document_id: str,
        version_number: int,
        title: str,
        content: str,
    ) -> Dict[str, Any]:
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        first_lines = lines[:5]
        summary_text = f"Executive summary for '{title}' (v{version_number}): " + " ".join(first_lines[:3])

        key_points = []
        for line in lines:
            if line.startswith("-") or line.startswith("*") or line.startswith("#"):
                clean = line.lstrip("-*# ").strip()
                if clean and len(clean) > 5:
                    key_points.append(clean)
            if len(key_points) >= 5:
                break

        if not key_points and lines:
            key_points = lines[:3]

        return {
            "document_id": document_id,
            "version_number": version_number,
            "title": title,
            "executive_summary": summary_text,
            "key_takeaways": key_points,
            "authority": "AI_INFERRED",
            "citation": f"Doc:{title} v{version_number}",
        }
