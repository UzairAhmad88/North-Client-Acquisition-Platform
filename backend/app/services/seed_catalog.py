from sqlalchemy.orm import Session

from app.repositories.service import ServiceRepository

INITIAL_NORTHS_CATALOG = [
    {
        "name": "Business Website",
        "slug": "business-website",
        "category": "WEB_DEVELOPMENT",
        "short_description": "High-converting business website tailored for local brands.",
        "description": (
            "Professional web presence with custom design, mobile optimization, "
            "lead capture forms, and SEO foundation."
        ),
        "delivery_model": "FIXED_PROJECT",
        "pricing_model": "STARTING_AT",
        "base_price": 750.0,
        "currency": "USD",
        "estimated_duration_days": 14,
        "is_featured": True,
        "is_active": True,
        "features": [
            "Responsive UI",
            "Lead Contact Forms",
            "SEO Optimization",
            "Fast Load Performance",
        ],
        "requirements": [
            "Brand Assets",
            "Business Description",
            "Contact Info",
            "Domain Access",
        ],
        "target_business_types": ["SERVICE", "RETAIL", "CLINIC", "ACADEMY"],
    },
    {
        "name": "Restaurant Website & Menu System",
        "slug": "restaurant-website",
        "category": "WEB_DEVELOPMENT",
        "short_description": "Interactive restaurant website with online digital menu.",
        "description": (
            "Custom restaurant web platform showcasing menus, location maps, "
            "opening hours, and online reservation requests."
        ),
        "delivery_model": "FIXED_PROJECT",
        "pricing_model": "STARTING_AT",
        "base_price": 950.0,
        "currency": "USD",
        "estimated_duration_days": 18,
        "is_featured": True,
        "is_active": True,
        "features": [
            "Digital Menu Display",
            "Reservation Form",
            "Google Maps Integration",
            "Mobile Touch Optimization",
        ],
        "requirements": [
            "Menu Pricing Data",
            "High-res Food Photos",
            "Operating Hours",
        ],
        "target_business_types": ["RESTAURANT", "CAFE"],
    },
    {
        "name": "Gym & Fitness Club Platform",
        "slug": "gym-website",
        "category": "WEB_DEVELOPMENT",
        "short_description": "Modern fitness center portal featuring membership tiers.",
        "description": (
            "Dynamic web platform designed for gyms and academies to highlight "
            "class schedules, trainer rosters, and membership signups."
        ),
        "delivery_model": "FIXED_PROJECT",
        "pricing_model": "STARTING_AT",
        "base_price": 1100.0,
        "currency": "USD",
        "estimated_duration_days": 21,
        "is_featured": False,
        "is_active": True,
        "features": [
            "Class Schedule Manager",
            "Membership Tiers",
            "Trainer Showcase",
            "Trial Pass Request Form",
        ],
        "requirements": [
            "Membership Pricing",
            "Class Timetable",
            "Trainer Bios",
        ],
        "target_business_types": ["GYM", "ACADEMY"],
    },
    {
        "name": "Custom CRM & Lead Management System",
        "slug": "crm-system",
        "category": "SOFTWARE_DEVELOPMENT",
        "short_description": "Customized CRM portal for sales team tracking.",
        "description": (
            "Tailored cloud software to manage business organization profiles, "
            "lead sales pipelines, status lifecycle transitions, and team tasks."
        ),
        "delivery_model": "FIXED_PROJECT",
        "pricing_model": "CUSTOM",
        "base_price": 2500.0,
        "currency": "USD",
        "estimated_duration_days": 30,
        "is_featured": True,
        "is_active": True,
        "features": [
            "Organization Directory",
            "Pipeline Kanban/Table",
            "Lifecycle Timestamps",
            "Role-based Security",
        ],
        "requirements": ["Business Process Workflow", "User Roles List"],
        "target_business_types": ["SERVICE", "REAL_ESTATE", "CLINIC"],
    },
    {
        "name": "Business Executive Dashboard",
        "slug": "business-dashboard",
        "category": "SOFTWARE_DEVELOPMENT",
        "short_description": "Unified analytics dashboard presenting business metrics.",
        "description": (
            "Interactive reporting dashboard visualizing client acquisition analytics, "
            "revenue metrics, conversion rates, and task tracking."
        ),
        "delivery_model": "FIXED_PROJECT",
        "pricing_model": "STARTING_AT",
        "base_price": 1500.0,
        "currency": "USD",
        "estimated_duration_days": 20,
        "is_featured": False,
        "is_active": True,
        "features": [
            "Real-time Metrics",
            "Interactive Charts",
            "CSV/PDF Exports",
            "Filtered Views",
        ],
        "requirements": [
            "Database Connections / API Feeds",
            "Key Performance Indicators List",
        ],
        "target_business_types": ["SERVICE", "RETAIL", "TRAVEL_AGENCY"],
    },
    {
        "name": "Lead Management & Outreach Automation",
        "slug": "lead-management-automation",
        "category": "BUSINESS_AUTOMATION",
        "short_description": "Automated workflow system for lead routing.",
        "description": (
            "Eliminate manual lead follow-up delays by automating incoming "
            "inquiry notifications, CRM status triggers, and task assignment."
        ),
        "delivery_model": "FIXED_PROJECT",
        "pricing_model": "STARTING_AT",
        "base_price": 850.0,
        "currency": "USD",
        "estimated_duration_days": 10,
        "is_featured": True,
        "is_active": True,
        "features": [
            "Instant Email/WhatsApp Alerting",
            "Automatic Lead Routing",
            "Status Change Triggers",
        ],
        "requirements": [
            "Zapier/Make or API Access",
            "Notification Recipient Rules",
        ],
        "target_business_types": ["SERVICE", "REAL_ESTATE", "CLINIC", "TRAVEL_AGENCY"],
    },
    {
        "name": "AI Customer Support Assistant",
        "slug": "ai-customer-support",
        "category": "AI_SYSTEMS",
        "short_description": "Custom-trained AI assistant to answer FAQ inquiries.",
        "description": (
            "Intelligent AI web widget trained on company knowledge bases to handle "
            "customer questions 24/7 and qualify prospective leads."
        ),
        "delivery_model": "FIXED_PROJECT",
        "pricing_model": "CUSTOM",
        "base_price": 2000.0,
        "currency": "USD",
        "estimated_duration_days": 25,
        "is_featured": True,
        "is_active": True,
        "features": [
            "Knowledge Base RAG Training",
            "Lead Information Capture",
            "Human Escalation Path",
            "24/7 Availability",
        ],
        "requirements": ["FAQ Documents", "Product/Service Handbooks"],
        "target_business_types": ["SERVICE", "RETAIL", "HOTEL", "CLINIC"],
    },
    {
        "name": "AI Lead Qualification System",
        "slug": "ai-lead-qualification",
        "category": "AI_SYSTEMS",
        "short_description": "Automated AI agent evaluating public presence signals.",
        "description": (
            "Autonomous AI system inspecting target business web presence, "
            "calculating deterministic fit scores, and suggesting tailored services."
        ),
        "delivery_model": "FIXED_PROJECT",
        "pricing_model": "CUSTOM",
        "base_price": 3000.0,
        "currency": "USD",
        "estimated_duration_days": 35,
        "is_featured": True,
        "is_active": True,
        "features": [
            "Web Presence Audit",
            "Deterministic Fit Scoring",
            "Automated Opportunity Reports",
        ],
        "requirements": ["Target Market Criteria", "Scoring Weight Rules"],
        "target_business_types": ["SERVICE", "REAL_ESTATE", "AGENCY"],
    },
]


def seed_service_catalog(db: Session) -> int:
    seeded_count = 0
    for service_data in INITIAL_NORTHS_CATALOG:
        slug = str(service_data["slug"])
        existing = ServiceRepository.get_by_slug(db, slug)
        if not existing:
            ServiceRepository.create(db, service_data)
            seeded_count += 1
    return seeded_count
