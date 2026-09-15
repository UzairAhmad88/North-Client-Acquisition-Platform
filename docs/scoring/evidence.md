# Score Evidence & Traceability

## Evidence Structure

Every score snapshot records evidence references linking back to underlying data models:

```json
{
  "business_id": "8f3b2a1c-...",
  "has_website": true,
  "audit_id": "4d2e1f0a-...",
  "research_records_count": 5,
  "components": {
    "website_need": ["crm:business:website_url=Present", "audit:4d2e1f0a-..."],
    "online_presence": ["audit:4d2e1f0a-...", "research:records_count=5"],
    "lead_capture": ["audit:4d2e1f0a-..."],
    "automation_potential": ["audit:4d2e1f0a-..."],
    "business_activity": ["crm:business:status=ACTIVE"],
    "contactability": ["crm:business:phone=+1...", "crm:business:email=info@..."],
    "service_fit": ["services:catalog_size=12"]
  }
}
```
