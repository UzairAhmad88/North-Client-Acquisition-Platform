"""Requirement Extractor engine parsing raw client text and conversation context."""

import re
from typing import Any, Dict, List, Tuple
from agents.requirements.models import ExtractedRequirementSchema


class RequirementExtractor:
    """Extracts explicit and inferred requirements, business goals, problems, and target users."""

    CATEGORY_PATTERNS = {
        "BOOKING": [r"book(ing)?", r"appointment", r"reservation", r"schedule a call", r"calendar"],
        "PAYMENT": [r"payment", r"credit card", r"stripe", r"checkout", r"billing", r"invoice"],
        "WEBSITE": [r"website", r"web page", r"landing page", r"site", r"domain"],
        "AUTOMATION": [r"automat(e|ion)", r"workflow", r"bot", r"webhook", r"sync"],
        "AI_FEATURE": [r"ai", r"chatbot", r"assistant", r"gpt", r"agent", r"llm"],
        "CRM": [r"crm", r"customer relationship", r"lead management", r"contact list"],
        "INVENTORY": [r"inventory", r"stock", r"warehouse", r"product catalogue"],
        "DASHBOARD": [r"dashboard", r"analytics", r"reporting", r"metrics", r"admin panel"],
        "AUTHENTICATION": [r"login", r"signup", r"user accounts", r"roles", r"permissions", r"auth"],
        "NOTIFICATION": [r"notification", r"email alert", r"sms alert", r"whatsapp message", r"reminder"],
        "MOBILE": [r"mobile app", r"ios", r"android", r"react native"],
        "DESIGN": [r"design", r"branding", r"logo", r"theme", r"custom layout"],
    }

    BUSINESS_GOALS = [
        (r"increase bookings|get more clients|grow sales", "Increase online bookings and client acquisitions"),
        (r"save time|reduce manual|automate", "Reduce manual operational effort through business automation"),
        (r"professional presence|modern look|rebrand", "Establish a modern, professional digital presence"),
        (r"track sales|manage inventory|centralize", "Centralize business data and customer operations"),
    ]

    BUSINESS_PROBLEMS = [
        (r"manual appointment|paper work|excel", "Manual appointment scheduling and tracking friction"),
        (r"slow response|missed inquiries|lost leads", "Delayed customer response times and lost lead inquiries"),
        (r"no website|outdated site", "Lack of an active modern digital presence"),
        (r"scattered data|no crm", "Scattered customer information across unintegrated channels"),
    ]

    @classmethod
    def extract(
        cls, message_body: str, message_id: str = None
    ) -> Tuple[List[ExtractedRequirementSchema], str, str, List[str]]:
        """
        Parses text and returns:
        (extracted_requirements, business_goal, business_problem, target_users)
        """
        requirements: List[ExtractedRequirementSchema] = []
        body_lower = message_body.lower()

        # 1. Business Goal Extraction
        goal = "Improve business operations and digital capability"
        for pattern, desc in cls.BUSINESS_GOALS:
            if re.search(pattern, body_lower):
                goal = desc
                break

        # 2. Business Problem Extraction
        problem = "Need modern digital solution for business growth"
        for pattern, desc in cls.BUSINESS_PROBLEMS:
            if re.search(pattern, body_lower):
                problem = desc
                break

        # 3. Target Users Extraction
        users = ["Customers", "Business Staff"]
        if "admin" in body_lower or "owner" in body_lower:
            users.append("Business Owner / Admin")
        if "patient" in body_lower:
            users.append("Patients")
        if "student" in body_lower:
            users.append("Students")

        # 4. Requirement Category Matching
        matched_categories = set()
        for cat, patterns in cls.CATEGORY_PATTERNS.items():
            for p in patterns:
                if re.search(p, body_lower):
                    matched_categories.add(cat)
                    break

        for cat in matched_categories:
            explicit = True
            confidence = "HIGH"
            title = f"{cat.replace('_', ' ').title()} System Requirement"
            desc = f"Client requested {cat.lower().replace('_', ' ')} functionality."

            requirements.append(
                ExtractedRequirementSchema(
                    category=cat,
                    title=title,
                    description=desc,
                    source_type="CLIENT_MESSAGE",
                    source_reference=message_id,
                    explicit=explicit,
                    confidence=confidence,
                    status="PROPOSED",
                    priority="HIGH" if cat in ("WEBSITE", "BOOKING", "PAYMENT") else "MEDIUM",
                    evidence_text=message_body[:250],
                )
            )

        # 5. Inferred System Requirement (e.g. if booking is requested, infer appointment database)
        if "BOOKING" in matched_categories and "AUTHENTICATION" not in matched_categories:
            requirements.append(
                ExtractedRequirementSchema(
                    category="AUTHENTICATION",
                    title="User Authentication & Roles",
                    description="Inferred requirement: Staff login and customer identity management for bookings.",
                    source_type="AI_INFERENCE",
                    source_reference=message_id,
                    explicit=False,
                    confidence="MEDIUM",
                    status="PROPOSED",
                    priority="MEDIUM",
                    evidence_text="Inferred from booking workflow requirement.",
                )
            )

        return requirements, goal, problem, users
