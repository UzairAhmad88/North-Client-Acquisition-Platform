"""Document version comparison and diff analysis engine."""

import difflib
from typing import Any, Dict, List, Optional


class DocumentAIComparator:
    """Performs deterministic and semantic comparison between document versions."""

    def compare_versions(
        self,
        doc_id: str,
        v1_num: int,
        v1_text: str,
        v2_num: int,
        v2_text: str,
    ) -> Dict[str, Any]:
        v1_lines = v1_text.splitlines()
        v2_lines = v2_text.splitlines()

        matcher = difflib.SequenceMatcher(None, v1_lines, v2_lines)
        similarity = matcher.ratio()

        added_lines = [line for line in v2_lines if line not in v1_lines]
        removed_lines = [line for line in v1_lines if line not in v2_lines]

        summary_diff = f"Version {v1_num} to {v2_num}: {len(added_lines)} lines added, {len(removed_lines)} lines removed. Similarity: {similarity:.1%}"

        return {
            "document_id": doc_id,
            "base_version": v1_num,
            "target_version": v2_num,
            "similarity_score": round(similarity, 3),
            "summary_diff": summary_diff,
            "lines_added_count": len(added_lines),
            "lines_removed_count": len(removed_lines),
            "added_samples": added_lines[:5],
            "removed_samples": removed_lines[:5],
            "authority": "AI_INFERRED",
        }
