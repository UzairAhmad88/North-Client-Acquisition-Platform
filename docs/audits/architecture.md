# Website & Digital Presence Audit Architecture

## Overview

The Website & Digital Presence Audit Engine evaluates publicly accessible digital presence for businesses present in **Uzaii Develop By North's**.

It converts raw website observations across 12 audit categories into structured, evidence-backed findings and explainable health classifications without interpreting lead value or initiating external side effects.

```text
BUSINESS
   ↓
RESEARCH PROFILE
   ↓
AUDIT REQUEST
   ↓
TARGET VALIDATION (SSRF Check)
   ↓
SAFE WEB FETCH
   ↓
PAGE DISCOVERY (Same-domain max 10 pages)
   ↓
TECHNICAL ANALYSIS
   ↓
CONTENT & SEO ANALYSIS
   ↓
UX / LEAD-CAPTURE ANALYSIS
   ↓
DIGITAL PRESENCE ANALYSIS
   ↓
FINDINGS & EVIDENCE PERSISTENCE
   ↓
AUDIT SUMMARY & HEALTH SCORE
```

## Categories Covered

1. `WEBSITE`: Availability, status code, response time, canonical target.
2. `TECHNICAL`: Title, meta description, canonical, viewport, image alt text.
3. `SECURITY`: HTTPS availability, HTTP redirect, security headers.
4. `SEO`: Heading hierarchy, Open Graph, meta tags, sitemap/robots signals.
5. `MOBILE`: Viewport meta, responsive CSS vs fixed-width layout signals.
6. `PERFORMANCE`: Initial response time, body size, average page load.
7. `CONTENT`: Text length, paragraph/heading count, service mentions, content gaps.
8. `UX`: Usability signals, navigation link structure, CTA visibility.
9. `LEAD_CAPTURE`: Contact forms, booking forms, quote CTAs, phone CTAs, WhatsApp CTAs.
10. `SOCIAL`: Facebook, Instagram, LinkedIn, YouTube, TikTok, X, WhatsApp public links.
11. `BUSINESS_INFORMATION`: Comparison of website signals vs Research/Business DB records (`BUSINESS_INFORMATION_CONFLICT`).
12. `DIGITAL_PRESENCE`: Consolidated channel signals.
