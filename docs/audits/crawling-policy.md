# Crawling Policy & Limits

## Bound Execution Limits

- `AUDIT_MAX_PAGES`: Default 10 max pages analyzed per audit job.
- `AUDIT_MAX_RESPONSE_BYTES`: Default 5,000,000 bytes (5 MB) per page response.
- `AUDIT_MAX_REDIRECTS`: Default 5 max redirects followed manually.
- `AUDIT_TIMEOUT_SECONDS`: Default 15 seconds request timeout.

## Page Discovery Strategy

1. Crawl homepage first (`/`).
2. Extract same-domain internal links.
3. Prioritize key paths: `/about`, `/services`, `/contact`, `/menu`, `/book`, `/booking`.
4. Ignore media files (`.png`, `.jpg`, `.pdf`, `.zip`, `.exe`, `.css`, `.js`).
