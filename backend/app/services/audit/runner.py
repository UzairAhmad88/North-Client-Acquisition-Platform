import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from integrations.web.audit_parser import AuditParser, ParsedPageData
from integrations.web.fetcher import WebFetchError, fetch_html
from integrations.web.security import SecurityValidationError, validate_url_security

from app.models.business import Business
from app.services.audit.analyzers import AuditAnalyzers, AuditFindingDTO


class AuditExecutionResult:
    def __init__(
        self,
        status: str,  # "AVAILABLE", "UNAVAILABLE", "TIMEOUT", "REDIRECT_ERROR", "BLOCKED", "INVALID", "NO_WEBSITE"
        overall_health: str,  # "HEALTHY", "FAIR", "NEEDS_ATTENTION", "LIMITED_DATA"
        target_url: Optional[str],
        summary: str,
        categories: Dict[str, Any],
        findings: List[AuditFindingDTO],
        metrics: Dict[str, Any],
        warnings: List[str],
        errors: List[str],
        pages: List[ParsedPageData],
        started_at: datetime,
        completed_at: datetime,
    ):
        self.status = status
        self.overall_health = overall_health
        self.target_url = target_url
        self.summary = summary
        self.categories = categories
        self.findings = findings
        self.metrics = metrics
        self.warnings = warnings
        self.errors = errors
        self.pages = pages
        self.started_at = started_at
        self.completed_at = completed_at


def compute_audit_health(
    status: str, findings: List[AuditFindingDTO]
) -> str:
    if status in ("NO_WEBSITE", "UNAVAILABLE", "BLOCKED", "TIMEOUT", "INVALID"):
        return "LIMITED_DATA"

    high_count = sum(1 for f in findings if f.severity == "HIGH")
    medium_count = sum(1 for f in findings if f.severity == "MEDIUM")

    if high_count >= 1:
        return "NEEDS_ATTENTION"
    elif medium_count > 2:
        return "FAIR"
    else:
        return "HEALTHY"


class BaseAuditRunner:
    async def run_audit(
        self, business: Business, target_url: Optional[str] = None, max_pages: int = 10
    ) -> AuditExecutionResult:
        raise NotImplementedError()


