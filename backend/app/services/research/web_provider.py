from datetime import datetime, timezone
from typing import List

from integrations.web.fetcher import WebFetchError, fetch_html
from integrations.web.parser import WebParser
from integrations.web.security import SecurityValidationError

from app.models.business import Business
from app.services.research.provider import ResearchEvidence, ResearchProvider


class WebScraperResearchProvider(ResearchProvider):
    async def research(
        self,
        business: Business,
        sections: List[str],
    ) -> List[ResearchEvidence]:
        evidence_list: List[ResearchEvidence] = []
        now = datetime.now(timezone.utc)
        target_url = business.website_url or (
            f"https://{business.normalized_website}" if business.normalized_website else None
        )

        if not target_url:
            return evidence_list

        try:
            html_content = fetch_html(target_url)
            facts = WebParser.extract_facts(html_content)

            # Title / Business Identity evidence
            if facts.title:
                evidence_list.append(
                    ResearchEvidence(
                        field_name="website_title",
                        raw_value=facts.title,
                        normalized_value=facts.title,
                        research_type="IDENTITY",
                        source_url=target_url,
                        source_trust="OFFICIAL",
                        confidence="HIGH",
                        evidence_text=f"HTML page title extracted from {target_url}",
                        observed_at=now,
                    )
                )

            # Meta description / Business Description
            if facts.meta_description:
                evidence_list.append(
                    ResearchEvidence(
                        field_name="description",
                        raw_value=facts.meta_description,
                        normalized_value=facts.meta_description,
                        research_type="DESCRIPTION",
                        source_url=target_url,
                        source_trust="OFFICIAL",
                        confidence="HIGH",
                        evidence_text=f"HTML meta description from {target_url}",
                        observed_at=now,
                    )
                )

            # Emails found
            for email_val in facts.emails:
                evidence_list.append(
                    ResearchEvidence(
                        field_name="email",
                        raw_value=email_val,
                        normalized_value=email_val.lower(),
                        research_type="CONTACT",
                        source_url=target_url,
                        source_trust="OFFICIAL",
                        confidence="HIGH",
                        evidence_text=f"Email address extracted from HTML text of {target_url}",
                        observed_at=now,
                    )
                )

            # Phones found
            for phone_val in facts.phones:
                evidence_list.append(
                    ResearchEvidence(
                        field_name="phone",
                        raw_value=phone_val,
                        normalized_value=phone_val,
                        research_type="CONTACT",
                        source_url=target_url,
                        source_trust="OFFICIAL",
                        confidence="HIGH",
                        evidence_text=f"Telephone number regex match on {target_url}",
                        observed_at=now,
                    )
                )

            # Social links
            for platform, social_url in facts.social_links.items():
                evidence_list.append(
                    ResearchEvidence(
                        field_name=f"social_{platform}",
                        raw_value=social_url,
                        normalized_value=social_url,
                        research_type="SOCIAL",
                        source_url=target_url,
                        source_trust="HIGH_TRUST",
                        confidence="HIGH",
                        evidence_text=f"Link to {platform} profile found on official website",
                        observed_at=now,
                    )
                )

        except (SecurityValidationError, WebFetchError):
            # Gracefully handle fetch/security failures by returning empty or fallback records
            pass
        except Exception:
            pass

        return evidence_list
