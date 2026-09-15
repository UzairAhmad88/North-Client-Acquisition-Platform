import html
import re


class ExtractedWebFacts:
    def __init__(
        self,
        title: str | None = None,
        meta_description: str | None = None,
        emails: list[str] | None = None,
        phones: list[str] | None = None,
        social_links: dict[str, str] | None = None,
        key_services: list[str] | None = None,
        clean_text_snippet: str | None = None,
    ):
        self.title = title
        self.meta_description = meta_description
        self.emails = emails or []
        self.phones = phones or []
        self.social_links = social_links or {}
        self.key_services = key_services or []
        self.clean_text_snippet = clean_text_snippet


class WebParser:
    @staticmethod
    def strip_html_tags(html_content: str) -> str:
        if not html_content:
            return ""
        # Remove script and style blocks
        cleaned = re.sub(
            r"<(script|style)[^>]*>.*?</\1>",
            " ",
            html_content,
            flags=re.DOTALL | re.IGNORECASE,
        )
        # Remove all HTML tags
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)
        # Unescape HTML entities & collapse spaces
        text = html.unescape(cleaned)
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def extract_title(html_content: str) -> str | None:
        match = re.search(
            r"<title[^>]*>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL
        )
        if match:
            raw_title = WebParser.strip_html_tags(match.group(1))
            return raw_title[:255] if raw_title else None
        return None

    @staticmethod
    def extract_meta_description(html_content: str) -> str | None:
        match = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
            html_content,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            raw_desc = WebParser.strip_html_tags(match.group(1))
            return raw_desc[:500] if raw_desc else None
        return None

    @staticmethod
    def extract_emails(html_content: str) -> list[str]:
        text = WebParser.strip_html_tags(html_content)
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        found = re.findall(pattern, text)
        unique_emails = []
        for e in found:
            email_lower = e.lower().strip()
            if email_lower not in unique_emails and not email_lower.endswith(
                (".png", ".jpg", ".svg", ".js")
            ):
                unique_emails.append(email_lower)
        return unique_emails[:5]

    @staticmethod
    def extract_phones(html_content: str) -> list[str]:
        text = WebParser.strip_html_tags(html_content)
        # Match standard phone number patterns with country codes or hyphen/dots
        pattern = r"\+?\b(?:\d{1,4}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b"
        matches = re.findall(pattern, text)
        unique_phones = []
        for p in matches:
            cleaned = re.sub(r"[^\d+]", "", p)
            if len(cleaned) >= 7 and cleaned not in unique_phones:
                unique_phones.append(p.strip())
        return unique_phones[:5]

    @staticmethod
    def extract_social_links(html_content: str) -> dict[str, str]:
        socials: dict[str, str] = {}
        patterns = {
            "linkedin": r"https?://(?:www\.)?linkedin\.com/(?:company|in)/[A-Za-z0-9_-]+",
            "twitter": r"https?://(?:www\.)?(?:twitter|x)\.com/[A-Za-z0-9_-]+",
            "facebook": r"https?://(?:www\.)?facebook\.com/[A-Za-z0-9_.-]+",
            "instagram": r"https?://(?:www\.)?instagram\.com/[A-Za-z0-9_.-]+",
            "youtube": r"https?://(?:www\.)?youtube\.com/(?:c/|user/|@)?[A-Za-z0-9_.-]+",
        }
        for platform, pat in patterns.items():
            match = re.search(pat, html_content, re.IGNORECASE)
            if match:
                socials[platform] = match.group(0)
        return socials

    @staticmethod
    def extract_facts(html_content: str) -> ExtractedWebFacts:
        title = WebParser.extract_title(html_content)
        meta_desc = WebParser.extract_meta_description(html_content)
        emails = WebParser.extract_emails(html_content)
        phones = WebParser.extract_phones(html_content)
        socials = WebParser.extract_social_links(html_content)
        clean_snippet = WebParser.strip_html_tags(html_content)[:1000]

        return ExtractedWebFacts(
            title=title,
            meta_description=meta_desc,
            emails=emails,
            phones=phones,
            social_links=socials,
            clean_text_snippet=clean_snippet,
        )