class MockAuditRunner(BaseAuditRunner):
    async def run_audit(
        self, business: Business, target_url: Optional[str] = None, max_pages: int = 10
    ) -> AuditExecutionResult:
        started_at = datetime.now(timezone.utc)
        url = target_url or business.website_url or (f"https://{business.normalized_website}" if business.normalized_website else None)

        if not url:
            completed_at = datetime.now(timezone.utc)
            return AuditExecutionResult(
                status="NO_WEBSITE",
                overall_health="LIMITED_DATA",
                target_url=None,
                summary="No website was provided or researched for this business.",
                categories={"WEBSITE": "NO_WEBSITE"},
                findings=[],
                metrics={"pages_analyzed": 0},
                warnings=["No website URL provided."],
                errors=[],
                pages=[],
                started_at=started_at,
                completed_at=completed_at,
            )

        biz_name = business.name if business else "Target Business"
        biz_desc = (business.description if business else None) or "Quality services and solutions."
        biz_phone = (business.phone if business else None) or "+1-555-0199"
        biz_norm = (business.normalized_name if business else None) or "official"

        # Build mock homepage data
        mock_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{biz_name} - Official Website</title>
            <meta name="description" content="{biz_desc}">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="canonical" href="{url}">
        </head>
        <body>
            <h1>Welcome to {biz_name}</h1>
            <p>We provide modern solutions for our clients.</p>
            <form action="/contact" method="post">
                <input type="text" name="name" placeholder="Name">
                <input type="email" name="email" placeholder="Email">
                <button type="submit">Contact Us</button>
            </form>
            <a href="/about">About Us</a>
            <a href="https://facebook.com/{biz_norm}">Facebook</a>
            <a href="https://linkedin.com/company/{biz_norm}">LinkedIn</a>
            <span>Phone: {biz_phone}</span>
        </body>
        </html>
        """
        homepage_parsed = AuditParser.parse_page(url, mock_html)
        pages = [homepage_parsed]

        headers_dict = {
            "strict-transport-security": "max-age=31536000",
            "x-content-type-options": "nosniff",
        }

        biz_info = {
            "name": biz_name,
            "phone": biz_phone,
            "email": business.email if business else None,
        }

        findings = AuditAnalyzers.analyze_all(
            homepage_data=homepage_parsed,
            all_pages=pages,
            headers_dict=headers_dict,
            is_https=url.startswith("https"),
            redirect_to_https=True,
            response_time_ms=240,
            business_info=biz_info,
        )

        health = compute_audit_health("AVAILABLE", findings)
        completed_at = datetime.now(timezone.utc)

        metrics = {
            "pages_analyzed": len(pages),
            "total_response_time_ms": 240,
            "homepage_response_time_ms": 240,
            "average_response_time_ms": 240,
            "status_code": 200,
            "redirect_count": 0,
            "title_present": bool(homepage_parsed.title),
            "meta_description_present": bool(homepage_parsed.meta_description),
            "canonical_present": bool(homepage_parsed.canonical),
            "viewport_present": bool(homepage_parsed.viewport),
            "https_enabled": url.startswith("https"),
            "contact_form_detected": homepage_parsed.contact_forms_count > 0,
            "phone_detected": len(homepage_parsed.phones) > 0,
            "email_detected": len(homepage_parsed.emails) > 0,
            "address_detected": False,
            "social_links_count": len(homepage_parsed.social_links),
            "cta_count": len(homepage_parsed.detected_ctas),
            "heading_count": len(homepage_parsed.h1_list) + len(homepage_parsed.h2_list),
            "image_count": homepage_parsed.image_count,
            "images_without_alt": homepage_parsed.images_missing_alt,
        }

        return AuditExecutionResult(
            status="AVAILABLE",
            overall_health=health,
            target_url=url,
            summary=f"Mock audit completed successfully for {url}. Analyzed 1 page.",
            categories={
                "WEBSITE": "AVAILABLE",
                "SECURITY": "PASSED_BASELINE",
                "SEO": "BASELINE_VERIFIED",
                "MOBILE": "GOOD_SIGNAL",
                "LEAD_CAPTURE": "CONTACT_FORM_PRESENT",
            },
            findings=findings,
            metrics=metrics,
            warnings=[],
            errors=[],
            pages=pages,
            started_at=started_at,
            completed_at=completed_at,
        )


class RealAuditRunner(BaseAuditRunner):
    async def run_audit(
        self, business: Business, target_url: Optional[str] = None, max_pages: int = 10
    ) -> AuditExecutionResult:
        started_at = datetime.now(timezone.utc)

        # Priority target determination
        url = target_url or business.website_url or (f"https://{business.normalized_website}" if business.normalized_website else None)

        if not url:
            completed_at = datetime.now(timezone.utc)
            return AuditExecutionResult(
                status="NO_WEBSITE",
                overall_health="LIMITED_DATA",
                target_url=None,
                summary="No official or verified website was found for this business.",
                categories={"WEBSITE": "NO_WEBSITE"},
                findings=[],
                metrics={"pages_analyzed": 0},
                warnings=["No website URL provided."],
                errors=[],
                pages=[],
                started_at=started_at,
                completed_at=completed_at,
            )

        # Target Validation & SSRF check
        try:
            validated_url = validate_url_security(url)
        except SecurityValidationError as e:
            completed_at = datetime.now(timezone.utc)
            return AuditExecutionResult(
                status="BLOCKED",
                overall_health="LIMITED_DATA",
                target_url=url,
                summary=f"Audit blocked for security reasons: {str(e)}",
                categories={"WEBSITE": "BLOCKED"},
                findings=[
                    AuditFindingDTO(
                        code="SSRF_TARGET_BLOCKED",
                        category="SECURITY",
                        severity="HIGH",
                        confidence="HIGH",
                        title="Target URL blocked by security policy",
                        description=f"Target URL '{url}' resolved to a blocked internal or loopback IP range.",
                        evidence={"reason": str(e)},
                    )
                ],
                metrics={"pages_analyzed": 0},
                warnings=[str(e)],
                errors=[str(e)],
                pages=[],
                started_at=started_at,
                completed_at=completed_at,
            )

        pages: List[ParsedPageData] = []
        crawled_urls: List[str] = []
        urls_to_crawl: List[str] = [validated_url]
        headers_dict: Dict[str, str] = {}
        total_time_ms = 0

        homepage_parsed: Optional[ParsedPageData] = None

        while urls_to_crawl and len(pages) < max_pages:
            current_url = urls_to_crawl.pop(0)
            if current_url in crawled_urls:
                continue

            crawled_urls.append(current_url)
            start_fetch = time.time()

            try:
                html_body = fetch_html(current_url)
                fetch_duration_ms = int((time.time() - start_fetch) * 1000)
                total_time_ms += fetch_duration_ms

                parsed = AuditParser.parse_page(current_url, html_body)
                pages.append(parsed)

                if current_url == validated_url:
                    homepage_parsed = parsed

                # Discover new internal links
                for link in parsed.internal_links:
                    if link not in crawled_urls and link not in urls_to_crawl:
                        urls_to_crawl.append(link)

            except WebFetchError as e:
                if current_url == validated_url:
                    # Homepage fetch failed
                    completed_at = datetime.now(timezone.utc)
                    status_val = "TIMEOUT" if "timeout" in str(e).lower() else "UNAVAILABLE"
                    return AuditExecutionResult(
                        status=status_val,
                        overall_health="LIMITED_DATA",
                        target_url=validated_url,
                        summary=f"Website was not reachable during this audit: {str(e)}",
                        categories={"WEBSITE": status_val},
                        findings=[
                            AuditFindingDTO(
                                code="WEBSITE_UNREACHABLE",
                                category="WEBSITE",
                                severity="HIGH",
                                confidence="HIGH",
                                title="Website unreachable",
                                description=f"Failed to fetch content from target URL '{validated_url}': {str(e)}",
                                evidence={"error": str(e)},
                            )
                        ],
                        metrics={"pages_analyzed": 0},
                        warnings=[str(e)],
                        errors=[str(e)],
                        pages=[],
                        started_at=started_at,
                        completed_at=completed_at,
                    )

        biz_info = {
            "name": business.name,
            "phone": business.phone,
            "email": business.email,
        }

        findings = AuditAnalyzers.analyze_all(
            homepage_data=homepage_parsed,
            all_pages=pages,
            headers_dict=headers_dict,
            is_https=validated_url.startswith("https"),
            redirect_to_https=validated_url.startswith("https"),
            response_time_ms=total_time_ms // max(1, len(pages)),
            business_info=biz_info,
        )

        health = compute_audit_health("AVAILABLE", findings)
        completed_at = datetime.now(timezone.utc)

        metrics = {
            "pages_analyzed": len(pages),
            "total_response_time_ms": total_time_ms,
            "homepage_response_time_ms": total_time_ms // max(1, len(pages)),
            "average_response_time_ms": total_time_ms // max(1, len(pages)),
            "status_code": 200,
            "redirect_count": 0,
            "title_present": bool(homepage_parsed.title) if homepage_parsed else False,
            "meta_description_present": bool(homepage_parsed.meta_description) if homepage_parsed else False,
            "canonical_present": bool(homepage_parsed.canonical) if homepage_parsed else False,
            "viewport_present": bool(homepage_parsed.viewport) if homepage_parsed else False,
            "https_enabled": validated_url.startswith("https"),
            "contact_form_detected": sum(p.contact_forms_count for p in pages) > 0,
            "phone_detected": any(len(p.phones) > 0 for p in pages),
            "email_detected": any(len(p.emails) > 0 for p in pages),
            "address_detected": False,
            "social_links_count": len(set().union(*(p.social_links.keys() for p in pages))) if pages else 0,
            "cta_count": len(set().union(*(p.detected_ctas for p in pages))) if pages else 0,
            "heading_count": sum(len(p.h1_list) + len(p.h2_list) for p in pages),
            "image_count": sum(p.image_count for p in pages),
            "images_without_alt": sum(p.images_missing_alt for p in pages),
        }

        return AuditExecutionResult(
            status="AVAILABLE",
            overall_health=health,
            target_url=validated_url,
            summary=f"Audit completed for {validated_url}. Analyzed {len(pages)} page(s) and identified {len(findings)} findings.",
            categories={
                "WEBSITE": "AVAILABLE",
                "SECURITY": "ANALYZED",
                "SEO": "ANALYZED",
                "MOBILE": "ANALYZED",
                "LEAD_CAPTURE": "ANALYZED",
            },
            findings=findings,
            metrics=metrics,
            warnings=[],
            errors=[],
            pages=pages,
            started_at=started_at,
            completed_at=completed_at,
        )
