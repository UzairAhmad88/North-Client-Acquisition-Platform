"""Controlled Contract Section Generator."""

import hashlib
import json
from typing import Any, Dict, List
from agents.contracts.models import ContractSectionSchema


class ContractGenerator:
    """Generates structured contract sections populated from approved proposal, estimate, and solution data."""

    @classmethod
    def generate_sections(
        cls,
        contract_number: str,
        business_name: str,
        proposal_data: Dict[str, Any],
        estimate_data: Dict[str, Any],
        solution_data: Dict[str, Any],
    ) -> List[ContractSectionSchema]:
        sections: List[ContractSectionSchema] = []

        # 1. Parties
        sections.append(
            ContractSectionSchema(
                title="1. Parties to the Agreement",
                section_type="PARTIES",
                content=f"Contract Number: {contract_number}\n\nClient Party: {business_name}\nService Provider: North's Technical Solutions Team",
                order_index=1,
            )
        )

        # 2. Executive Overview
        sections.append(
            ContractSectionSchema(
                title="2. Project Overview & Objectives",
                section_type="OVERVIEW",
                content=proposal_data.get("summary", f"Technical solution implementation for {business_name}."),
                order_index=2,
            )
        )

        # 3. Scope of Work
        features = solution_data.get("features", [])
        feat_list = "\n".join([f"- **{f.get('title')}**: {f.get('description')}" for f in features])
        sections.append(
            ContractSectionSchema(
                title="3. Scope of Work & Functional Modules",
                section_type="SCOPE",
                content=f"The project encompasses the development of the following core modules:\n{feat_list}",
                order_index=3,
            )
        )

        # 4. Deliverables
        deliverables = solution_data.get("deliverables", [])
        deliv_list = "\n".join([f"- **{d.get('name')}**: {d.get('description')}" for d in deliverables])
        sections.append(
            ContractSectionSchema(
                title="4. Concrete Outcomes & Deliverables",
                section_type="DELIVERABLES",
                content=f"Concrete Deliverables:\n{deliv_list}",
                order_index=4,
            )
        )

        # 5. Exclusions
        out_of_scope = solution_data.get("out_of_scope", ["Custom Native Mobile App", "Legacy Data Migration"])
        excl_list = "\n".join([f"- {e}" for e in out_of_scope])
        sections.append(
            ContractSectionSchema(
                title="5. Exclusions & Out-of-Scope Items",
                section_type="EXCLUSIONS",
                content=excl_list,
                order_index=5,
            )
        )

        # 6. Commercial Terms & Pricing Baseline
        rec_min = estimate_data.get("recommended_min")
        rec_max = estimate_data.get("recommended_max")
        comm_text = (
            f"Approved Commercial Range Recommendation: ${rec_min} - ${rec_max} USD.\n"
            "Final binding price, payment terms, and billing milestone schedules are subject to explicit human operator confirmation."
            if rec_min and rec_max
            else "Commercial Pricing Status: PRICING_REQUIRES_HUMAN_REVIEW."
        )
        sections.append(
            ContractSectionSchema(
                title="6. Commercial Baseline & Payment Structure",
                section_type="COMMERCIAL",
                content=comm_text,
                order_index=6,
            )
        )

        # 7. Intellectual Property & Confidentiality
        sections.append(
            ContractSectionSchema(
                title="7. Intellectual Property & Data Confidentiality",
                section_type="IP",
                content="Upon full payment confirmation, Client retains ownership of custom deliverable software. North's retains ownership of pre-existing core platforms.",
                order_index=7,
            )
        )

        # 8. Signatures Section
        sections.append(
            ContractSectionSchema(
                title="8. Execution & Signatures Section",
                section_type="SIGNATURES",
                content="IN WITNESS WHEREOF, the Parties execute this agreement through authorized signatures.",
                order_index=8,
            )
        )

        return sections

    @classmethod
    def calculate_content_hash(cls, sections: List[ContractSectionSchema]) -> str:
        dumped = json.dumps([s.model_dump() for s in sections], sort_keys=True)
        return hashlib.sha256(dumped.encode("utf-8")).hexdigest()
