"""Preview and thumbnail derivative generator."""

import base64
import html
from typing import Dict, Optional


class PreviewGenerator:
    """Generates sanitized visual and textual previews for documents and media."""

    def generate_preview_payload(
        self,
        filename: str,
        mime_type: str,
        data: bytes,
        extracted_text: Optional[str] = None,
    ) -> Dict[str, str]:
        """Generate safe preview representation without mutating source."""
        lower_name = filename.lower()

        # Text and Markdown
        if (
            mime_type.startswith("text/")
            or lower_name.endswith(".md")
            or lower_name.endswith(".txt")
            or lower_name.endswith(".csv")
            or lower_name.endswith(".json")
        ):
            safe_text = html.escape(extracted_text or data.decode("utf-8", errors="replace"))
            return {
                "preview_type": "text",
                "content": safe_text[:10000],
                "truncated": str(len(safe_text) > 10000),
            }

        # Images
        elif mime_type.startswith("image/"):
            b64_img = base64.b64encode(data).decode("ascii")
            return {
                "preview_type": "image",
                "content": f"data:{mime_type};base64,{b64_img}",
                "thumbnail": f"data:{mime_type};base64,{b64_img[:500]}...",
            }

        # PDF documents
        elif mime_type == "application/pdf" or lower_name.endswith(".pdf"):
            safe_snippet = html.escape((extracted_text or "PDF Document Preview")[:2000])
            return {
                "preview_type": "pdf",
                "content": safe_snippet,
                "pages_detected": "1",
            }

        # Generic binary
        return {
            "preview_type": "binary",
            "content": f"Binary file preview unavailable for {filename} ({len(data)} bytes).",
        }
