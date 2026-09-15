from typing import Any, Dict, List, Optional

from integrations.web.audit_parser import ParsedPageData


class AuditFindingDTO:
    def __init__(
        self,
        code: str,
        category: str,
        severity: str,
        confidence: str,
        title: str,
        description: str,
        evidence: Dict[str, Any],
        affected_page: Optional[str] = None,
    ):
        self.code = code
        self.category = category
        self.severity = severity  # "INFO", "LOW", "MEDIUM", "HIGH"
        self.confidence = confidence  # "HIGH", "MEDIUM", "LOW"
        self.title = title
        self.description = description
        self.evidence = evidence
        self.affected_page = affected_page

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "category": self.category,
            "severity": self.severity,
            "confidence": self.confidence,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "affected_page": self.affected_page,
        }


class AuditAnalyzers:
    @staticmethod
    def analyze_all(
        homepage_data: Optional[ParsedPageData],
        all_pages: List[ParsedPageData],
        headers_dict: Dict[str, str],
        is_https: bool,
        redirect_to_https: bool,
        response_time_ms: int,
        business_info: Optional[Dict[str, Any]] = None,
    ) -> List[AuditFindingDTO]:
        findings: List[AuditFindingDTO] = []

        if not homepage_data or not homepage_data.url:
            findings.append(
                AuditFindingDTO(
                    code="WEBSITE_UNREACHABLE",
                    category="WEBSITE",
                    severity="HIGH",
                    confidence="HIGH",
                    title="Website was not reachable during audit",
                    description="The target website could not be accessed or returned an error during analysis.",
                    evidence={"response_time_ms": response_time_ms},
                )
            )
            return findings

        page_urls = [p.url for p in all_pages]

        # 1. WEBSITE Availability & Performance
        if response_time_ms > 3000:
            findings.append(
                AuditFindingDTO(
                    code="SLOW_HOMEPAGE_RESPONSE",
                    category="PERFORMANCE",
                    severity="MEDIUM",
                    confidence="HIGH",
                    title="Homepage initial response time is slow",
                    description=f"Homepage took {response_time_ms}ms to respond, exceeding the recommended 3000ms threshold.",
                    evidence={"response_time_ms": response_time_ms},
                    affected_page=homepage_data.url,
                )
            )

        # 2. SECURITY Analysis
        if is_https:
            findings.append(
                AuditFindingDTO(
                    code="HTTPS_ENABLED",
                    category="SECURITY",
                    severity="INFO",
                    confidence="HIGH",
                    title="HTTPS is enabled",
                    description="The website uses HTTPS for encrypted communications.",
                    evidence={"is_https": True, "redirect_to_https": redirect_to_https},
                    affected_page=homepage_data.url,
                )
            )
        else:
            findings.append(
                AuditFindingDTO(
                    code="MISSING_HTTPS",
                    category="SECURITY",
                    severity="HIGH",
                    confidence="HIGH",
                    title="HTTPS not observed",
                    description="The target URL does not enforce HTTPS encryption.",
                    evidence={"is_https": False},
                    affected_page=homepage_data.url,
                )
            )

        sec_headers = {
            "Content-Security-Policy": "content-security-policy" in headers_dict,
            "Strict-Transport-Security": "strict-transport-security" in headers_dict,
            "X-Content-Type-Options": "x-content-type-options" in headers_dict,
            "Referrer-Policy": "referrer-policy" in headers_dict,
            "Permissions-Policy": "permissions-policy" in headers_dict,
        }
        missing_sec_headers = [h for h, present in sec_headers.items() if not present]
        if missing_sec_headers:
            findings.append(
                AuditFindingDTO(
                    code="SECURITY_HEADERS_MISSING",
                    category="SECURITY",
                    severity="LOW",
                    confidence="MEDIUM",
                    title="Security headers were not observed",
                    description=f"The following security headers were not observed in the HTTP response: {', '.join(missing_sec_headers)}.",
                    evidence={"missing_headers": missing_sec_headers},
                    affected_page=homepage_data.url,
                )
            )

        # 3. SEO Analysis
        if not homepage_data.title:
            findings.append(
                AuditFindingDTO(
                    code="MISSING_TITLE_TAG",
                    category="SEO",
                    severity="HIGH",
                    confidence="HIGH",
                    title="Missing page title tag",
                    description="No <title> tag was detected on the homepage.",
                    evidence={"page": homepage_data.url},
                    affected_page=homepage_data.url,
                )
            )

        if not homepage_data.meta_description:
            findings.append(
                AuditFindingDTO(
                    code="MISSING_META_DESCRIPTION",
                    category="SEO",
                    severity="MEDIUM",
                    confidence="HIGH",
                    title="Missing meta description tag",
                    description="No meta description was detected on the homepage.",
                    evidence={"page": homepage_data.url},
                    affected_page=homepage_data.url,
                )
            )

        if not homepage_data.canonical:
            findings.append(
                AuditFindingDTO(
                    code="MISSING_CANONICAL_TAG",
                    category="SEO",
                    severity="LOW",
                    confidence="HIGH",
                    title="Missing canonical link tag",
                    description="No rel='canonical' tag was detected on the homepage.",
                    evidence={"page": homepage_data.url},
                    affected_page=homepage_data.url,
                )
            )

        if len(homepage_data.h1_list) == 0:
            findings.append(
                AuditFindingDTO(
                    code="MISSING_H1_TAG",
                    category="SEO",
                    severity="MEDIUM",
                    confidence="HIGH",
                    title="Missing H1 heading",
                    description="No <h1> heading was detected on the homepage.",
                    evidence={"page": homepage_data.url},
                    affected_page=homepage_data.url,
                )
            )
        elif len(homepage_data.h1_list) > 1:
            findings.append(
                AuditFindingDTO(
                    code="MULTIPLE_H1_TAGS",
                    category="SEO",
                    severity="LOW",
                    confidence="HIGH",
                    title="Multiple H1 headings detected",
                    description=f"Detected {len(homepage_data.h1_list)} <h1> headings on the homepage.",
                    evidence={"h1_count": len(homepage_data.h1_list), "h1_elements": homepage_data.h1_list},
                    affected_page=homepage_data.url,
                )
            )

        total_images_missing_alt = sum(p.images_missing_alt for p in all_pages)
        if total_images_missing_alt > 0:
            findings.append(
                AuditFindingDTO(
                    code="IMAGES_MISSING_ALT",
                    category="SEO",
                    severity="LOW",
                    confidence="HIGH",
                    title="Images missing ALT text attributes",
                    description=f"Detected {total_images_missing_alt} image(s) lacking descriptive alt attributes.",
                    evidence={"count": total_images_missing_alt, "analyzed_pages": len(all_pages)},
                )
            )

        # 4. MOBILE Analysis
        if homepage_data.responsive_signals:
            findings.append(
                AuditFindingDTO(
                    code="MOBILE_VIEWPORT_PRESENT",
                    category="MOBILE",
                    severity="INFO",
                    confidence="HIGH",
                    title="Mobile viewport metadata detected",
                    description="Viewport meta tag is present to configure mobile layout.",
                    evidence={"viewport": homepage_data.viewport},
                    affected_page=homepage_data.url,
                )
            )
        else:
            findings.append(
                AuditFindingDTO(
                    code="MISSING_MOBILE_VIEWPORT",
                    category="MOBILE",
                    severity="HIGH",
                    confidence="HIGH",
                    title="Mobile viewport metadata was not detected",
                    description="No viewport meta tag was observed, which may degrade mobile readability.",
                    evidence={"page": homepage_data.url},
                    affected_page=homepage_data.url,
                )
            )

        if homepage_data.fixed_width_signals:
            findings.append(
                AuditFindingDTO(
                    code="FIXED_WIDTH_LAYOUT",
                    category="MOBILE",
                    severity="MEDIUM",
                    confidence="MEDIUM",
                    title="Fixed-width layout indicators detected",
                    description="Styles or layout attributes indicate potential fixed-width container dimensions.",
                    evidence={"page": homepage_data.url},
                    affected_page=homepage_data.url,
                )
            )

        # 5. LEAD CAPTURE Analysis
        total_contact_forms = sum(p.contact_forms_count for p in all_pages)
        total_booking_forms = sum(p.booking_forms_count for p in all_pages)
        total_quote_forms = sum(p.quote_forms_count for p in all_pages)

        all_ctas: List[str] = []
        for p in all_pages:
            for cta in p.detected_ctas:
                if cta not in all_ctas:
                    all_ctas.append(cta)

        if total_contact_forms > 0:
            findings.append(
                AuditFindingDTO(
                    code="CONTACT_FORM_PRESENT",
                    category="LEAD_CAPTURE",
                    severity="INFO",
                    confidence="HIGH",
                    title="Contact form detected",
                    description=f"Visible contact form detected across analyzed pages ({total_contact_forms} form(s)).",
                    evidence={"contact_forms_count": total_contact_forms, "pages": page_urls},
                )
            )
        else:
            findings.append(
                AuditFindingDTO(
                    code="MISSING_CONTACT_FORM",
                    category="LEAD_CAPTURE",
                    severity="MEDIUM",
                    confidence="MEDIUM",
                    title="No obvious contact form detected",
                    description="No visible contact form was detected on the analyzed pages.",
                    evidence={"pages_analyzed": page_urls},
                )
            )

        if total_booking_forms > 0:
            findings.append(
                AuditFindingDTO(
                    code="BOOKING_PRESENT",
                    category="LEAD_CAPTURE",
                    severity="INFO",
                    confidence="HIGH",
                    title="Online booking mechanism detected",
                    description="Detected online appointment/booking CTA or form mechanism.",
                    evidence={"booking_forms_count": total_booking_forms},
                )
            )

        if total_quote_forms > 0:
            findings.append(
                AuditFindingDTO(
                    code="QUOTE_CTA_PRESENT",
                    category="LEAD_CAPTURE",
                    severity="INFO",
                    confidence="HIGH",
                    title="Quote request mechanism detected",
                    description="Detected quote request CTA or estimate form.",
                    evidence={"quote_forms_count": total_quote_forms},
                )
            )

        if not all_ctas and total_contact_forms == 0:
            findings.append(
                AuditFindingDTO(
                    code="NO_OBVIOUS_LEAD_CAPTURE",
                    category="LEAD_CAPTURE",
                    severity="HIGH",
                    confidence="HIGH",
                    title="No obvious lead-capture mechanisms detected",
                    description="Analyzed pages lack clear contact forms, quote requests, or prominent call-to-action buttons.",
                    evidence={"pages_analyzed": page_urls},
                )
            )

        # 6. SOCIAL Presence
        all_socials: Dict[str, str] = {}
        for p in all_pages:
            all_socials.update(p.social_links)

        if all_socials:
            findings.append(
                AuditFindingDTO(
                    code="SOCIAL_PROFILES_LINKED",
                    category="SOCIAL",
                    severity="INFO",
                    confidence="HIGH",
                    title=f"Publicly linked social profiles detected ({len(all_socials)})",
                    description=f"Public links to {', '.join(all_socials.keys())} were detected on the website.",
                    evidence={"social_links": all_socials},
                )
            )
        else:
            findings.append(
                AuditFindingDTO(
                    code="NO_SOCIAL_LINKS_DETECTED",
                    category="SOCIAL",
                    severity="LOW",
                    confidence="HIGH",
                    title="No social profile links detected",
                    description="No links to public social profiles were observed on the website.",
                    evidence={"pages_analyzed": len(all_pages)},
                )
            )

        # 7. BUSINESS INFORMATION CONSISTENCY
        all_emails: List[str] = []
        all_phones: List[str] = []
        for p in all_pages:
            for e in p.emails:
                if e not in all_emails:
                    all_emails.append(e)
            for ph in p.phones:
                if ph not in all_phones:
                    all_phones.append(ph)

        if business_info:
            res_phone = business_info.get("phone")
            res_email = business_info.get("email")

            if res_phone and all_phones and res_phone not in all_phones:
                findings.append(
                    AuditFindingDTO(
                        code="BUSINESS_INFORMATION_CONFLICT",
                        category="BUSINESS_INFORMATION",
                        severity="MEDIUM",
                        confidence="MEDIUM",
                        title="Phone number mismatch detected",
                        description=f"Research record phone ({res_phone}) differs from website detected phone numbers ({', '.join(all_phones)}).",
                        evidence={"research_phone": res_phone, "website_phones": all_phones},
                    )
                )

            if res_email and all_emails and res_email.lower() not in [e.lower() for e in all_emails]:
                findings.append(
                    AuditFindingDTO(
                        code="BUSINESS_INFORMATION_CONFLICT",
                        category="BUSINESS_INFORMATION",
                        severity="MEDIUM",
                        confidence="MEDIUM",
                        title="Email address mismatch detected",
                        description=f"Research record email ({res_email}) differs from website detected email addresses ({', '.join(all_emails)}).",
                        evidence={"research_email": res_email, "website_emails": all_emails},
                    )
                )

        # 8. CONTENT & UX
        avg_word_count = (
            sum(p.word_count for p in all_pages) // len(all_pages) if all_pages else 0
        )
        if avg_word_count < 100:
            findings.append(
                AuditFindingDTO(
                    code="THIN_CONTENT_OBSERVED",
                    category="CONTENT",
                    severity="LOW",
                    confidence="MEDIUM",
                    title="Thin textual content observed",
                    description=f"Analyzed pages average {avg_word_count} words, which may indicate limited service descriptions.",
                    evidence={"avg_word_count": avg_word_count, "pages_analyzed": len(all_pages)},
                )
            )

        return findings
