"""Proposal Section Composer creating structured client proposal sections."""

import hashlib
import json
from typing import Any, Dict, List
from agents.proposal.models import ProposalItemDraftSchema, ProposalSectionSchema


class ProposalComposer:
    """Composes professional, evidence-grounded proposal document sections."""

    @classmethod
    def compose_sections(
        cls,
        business_name: str,
        solution_data: Dict[str, Any],
        proposal_type: str = "FULL",
    ) -> List[ProposalSectionSchema]:
        features = solution_data.get("features", [])
        deliverables = solution_data.get("deliverables", [])
        assumptions = solution_data.get("assumptions", [])
        out_of_scope = solution_data.get("out_of_scope", [])
        optional_features = solution_data.get("optional_features", [])

        sections: List[ProposalSectionSchema] = []

        # 1. Cover
        sections.append(
            ProposalSectionSchema(
                title="Project Proposal & Solution Overview",
                section_type="COVER",
                content=f"Prepared for: {business_name}\nPrepared by: North's Technical Solutions Team",
            )
        )

        # 2. Executive Summary
        sections.append(
            ProposalSectionSchema(
                title="Executive Summary",
                section_type="SUMMARY",
                content=solution_data.get(
                    "overview",
                    f"North's presents a tailored technical solution for {business_name} designed to digitize business operations and drive client engagement.",
                ),
            )
        )

        # 3. Understanding of Client Needs
        sections.append(
            ProposalSectionSchema(
                title="Understanding of Client Needs",
                section_type="NEEDS",
                content=f"Based on discovery analysis, {business_name} requires a modern, reliable web application supporting core operational capabilities, scheduling, and customer management.",
            )
        )

        # 4. Proposed Solution & Features
        feat_list = "\n".join([f"- **{f.get('title')}**: {f.get('description')}" for f in features])
        sections.append(
            ProposalSectionSchema(
                title="Proposed Technical Solution",
                section_type="SOLUTION",
                content=f"Architecture Overview: {solution_data.get('architecture_summary', 'Web & REST API Architecture')}\n\nCore Modules:\n{feat_list}",
            )
        )

        # 5. Scope of Work & Deliverables
        deliv_list = "\n".join([f"- **{d.get('name')}**: {d.get('description')}" for d in deliverables])
        sections.append(
            ProposalSectionSchema(
                title="Deliverables & Scope of Work",
                section_type="DELIVERABLES",
                content=f"Deliverables Included:\n{deliv_list}",
            )
        )

        # 6. Assumptions
        assump_list = "\n".join([f"- {a.get('assumption_text')}" for a in assumptions]) if assumptions else "- Client will provide branding assets and copy content."
        sections.append(
            ProposalSectionSchema(
                title="Project Assumptions",
                section_type="ASSUMPTIONS",
                content=assump_list,
            )
        )

        # 7. Exclusions / Out of Scope
        excl_list = "\n".join([f"- {e}" for e in out_of_scope]) if out_of_scope else "- Mobile native application\n- Third-party API fees"
        sections.append(
            ProposalSectionSchema(
                title="Out of Scope",
                section_type="EXCLUSIONS",
                content=excl_list,
            )
        )

        # 8. Optional Features
        if optional_features:
            opt_list = "\n".join([f"- {opt}" for opt in optional_features])
            sections.append(
                ProposalSectionSchema(
                    title="Optional Add-On Modules",
                    section_type="OPTIONAL",
                    content=f"The following optional add-ons can be enabled upon request:\n{opt_list}",
                )
            )

        # 9. Terms
        sections.append(
            ProposalSectionSchema(
                title="Project Terms & Conditions",
                section_type="TERMS",
                content="Proposal valid for 30 days. Implementation begins upon formal agreement and kickoff confirmation.",
            )
        )

        return sections

    @classmethod
    def calculate_content_hash(cls, sections: List[ProposalSectionSchema]) -> str:
        dumped = json.dumps([s.model_dump() for s in sections], sort_keys=True)
        return hashlib.sha256(dumped.encode("utf-8")).hexdigest()
