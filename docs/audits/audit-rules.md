# Website Audit Rules & Category Definitions

## Overview

The Website & Digital Presence Audit engine executes deterministic rules across 12 categories:

### 1. WEBSITE
- `WEBSITE_UNREACHABLE` (HIGH): Website failed to respond or returned connection error.
- `SLOW_HOMEPAGE_RESPONSE` (MEDIUM): Response time exceeds 3000ms threshold.

### 2. SECURITY
- `HTTPS_ENABLED` (INFO): Target URL uses HTTPS.
- `MISSING_HTTPS` (HIGH): Target URL does not enforce HTTPS.
- `SECURITY_HEADERS_MISSING` (LOW): One or more security headers (`CSP`, `HSTS`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`) missing.

### 3. SEO
- `MISSING_TITLE_TAG` (HIGH): Missing `<title>` element on homepage.
- `MISSING_META_DESCRIPTION` (MEDIUM): Missing meta description tag.
- `MISSING_CANONICAL_TAG` (LOW): Missing canonical URL link tag.
- `MISSING_H1_TAG` (MEDIUM): No <h1> tag detected.
- `MULTIPLE_H1_TAGS` (LOW): More than one <h1> tag detected on page.
- `IMAGES_MISSING_ALT` (LOW): Image elements missing descriptive alt attributes.

### 4. MOBILE
- `MOBILE_VIEWPORT_PRESENT` (INFO): Viewport meta tag present.
- `MISSING_MOBILE_VIEWPORT` (HIGH): No viewport meta tag present.
- `FIXED_WIDTH_LAYOUT` (MEDIUM): Fixed px width layout attributes observed.

### 5. LEAD CAPTURE
- `CONTACT_FORM_PRESENT` (INFO): Visible contact form detected.
- `MISSING_CONTACT_FORM` (MEDIUM): No visible contact form observed across analyzed pages.
- `BOOKING_PRESENT` (INFO): Online booking/appointment CTA detected.
- `QUOTE_CTA_PRESENT` (INFO): Quote request or estimate form detected.
- `NO_OBVIOUS_LEAD_CAPTURE` (HIGH): Lack of clear forms, CTAs, or contact mechanisms.

### 6. SOCIAL
- `SOCIAL_PROFILES_LINKED` (INFO): Public social profile links detected.
- `NO_SOCIAL_LINKS_DETECTED` (LOW): No public social profile links observed.

### 7. BUSINESS INFORMATION CONSISTENCY
- `BUSINESS_INFORMATION_CONFLICT` (MEDIUM): Website phone or email differs from Research/Business DB records.

### 8. CONTENT & UX
- `THIN_CONTENT_OBSERVED` (LOW): Average word count per page under 100 words.
