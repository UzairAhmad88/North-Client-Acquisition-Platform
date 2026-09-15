"""Declarative mapping rules linking business categories, audit findings, and research signals to services."""

from typing import Dict, List

# Business Type to Service Category / Keyword Mappings
BUSINESS_TYPE_SERVICE_FIT: Dict[str, Dict[str, float]] = {
    "restaurant": {
        "restaurant_website": 95.0,
        "business_website": 85.0,
        "booking_system": 90.0,
        "reservation_system": 90.0,
        "automation": 75.0,
        "lead_automation": 70.0,
        "ai_assistant": 60.0,
    },
    "gym": {
        "gym_website": 95.0,
        "business_website": 85.0,
        "booking_system": 95.0,
        "membership_system": 95.0,
        "attendance_system": 90.0,
        "billing_system": 85.0,
        "workflow_automation": 80.0,
    },
    "fitness": {
        "gym_website": 95.0,
        "business_website": 85.0,
        "booking_system": 95.0,
        "membership_system": 95.0,
        "attendance_system": 90.0,
        "billing_system": 85.0,
    },
    "hotel": {
        "hotel_website": 95.0,
        "corporate_website": 85.0,
        "booking_system": 95.0,
        "reservation_system": 95.0,
        "management_system": 90.0,
        "billing_system": 85.0,
        "customer_support_agent": 80.0,
    },
    "school": {
        "school_website": 95.0,
        "corporate_website": 80.0,
        "student_management": 95.0,
        "attendance_system": 95.0,
        "billing_system": 90.0,
        "management_system": 90.0,
    },
    "education": {
        "school_website": 95.0,
        "corporate_website": 80.0,
        "student_management": 95.0,
        "attendance_system": 95.0,
        "billing_system": 90.0,
    },
    "healthcare": {
        "corporate_website": 85.0,
        "business_website": 85.0,
        "booking_system": 95.0,
        "attendance_system": 80.0,
        "crm": 85.0,
        "customer_support_agent": 75.0,
    },
    "retail": {
        "e_commerce": 95.0,
        "business_website": 85.0,
        "inventory_system": 95.0,
        "billing_system": 90.0,
        "crm": 85.0,
        "lead_automation": 75.0,
    },
    "general_business": {
        "business_website": 80.0,
        "corporate_website": 80.0,
        "crm": 75.0,
        "workflow_automation": 75.0,
        "business_dashboard": 70.0,
    },
}

# Audit Findings to Service Mappings
AUDIT_FINDING_SERVICE_MAPPINGS: Dict[str, Dict[str, float]] = {
    "NO_WEBSITE": {
        "business_website": 100.0,
        "corporate_website": 95.0,
        "landing_page": 90.0,
        "restaurant_website": 95.0,
        "gym_website": 95.0,
        "hotel_website": 95.0,
        "school_website": 95.0,
    },
    "WEBSITE_UNAVAILABLE": {
        "business_website": 95.0,
        "corporate_website": 90.0,
        "landing_page": 85.0,
    },
    "MISSING_CONTACT_FORM": {
        "landing_page": 85.0,
        "business_website": 80.0,
        "lead_automation": 90.0,
        "crm": 85.0,
    },
    "NO_BOOKING_CTA": {
        "booking_system": 95.0,
        "reservation_system": 90.0,
        "workflow_automation": 80.0,
    },
    "NO_CLEAR_CTA": {
        "landing_page": 90.0,
        "business_website": 85.0,
        "lead_automation": 85.0,
    },
    "MISSING_MOBILE_VIEWPORT": {
        "business_website": 90.0,
        "corporate_website": 85.0,
        "landing_page": 85.0,
    },
    "WEAK_SEO_METADATA": {
        "business_website": 75.0,
        "corporate_website": 75.0,
        "landing_page": 70.0,
    },
    "NO_OBVIOUS_LEAD_CAPTURE": {
        "lead_automation": 95.0,
        "crm": 90.0,
        "landing_page": 85.0,
        "notification_automation": 80.0,
    },
}

# Research Signals to Service Mappings
RESEARCH_SIGNAL_SERVICE_MAPPINGS: Dict[str, Dict[str, float]] = {
    "no_online_booking": {
        "booking_system": 90.0,
        "reservation_system": 85.0,
    },
    "appointment_based_services": {
        "booking_system": 95.0,
        "reservation_system": 90.0,
        "workflow_automation": 80.0,
    },
    "no_online_ordering": {
        "e_commerce": 90.0,
        "inventory_system": 85.0,
    },
    "membership_services": {
        "membership_system": 95.0,
        "billing_system": 90.0,
        "crm": 85.0,
    },
    "manual_contact_method": {
        "workflow_automation": 90.0,
        "lead_automation": 90.0,
        "ai_assistant": 85.0,
        "customer_support_agent": 85.0,
    },
    "multiple_locations": {
        "management_system": 90.0,
        "attendance_system": 85.0,
        "business_dashboard": 90.0,
    },
}
