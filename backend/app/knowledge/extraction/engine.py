"""
Document Intelligence & Structural Extraction Engine (Section 20-22).
Parses unstructured content, extracts named entities and factual assertions, and performs intelligent chunking.
"""

from datetime import datetime, timezone
import hashlib
import re
from typing import Any, Dict, List, Optional
import uuid

from backend.app.knowledge.base import (
    FactItem,
    KnowledgeAuthority,
    KnowledgeChunk,
    KnowledgeEntity,
    KnowledgeProvenance,
)


class DocumentIntelligenceEngine:
    """Extracts entities, facts, and structured chunks from technical and business documents."""

    def __init__(self):
        self._chunks: Dict[str, KnowledgeChunk] = {}
        self._extracted_facts: List[FactItem] = []
        self._extracted_entities: List[KnowledgeEntity] = []

    @staticmethod
    def calculate_chunk_hash(text: str) -> str:
        return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    def chunk_document(
        self,
        document_id: str,
        text_content: str,
        target_chunk_size: int = 500,
        access_scope: str = "INTERNAL",
        tenant_id: str = "default_tenant",
    ) -> List[KnowledgeChunk]:
        """
        Chunks documents along structural boundaries (headings, double newlines).
        Prevents arbitrary truncation of sentences and structural sections.
        """
        if not text_content:
            return []

        # Split along markdown headings (#, ##, ###) or paragraph breaks
        raw_sections = re.split(r"\n(?=#{1,4}\s)|\n\n+", text_content)
        chunks: List[KnowledgeChunk] = []
        chunk_idx = 0

        for section in raw_sections:
            clean_sec = section.strip()
            if not clean_sec:
                continue

            # Extract heading if present
            heading_match = re.match(r"^(#{1,4})\s+(.+)$", clean_sec, re.MULTILINE)
            heading = heading_match.group(2) if heading_match else None

            # Sub-split long sections if exceeding target size
            if len(clean_sec) > target_chunk_size * 2:
                paragraphs = clean_sec.split("\n")
                current_buf = ""
                for p in paragraphs:
                    if len(current_buf) + len(p) > target_chunk_size and current_buf:
                        chunk_code = f"CHK-{document_id}-{chunk_idx:03d}"
                        chk = KnowledgeChunk(
                            chunk_code=chunk_code,
                            document_id=document_id,
                            chunk_index=chunk_idx,
                            section_heading=heading,
                            content=current_buf.strip(),
                            content_hash=self.calculate_chunk_hash(current_buf),
                            token_estimate=len(current_buf) // 4,
                            access_scope=access_scope,
                            tenant_id=tenant_id,
                        )
                        chunks.append(chk)
                        self._chunks[chunk_code] = chk
                        chunk_idx += 1
                        current_buf = p + "\n"
                    else:
                        current_buf += p + "\n"
                if current_buf.strip():
                    chunk_code = f"CHK-{document_id}-{chunk_idx:03d}"
                    chk = KnowledgeChunk(
                        chunk_code=chunk_code,
                        document_id=document_id,
                        chunk_index=chunk_idx,
                        section_heading=heading,
                        content=current_buf.strip(),
                        content_hash=self.calculate_chunk_hash(current_buf),
                        token_estimate=len(current_buf) // 4,
                        access_scope=access_scope,
                        tenant_id=tenant_id,
                    )
                    chunks.append(chk)
                    self._chunks[chunk_code] = chk
                    chunk_idx += 1
            else:
                chunk_code = f"CHK-{document_id}-{chunk_idx:03d}"
                chk = KnowledgeChunk(
                    chunk_code=chunk_code,
                    document_id=document_id,
                    chunk_index=chunk_idx,
                    section_heading=heading,
                    content=clean_sec,
                    content_hash=self.calculate_chunk_hash(clean_sec),
                    token_estimate=len(clean_sec) // 4,
                    access_scope=access_scope,
                    tenant_id=tenant_id,
                )
                chunks.append(chk)
                self._chunks[chunk_code] = chk
                chunk_idx += 1

        return chunks

    def extract_entities_and_facts(
        self,
        text_content: str,
        source_reference: str,
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        """
        Extracts candidate entities and factual assertions with confidence scoring.
        Enforces Rule 2-3: Extracted items are marked INFERRED, never Authoritative.
        """
        entities: List[KnowledgeEntity] = []
        facts: List[FactItem] = []

        # Entity pattern matching for platform domains
        tech_patterns = re.findall(r"\b(PostgreSQL|Redis|FastAPI|Next\.js|Docker|Celery|Alembic|Stripe|WebAuthn)\b", text_content, re.IGNORECASE)
        for tech in set(tech_patterns):
            code = f"ENT-TECH-{tech.upper()}"
            entities.append(
                KnowledgeEntity(
                    entity_code=code,
                    tenant_id=tenant_id,
                    entity_type="TECHNOLOGY",
                    name=tech,
                    domain="TECHNICAL",
                    metadata_payload={"extracted_from": source_reference},
                )
            )

        client_patterns = re.findall(r"\bClient:\s*([A-Za-z0-9\s\-]+?)(?=\.|\n|$)", text_content)
        for c in client_patterns:
            clean_c = c.strip()
            if clean_c:
                code = f"ENT-CLI-{re.sub(r'[^a-zA-Z0-9]', '', clean_c).upper()}"
                entities.append(
                    KnowledgeEntity(
                        entity_code=code,
                        tenant_id=tenant_id,
                        entity_type="CLIENT",
                        name=clean_c,
                        domain="CLIENT",
                        metadata_payload={"extracted_from": source_reference},
                    )
                )

        # Factual claims extraction (requirement or capability statements)
        claim_patterns = re.findall(r"(?:must|shall|requires|supports|enforces)\s+([^.\n]+)", text_content, re.IGNORECASE)
        fact_idx = 0
        for claim in claim_patterns:
            clean_claim = claim.strip()
            if len(clean_claim) > 10:
                fact_code = f"FCT-{hashlib.md5(clean_claim.encode()).hexdigest()[:8]}"
                facts.append(
                    FactItem(
                        fact_code=fact_code,
                        tenant_id=tenant_id,
                        subject="SYSTEM_CAPABILITY",
                        predicate="REQUIREMENT",
                        target_value=clean_claim,
                        authority=KnowledgeAuthority.INFERRED,  # Extracted AI inference
                        confidence=0.82,
                        source_reference=source_reference,
                    )
                )
                fact_idx += 1

        self._extracted_entities.extend(entities)
        self._extracted_facts.extend(facts)

        return {
            "entities_found": len(entities),
            "facts_extracted": len(facts),
            "entities": entities,
            "facts": facts,
            "provenance": KnowledgeProvenance.DOCUMENT.value,
            "authority": KnowledgeAuthority.INFERRED.value,
        }

    def extract_entities(self, document_id: str, content: str, tenant_id: str = "default_tenant") -> List[KnowledgeEntity]:
        res = self.extract_entities_and_facts(content, source_reference=document_id, tenant_id=tenant_id)
        return res["entities"]

    def extract_candidate_facts(self, document_id: str, content: str, tenant_id: str = "default_tenant") -> List[FactItem]:
        res = self.extract_entities_and_facts(content, source_reference=document_id, tenant_id=tenant_id)
        return res["facts"]

    def get_chunk(self, chunk_code: str) -> Optional[KnowledgeChunk]:
        return self._chunks.get(chunk_code)
