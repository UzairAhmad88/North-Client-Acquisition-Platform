import html
import re
from urllib.parse import urljoin, urlparse


class ParsedPageData:
    def __init__(
        self,
        url: str,
        title: str | None = None,
        meta_description: str | None = None,
        viewport: str | None = None,
        canonical: str | None = None,
        open_graph: dict[str, str] | None = None,
        h1_list: list[str] | None = None,
        h2_list: list[str] | None = None,
        h3_list: list[str] | None = None,
        image_count: int = 0,
        images_missing_alt: int = 0,
        internal_links: list[str] | None = None,
        contact_forms_count: int = 0,
        booking_forms_count: int = 0,
        quote_forms_count: int = 0,
        detected_ctas: list[str] | None = None,
        emails: list[str] | None = None,
        phones: list[str] | None = None,
        social_links: dict[str, str] | None = None,
        clean_text: str = "",
        word_count: int = 0,
        responsive_signals: bool = False,
        fixed_width_signals: bool = False,
    ):
        self.url = url
        self.title = title
        self.meta_description = meta_description
        self.viewport = viewport
        self.canonical = canonical
        self.open_graph = open_graph or {}
        self.h1_list = h1_list or []
        self.h2_list = h2_list or []
        self.h3_list = h3_list or []
        self.image_count = image_count
        self.images_missing_alt = images_missing_alt
        self.internal_links = internal_links or []
        self.contact_forms_count = contact_forms_count
        self.booking_forms_count = booking_forms_count
        self.quote_forms_count = quote_forms_count
        self.detected_ctas = detected_ctas or []
        self.emails = emails or []
        self.phones = phones or []
        self.social_links = social_links or {}
        self.clean_text = clean_text
        self.word_count = word_count
        self.responsive_signals = responsive_signals
        self.fixed_width_signals = fixed_width_signals


CTA_PATTERNS = [
    r"\bbook\b",
    r"\bbooking\b",
    r"\bcontact\b",
    r"\bcall\b",
    r"\bget quote\b",
    r"\brequest quote\b",
    r"\border\b",
    r"\breserve\b",
    r"\brequest\b",
    r"\bschedule\b",
    r"\bwhatsapp\b",
    r"\blearn more\b",
    r"\bsign up\b",
    r"\bget started\b",
]


