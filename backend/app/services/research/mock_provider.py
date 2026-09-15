from datetime import datetime, timezone
from typing import List

from app.models.business import Business
from app.services.research.provider import ResearchEvidence, ResearchProvider


class MockResearchProvider(ResearchProvider):
    async def research(
        self,
        business: Business,
        sections: List[str],
    ) -> List[ResearchEvidence]:
        evidence_list: List[ResearchEvidence] = []
        now = datetime.now(timezone.utc)
        domain = (
            business.normalized_website
            or f"https://{business.normalized_name.replace(' ', '')}.com"
        )

        # Normalize requested sections
        req_sections = [s.upper() for s in sections] if sections else ["ALL"]
        is_all = "ALL" in req_sections

        # 1. Identity Section
        if is_all or "IDENTITY" in req_sections:
            evidence_list.append(
                ResearchEvidence(
                    field_name="business_name",
                    raw_value=business.name,
                    normalized_value=business.name,
                    research_type="IDENTITY",
                    source_url=domain,
                    source_trust="OFFICIAL",
                    confidence="HIGH",
                    evidence_text=f"Official business branding header on {domain}",
                    observed_at=now,
                )
            )

        # 2. Contact Section
        if is_all or "CONTACT" in req_sections:
            mock_phone = business.phone or "+15125550199"
            mock_email = (
                business.email
                or f"info@{domain.replace('https://', '').replace('http://', '').split('/')[0]}"
            )
            evidence_list.extend(
                [
                    ResearchEvidence(
                        field_name="phone",
                        raw_value=mock_phone,
                        normalized_value=mock_phone,
                        research_type="CONTACT",
                        source_url=f"{domain}/contact",
                        source_trust="OFFICIAL",
                        confidence="HIGH",
                        evidence_text="Verified telephone number listed on website contact page",
                        observed_at=now,
                    ),
                    ResearchEvidence(
                        field_name="email",
                        raw_value=mock_email,
                        normalized_value=mock_email,
                        research_type="CONTACT",
                        source_url=f"{domain}/contact",
                        source_trust="OFFICIAL",
                        confidence="HIGH",
                        evidence_text="Public contact inquiry email address on website",
                        observed_at=now,
                    ),
                ]
            )

        # 3. Location Section
        if is_all or "LOCATION" in req_sections:
            mock_city = business.city or "Austin"
            evidence_list.append(
                ResearchEvidence(
                    field_name="city",
                    raw_value=mock_city,
                    normalized_value=mock_city,
                    research_type="LOCATION",
                    source_url=f"{domain}/about",
                    source_trust="OFFICIAL",
                    confidence="HIGH",
                    evidence_text=f"Headquarters and service area location in {mock_city}",
                    observed_at=now,
                )
            )

        # 4. Services Section
        if is_all or "SERVICES" in req_sections:
            evidence_list.append(
                ResearchEvidence(
                    field_name="known_services",
                    raw_value="Web Development, Software Automation, AI Systems",
                    normalized_value="Web Development, Software Automation, AI Systems",
                    research_type="SERVICES",
                    source_url=f"{domain}/services",
                    source_trust="OFFICIAL",
                    confidence="HIGH",
                    evidence_text="Service catalogue offerings published on company website",
                    observed_at=now,
                )
            )

        # 5. Website & Social Presence Section
        if is_all or "WEBSITE" in req_sections or "SOCIAL" in req_sections:
            li_slug = business.normalized_name.replace(" ", "-")
            li_url = f"https://linkedin.com/company/{li_slug}"
            evidence_list.extend(
                [
                    ResearchEvidence(
                        field_name="website",
                        raw_value=domain,
                        normalized_value=domain,
                        research_type="WEBSITE",
                        source_url=domain,
                        source_trust="OFFICIAL",
                        confidence="HIGH",
                        evidence_text="Primary domain website URL",
                        observed_at=now,
                    ),
                    ResearchEvidence(
                        field_name="social_linkedin",
                        raw_value=li_url,
                        normalized_value=li_url,
                        research_type="SOCIAL",
                        source_url=li_url,
                        source_trust="HIGH_TRUST",
                        confidence="MEDIUM",
                        evidence_text="Public LinkedIn organization profile",
                        observed_at=now,
                    ),
                ]
            )

        return evidence_list
