import re
import uuid
from enum import Enum
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.business import Business
from app.repositories.business import BusinessRepository
from app.schemas.business import (
    BusinessCreate,
    BusinessDataQuality,
    BusinessDuplicateCheckResponse,
    BusinessDuplicateMatch,
    BusinessUpdate,
)


class BusinessService:
    @staticmethod
    def normalize_name(name: str) -> str:
        if not name:
            return ""
        # Lowercase, replace non-alphanumeric chars with space, collapse spaces
        cleaned = re.sub(r"[^\w\s]", "", name.lower())
        return re.sub(r"\s+", " ", cleaned).strip()

    @staticmethod
    def normalize_phone(phone: Optional[str]) -> Optional[str]:
        if not phone:
            return None
        # Keep digits and leading +
        digits = re.sub(r"[^\d+]", "", phone)
        return digits if digits else None

    @staticmethod
    def normalize_email(email: Optional[str]) -> Optional[str]:
        if not email:
            return None
        return email.strip().lower()

    @staticmethod
    def normalize_website(url: Optional[str]) -> Optional[str]:
        if not url:
            return None
        cleaned = url.strip().lower()
        cleaned = re.sub(r"^https?://", "", cleaned)
        cleaned = re.sub(r"^www\.", "", cleaned)
        cleaned = cleaned.rstrip("/")
        return cleaned if cleaned else None

    @classmethod
    def calculate_data_quality(cls, business: Business) -> BusinessDataQuality:
        score = 100
        missing_fields: List[str] = []
        warnings: List[str] = []

        if not business.website_url or not business.website_url.strip():
            score -= 20
            missing_fields.append("website_url")
            warnings.append("No website recorded.")

        if not business.email or not business.email.strip():
            score -= 15
            missing_fields.append("email")
            warnings.append("No email contact recorded.")

        if not business.phone or not business.phone.strip():
            score -= 15
            missing_fields.append("phone")
            warnings.append("No phone contact recorded.")

        if not business.city or not business.city.strip():
            score -= 15
            missing_fields.append("city")
            warnings.append("No location city recorded.")

        if not business.address or not business.address.strip():
            score -= 10
            missing_fields.append("address")

        if not business.description or not business.description.strip():
            score -= 10
            missing_fields.append("description")

        if not business.category:
            score -= 5
            missing_fields.append("category")

        if not business.source_url:
            score -= 5
            missing_fields.append("source_url")

        final_score = max(0, score)
        return BusinessDataQuality(
            score=final_score,
            missing_fields=missing_fields,
            warnings=warnings,
        )

    @classmethod
    def check_duplicates(
        cls,
        db: Session,
        name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        website_url: Optional[str] = None,
        city: Optional[str] = None,
        source: Optional[str] = None,
        external_id: Optional[str] = None,
        exclude_id: Optional[uuid.UUID] = None,
    ) -> BusinessDuplicateCheckResponse:
        norm_name = cls.normalize_name(name)
        norm_phone = cls.normalize_phone(phone)
        norm_email = cls.normalize_email(email)
        norm_website = cls.normalize_website(website_url)

        candidates = BusinessRepository.find_candidate_duplicates(
            db=db,
            normalized_name=norm_name,
            normalized_phone=norm_phone,
            normalized_email=norm_email,
            normalized_website=norm_website,
            city=city,
            source=source,
            external_id=external_id,
            exclude_id=exclude_id,
        )

        matches: List[BusinessDuplicateMatch] = []
        all_signals: set[str] = set()
        max_confidence = 0.0

        for candidate in candidates:
            signals: List[str] = []
            cand_confidence = 0.0

            if (
                external_id
                and source
                and candidate.source == source
                and candidate.external_id == external_id
            ):
                signals.append("same_source_external_id")
                cand_confidence = max(cand_confidence, 0.99)

            if norm_email and candidate.normalized_email == norm_email:
                signals.append("same_email")
                cand_confidence = max(cand_confidence, 0.95)

            if norm_website and candidate.normalized_website == norm_website:
                signals.append("same_website_domain")
                cand_confidence = max(cand_confidence, 0.90)

            if norm_phone and candidate.normalized_phone == norm_phone:
                signals.append("same_phone")
                cand_confidence = max(cand_confidence, 0.85)

            if (
                norm_name
                and city
                and candidate.normalized_name == norm_name
                and (candidate.city and candidate.city.lower() == city.lower())
            ):
                signals.append("same_name_and_city")
                cand_confidence = max(cand_confidence, 0.80)

            if signals:
                all_signals.update(signals)
                max_confidence = max(max_confidence, cand_confidence)
                matches.append(
                    BusinessDuplicateMatch(
                        business_id=candidate.id,
                        name=candidate.name,
                        confidence=round(cand_confidence, 2),
                        signals=signals,
                    )
                )

        possible_duplicate = max_confidence >= 0.70
        return BusinessDuplicateCheckResponse(
            possible_duplicate=possible_duplicate,
            confidence=round(max_confidence, 2),
            signals=sorted(list(all_signals)),
            matches=matches,
        )

    @classmethod
    def create_business(
        cls,
        db: Session,
        business_in: BusinessCreate,
        user_id: Optional[uuid.UUID] = None,
    ) -> Business:
        business_data = business_in.model_dump()
        business_data["normalized_name"] = cls.normalize_name(business_in.name)
        business_data["normalized_phone"] = cls.normalize_phone(business_in.phone)
        business_data["normalized_email"] = cls.normalize_email(business_in.email)
        business_data["normalized_website"] = cls.normalize_website(business_in.website_url)
        business_data["created_by_user_id"] = user_id
        business_data["status"] = "ACTIVE"

        business = BusinessRepository.create(db, business_data)
        return business

    @classmethod
    def get_business(cls, db: Session, business_id: uuid.UUID) -> Business:
        business = BusinessRepository.get_by_id(db, business_id)
        if not business:
            raise AppError(
                code="BUSINESS_NOT_FOUND",
                message="Business not found.",
                status_code=404,
            )
        return business

    @classmethod
    def list_businesses(
        cls,
        db: Session,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        status: Optional[str] = None,
        industry: Optional[str] = None,
        business_type: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        source: Optional[str] = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> Tuple[List[Business], int]:
        return BusinessRepository.list_businesses(
            db=db,
            page=page,
            page_size=page_size,
            search=search,
            status=status,
            industry=industry,
            business_type=business_type,
            city=city,
            country=country,
            source=source,
            sort=sort,
            order=order,
        )

    @classmethod
    def update_business(
        cls,
        db: Session,
        business_id: uuid.UUID,
        business_in: BusinessUpdate,
    ) -> Business:
        business = cls.get_business(db, business_id)
        update_dict = business_in.model_dump(exclude_unset=True)

        if "name" in update_dict and update_dict["name"]:
            update_dict["normalized_name"] = cls.normalize_name(update_dict["name"])
        if "phone" in update_dict:
            update_dict["normalized_phone"] = cls.normalize_phone(update_dict["phone"])
        if "email" in update_dict:
            update_dict["normalized_email"] = cls.normalize_email(update_dict["email"])
        if "website_url" in update_dict:
            update_dict["normalized_website"] = cls.normalize_website(update_dict["website_url"])
        if "status" in update_dict and isinstance(update_dict["status"], Enum):
            update_dict["status"] = update_dict["status"].value

        updated = BusinessRepository.update(db, business, update_dict)
        return updated

    @classmethod
    def archive_business(cls, db: Session, business_id: uuid.UUID) -> Business:
        business = cls.get_business(db, business_id)
        if business.status == "ARCHIVED":
            return business
        return BusinessRepository.archive(db, business)

    @classmethod
    def restore_business(cls, db: Session, business_id: uuid.UUID) -> Business:
        business = cls.get_business(db, business_id)
        if business.status == "ACTIVE":
            return business
        return BusinessRepository.restore(db, business)
