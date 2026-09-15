"""Document, File & Digital Asset AI Understanding Agent."""

from typing import Any, Dict, List, Set
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.document.classification import DocumentAIClassifier
from agents.document.comparison import DocumentAIComparator
from agents.document.extraction import DocumentAIExtractor
from agents.document.summarization import DocumentAISummarizer
from agents.document.validation import DocumentAIValidator


class DocumentAgent(BaseAgent):
    """
    Production Document & Digital Asset AI Agent.
    Assists in document summarization, classification, metadata extraction,
    requirement drafting, and version diff comparison while treating document
    content as untrusted reference data and preserving provenance.
    """

    agent_id = "document_agent"
    name = "Document Agent"
    version = "1.0"
    description = "Provides AI-assisted document classification, summarization, requirement extraction, and version diff comparison."
    permissions: Set[str] = {
        "READ_DOCUMENT",
        "READ_DOCUMENT_VERSION",
        "READ_AUTHORIZED_CONTENT",
        "CREATE_METADATA_DRAFT",
        "CREATE_SUMMARY_DRAFT",
        "CREATE_CLASSIFICATION_DRAFT",
        "CREATE_EXTRACTION_DRAFT",
        "CREATE_COMPARISON_DRAFT",
    }

    def __init__(self) -> None:
        super().__init__()
        self.extractor = DocumentAIExtractor()
        self.classifier = DocumentAIClassifier()
        self.summarizer = DocumentAISummarizer()
        self.comparator = DocumentAIComparator()
        self.validator = DocumentAIValidator()

    def get_permissions(self) -> List[AgentPermission]:
        return [AgentPermission(p) for p in self.permissions if p in AgentPermission.__members__]

    async def run(self, context: AgentContext) -> AgentResult:
        task = context.metadata.get("task", "summarize")
        doc_id = context.metadata.get("document_id", "doc-unknown")
        version_num = context.metadata.get("version_number", 1)
        filename = context.metadata.get("filename", "document.txt")
        content = context.metadata.get("content", "")

        if task == "classify":
            result_data = self.classifier.classify_document(filename, content)
        elif task == "extract_requirements":
            result_data = self.extractor.extract_structured_requirements(doc_id, version_num, content)
        elif task == "compare":
            v1_text = context.metadata.get("v1_content", "")
            v2_text = context.metadata.get("v2_content", "")
            v1_num = context.metadata.get("v1_number", 1)
            v2_num = context.metadata.get("v2_number", 2)
            result_data = self.comparator.compare_versions(doc_id, v1_num, v1_text, v2_num, v2_text)
        else:
            title = context.metadata.get("title", filename)
            result_data = self.summarizer.summarize_document(doc_id, version_num, title, content)

        is_valid = self.validator.validate_ai_output(result_data)

        return AgentResult(
            success=is_valid,
            data=result_data,
            metrics={"task": task, "content_length": len(content)},
            logs=[f"DocumentAgent executed task '{task}' successfully with AI_INFERRED authority."],
        )