class AuditParser:
    @staticmethod
    def strip_html(html_content: str) -> str:
        if not html_content:
            return ""
        cleaned = re.sub(
            r"<(script|style|noscript|svg)[^>]*>.*?</\1>",
            " ",
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)
        text = html.unescape(cleaned)
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def parse_page(url: str, html_content: str) -> ParsedPageData:
        if not html_content:
            return ParsedPageData(url=url)

        # 1. Title
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
        title = AuditParser.strip_html(title_match.group(1))[:255] if title_match else None

        # 2. Meta description
        desc_match = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
            html_content,
            re.IGNORECASE | re.DOTALL,
        )
        if not desc_match:
            desc_match = re.search(
                r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']',
                html_content,
                re.IGNORECASE | re.DOTALL,
            )
        meta_description = AuditParser.strip_html(desc_match.group(1))[:500] if desc_match else None

        # 3. Viewport tag
        viewport_match = re.search(
            r'<meta\s+name=["\']viewport["\']\s+content=["\'](.*?)["\']',
            html_content,
            re.IGNORECASE,
        )
        viewport = viewport_match.group(1) if viewport_match else None

        # 4. Canonical tag
        canonical_match = re.search(
            r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']',
            html_content,
            re.IGNORECASE,
        )
        canonical = canonical_match.group(1) if canonical_match else None

        # 5. Open Graph tags
        open_graph: dict[str, str] = {}
        og_matches = re.findall(
            r'<meta\s+property=["\'](og:[a-z:_-]+)["\']\s+content=["\'](.*?)["\']',
            html_content,
            re.IGNORECASE,
        )
        for prop, val in og_matches:
            open_graph[prop.lower()] = val.strip()

        # 6. Headings
        h1_raw = re.findall(r"<h1[^>]*>(.*?)</h1>", html_content, re.IGNORECASE | re.DOTALL)
        h1_list = [AuditParser.strip_html(h) for h in h1_raw if AuditParser.strip_html(h)]

        h2_raw = re.findall(r"<h2[^>]*>(.*?)</h2>", html_content, re.IGNORECASE | re.DOTALL)
        h2_list = [AuditParser.strip_html(h) for h in h2_raw if AuditParser.strip_html(h)]

        h3_raw = re.findall(r"<h3[^>]*>(.*?)3>", html_content, re.IGNORECASE | re.DOTALL)
        h3_list = [AuditParser.strip_html(h) for h in h3_raw if AuditParser.strip_html(h)]

        # 7. Images
        images = re.findall(r"<img\s+([^>]+)>", html_content, re.IGNORECASE)
        image_count = len(images)
        images_missing_alt = 0
        for img_attr in images:
            if not re.search(r'alt=["\'][^"\']+["\']', img_attr, re.IGNORECASE):
                images_missing_alt += 1

        # 8. Forms & Lead Capture
        contact_forms_count = 0
        booking_forms_count = 0
        quote_forms_count = 0

        forms = re.findall(r"<form[^>]*>(.*?)</form>", html_content, re.IGNORECASE | re.DOTALL)
        for form_html in forms:
            form_text = AuditParser.strip_html(form_html).lower()
            if any(k in form_text for k in ["booking", "appointment", "schedule", "date", "time"]):
                booking_forms_count += 1
            elif any(k in form_text for k in ["quote", "estimate", "pricing"]):
                quote_forms_count += 1
            else:
                contact_forms_count += 1

        # 9. CTAs
        detected_ctas: list[str] = []
        clean_text = AuditParser.strip_html(html_content)
        words = clean_text.split()
        word_count = len(words)

        for pat in CTA_PATTERNS:
            if re.search(pat, clean_text, re.IGNORECASE):
                match_text = pat.replace(r"\b", "").replace(r"\s+", " ").title()
                if match_text not in detected_ctas:
                    detected_ctas.append(match_text)

        # 10. Contact Info (Emails & Phones)
        email_matches = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", clean_text)
        emails = list(dict.fromkeys([e.lower() for e in email_matches if not e.lower().endswith((".png", ".jpg", ".svg", ".js"))]))[:10]

        phone_matches = re.findall(
            r"\+?\b(?:\d{1,4}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b", clean_text
        )
        phones = []
        for p in phone_matches:
            cleaned_p = re.sub(r"[^\d+]", "", p)
            if len(cleaned_p) >= 7 and p.strip() not in phones:
                phones.append(p.strip())
        phones = phones[:10]

        # 11. Social Links & WhatsApp
        socials: dict[str, str] = {}
        social_patterns = {
            "facebook": r"https?://(?:www\.)?facebook\.com/[A-Za-z0-9_.-]+",
            "instagram": r"https?://(?:www\.)?instagram\.com/[A-Za-z0-9_.-]+",
            "linkedin": r"https?://(?:www\.)?linkedin\.com/(?:company|in)/[A-Za-z0-9_-]+",
            "youtube": r"https?://(?:www\.)?youtube\.com/(?:c/|user/|@)?[A-Za-z0-9_.-]+",
            "tiktok": r"https?://(?:www\.)?tiktok\.com/@[A-Za-z0-9_.-]+",
            "twitter": r"https?://(?:www\.)?(?:twitter|x)\.com/[A-Za-z0-9_-]+",
            "whatsapp": r"https?://(?:wa\.me|api\.whatsapp\.com/send)[^\s\"'>]+",
        }
        for platform, pat in social_patterns.items():
            match = re.search(pat, html_content, re.IGNORECASE)
            if match:
                socials[platform] = match.group(0)

        # 12. Internal Links Discovery
        parsed_base = urlparse(url)
        base_domain = parsed_base.netloc.lower()

        hrefs = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        internal_links_set: set[str] = set()

        for href in hrefs:
            href_clean = href.strip()
            if (
                not href_clean
                or href_clean.startswith(("#", "javascript:", "mailto:", "tel:"))
                or any(href_clean.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".pdf", ".zip", ".exe", ".css", ".js"])
            ):
                continue

            abs_url = urljoin(url, href_clean)
            p_abs = urlparse(abs_url)
            if p_abs.scheme in ("http", "https") and p_abs.netloc.lower() == base_domain:
                # Strip query params & fragment for canonical link discovery
                norm_link = f"{p_abs.scheme}://{p_abs.netloc}{p_abs.path}".rstrip("/")
                if not norm_link:
                    norm_link = f"{p_abs.scheme}://{p_abs.netloc}/"
                internal_links_set.add(norm_link)

        # Priority path sorting for crawler: /contact, /about, /services, /book, /booking, /menu
        priority_paths = ["/contact", "/about", "/services", "/book", "/booking", "/menu"]
        sorted_links = sorted(
            internal_links_set,
            key=lambda l: (0 if any(p in l.lower() for p in priority_paths) else 1, l),
        )

        # 13. Mobile responsiveness indicators
        responsive_signals = bool(viewport) or "@media" in html_content or "meta-viewport" in html_content
        fixed_width_signals = bool(re.search(r"width:\s*\d{3,4}px", html_content, re.IGNORECASE))

        return ParsedPageData(
            url=url,
            title=title,
            meta_description=meta_description,
            viewport=viewport,
            canonical=canonical,
            open_graph=open_graph,
            h1_list=h1_list,
            h2_list=h2_list,
            h3_list=h3_list,
            image_count=image_count,
            images_missing_alt=images_missing_alt,
            internal_links=sorted_links,
            contact_forms_count=contact_forms_count,
            booking_forms_count=booking_forms_count,
            quote_forms_count=quote_forms_count,
            detected_ctas=detected_ctas,
            emails=emails,
            phones=phones,
            social_links=socials,
            clean_text=clean_text,
            word_count=word_count,
            responsive_signals=responsive_signals,
            fixed_width_signals=fixed_width_signals,
        )
